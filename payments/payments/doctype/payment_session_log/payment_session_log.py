# Copyright (c) 2021, Frappe and contributors
# For license information, please see LICENSE

import json

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.query_builder import Interval
from frappe.query_builder.functions import Now
from frappe.utils import strip_html
from frappe.utils.data import cstr

from payments.types import TxData, RemoteServerInitiationPayload, GatewayProcessingResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from payments.controllers import PaymentController
	from payments.payments.doctype.payment_gateway.payment_gateway import PaymentGateway
	from payments.payments.doctype.payment_button.payment_button import PaymentButton

import collections.abc


def update(d, u):
	for k, v in u.items():
		if isinstance(v, collections.abc.Mapping):
			d[k] = update(d.get(k, {}), v)
		else:
			d[k] = v
	return d


PSLState = dict


class PaymentSessionLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		button: DF.Data | None
		correlation_id: DF.Data | None
		decline_reason: DF.Data | None
		flow_type: DF.Data | None
		gateway: DF.Data | None
		gateway_specific_state: DF.Code | None
		initiation_response_payload: DF.Code | None
		mandate: DF.Data | None
		processing_response_payload: DF.Code | None
		requires_data_capture: DF.Check
		status: DF.Data | None
		title: DF.Data | None
		tx_data: DF.Code | None
	# end: auto-generated types
	def update_tx_data(self, tx_data: TxData, status: str) -> None:
		d = json.loads(self.tx_data)
		update(d, tx_data)
		self.db_set(
			{
				"tx_data": frappe.as_json(d),
				"status": status,
			},
			commit=True,
		)

	def update_gateway_specific_state(self, data: dict, status: str) -> None:
		d = json.loads(self.gateway_specific_state) if self.gateway_specific_state else {}
		update(d, data)
		self.db_set(
			{
				"gateway_specific_state": frappe.as_json(d),
				"status": status,
			},
			commit=True,
		)

	def set_initiation_payload(
		self, initiation_payload: RemoteServerInitiationPayload, status: str
	) -> None:
		self.db_set(
			{
				"initiation_response_payload": frappe.as_json(initiation_payload),
				"status": status,
			},
			commit=True,
		)

	def set_processing_payload(
		self, processing_response: GatewayProcessingResponse, status: str
	) -> None:
		self.db_set(
			{
				"processing_response_payload": frappe.as_json(processing_response.payload),
				"status": status,
			},
			commit=True,
		)

	def load_state(self) -> PSLState:
		return frappe._dict(
			psl=frappe._dict(self.as_dict()),
			tx_data=TxData(**json.loads(self.tx_data)),
			gateway_data=json.loads(self.gateway_specific_state) if self.gateway_specific_state else {},
		)

	def get_controller(self) -> "PaymentController":
		"""
		Retrieves the payment controller associated with the current Payment Session Log's gateway.

		This method uses a JSON-encoded gateway value instead of a dynamic link
		for performance optimization. The controller is only fetched when necessary.

		Returns:
		    PaymentController: The cached document of the payment controller.

		Raises:
		    frappe.ValidationError: If no gateway is selected for this Payment Session Log.
		"""
		if not self.gateway:
			self.log_error("No gateway selected yet")
			frappe.throw(_("No gateway selected for this payment session"))
		d = json.loads(self.gateway)
		doctype, docname = d["gateway_settings"], d["gateway_controller"]
		return frappe.get_cached_doc(doctype, docname)

	def get_gateway(self) -> "PaymentGateway":
		"""
		Retrieves the Payment Gateway document associated with the current Payment Session Log.

		The 'gateway' attribute of the Payment Session Log serves a dual purpose,
		acting as both a data store and a filter for recovering the Payment Gateway document.

		Returns:
		    Payment Gateway: The most recent Payment Gateway document matching the stored gateway data.

		Raises:
		    frappe.ValidationError: If no gateway is selected for this Payment Session Log.
		"""
		if not self.gateway:
			self.log_error("No gateway selected yet")
			frappe.throw(_("No gateway selected for this payment session"))
		d = json.loads(self.gateway)
		return frappe.get_cached_doc("Payment Gateway", d["payment_gateway"])

	def get_button(self) -> "PaymentButton":
		if not self.button:
			self.log_error("No button selected yet")
			frappe.throw(_("No button selected for this payment session"))
		return frappe.get_cached_doc("Payment Button", self.button)

	@staticmethod
	def clear_old_logs(days=90):
		table = frappe.qb.DocType("Payment Session Log")
		frappe.db.delete(
			table, filters=(table.modified < (Now() - Interval(days=days))) & (table.status == "Success")
		)


@frappe.whitelist(allow_guest=True)
def select_button(pslName: str = None, buttonName: str = None) -> str:
	try:
		psl = frappe.get_cached_doc("Payment Session Log", pslName)
	except Exception:
		e = frappe.log_error("Payment Session Log not found", reference_doctype="Payment Session Log")
		# Ensure no more details are leaked than the error log reference
		frappe.local.message_log = [_("Server Failure!<br>{}").format(e)]
		return
	try:
		btn: PaymentButton = frappe.get_cached_doc("Payment Button", buttonName)
	except Exception:
		e = frappe.log_error("Payment Button not found", reference_doctype="Payment Button")
		# Ensure no more details are leaked than the error log reference
		frappe.local.message_log = [_("Server Failure!<br>{}").format(e)]
		return

	psl.db_set(
		{
			"button": buttonName,
			"requires_data_capture": btn.requires_data_catpure,
			"gateway": json.dumps(
				{
					"gateway_settings": btn.gateway_settings,
					"gateway_controller": btn.gateway_controller,
					"payment_gateway": btn.payment_gateway,
				}
			),
		}
	)
	# once state set: reload the page to activate widget
	return {"reload": True}


def create_log(
	tx_data: TxData,
	controller: "PaymentController" = None,
	status: str = "Created",
) -> PaymentSessionLog:

	log = frappe.new_doc("Payment Session Log")
	log.tx_data = frappe.as_json(tx_data)
	log.status = status
	if controller:
		log.gateway = json.dumps(
			{
				"gateway_settings": controller.doctype,
				"gateway_controller": controller.name,
			}
		)

	log.insert(ignore_permissions=True)
	return log


@frappe.whitelist()
def resync(method, name, request_data):
	_retry_job(name)


def _retry_job(job: str):
	frappe.only_for("System Manager")

	doc = frappe.get_doc("Payment Session Log", job)
	if not doc.method.startswith("payments.payment_gateways.") or doc.status != "Error":
		return

	doc.db_set("status", "Queued", update_modified=False)
	doc.db_set("traceback", "", update_modified=False)

	frappe.enqueue(
		method=doc.method,
		queue="short",
		timeout=300,
		is_async=True,
		payload=json.loads(doc.request_data),
		request_id=doc.name,
		enqueue_after_commit=True,
	)


@frappe.whitelist()
def bulk_retry(names):
	if isinstance(names, str):
		names = json.loads(names)
	for name in names:
		_retry_job(name)
