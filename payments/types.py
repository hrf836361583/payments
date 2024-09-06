from dataclasses import dataclass
from typing import Optional, Dict, List

from types import MappingProxyType

from frappe.model.document import Document

from enum import Enum


class SessionType(str, Enum):
	"""We distinguish three distinct flow types.

	They may be chained into a composed flow from the business logic, for example a
	mandate_aquisition can precede a mandated_charge in a continuous flow.
	"""

	charge = "charge"
	mandated_charge = "mandated_charge"
	mandate_acquisition = "mandate_acquisition"


@dataclass
class SessionStates:
	"""Define gateway states in their respective category"""

	success: list[str]
	pre_authorized: list[str]
	processing: list[str]
	declined: list[str]


@dataclass
class FrontendDefaults:
	"""Define gateway widget frontend defaults for css, js and the wrapper components
	or a data capture form.

	All four are html snippets and jinja templates rendered against this gateway's
	PaymentController instance and its RemoteServerInitiationPayload.

	These are loaded into the Payment Button document and give users a starting point
	to customize payment button(s).

	If the button implements a third party widget, then gateway_* are rendered into the checkout.
	If the button implements first party data capture, then data_capture is rendered.
	"""

	gateway_css: str
	gateway_js: str
	gateway_wrapper: str
	data_capture: str


class RemoteServerInitiationPayload(dict):
	"""The remote server payload returned during flow initiation.

	Interface: Remote Server -> Concrete Gateway Implementation
	           Concrete Gateway Implementation -> Payment Gateway Controller
	           Payment Gateway Controller -> Payment Gateway Controller
	"""

	pass


@dataclass(frozen=True)
class Initiated:
	"""The return data structure from a gateway flow initiation.

	Interface: Concrete Gateway Implementation -> Payment Gateway Controller

	correlation_id:
	    stored as request_id in the integration log to correlate
	    remote and local request
	"""

	correlation_id: str
	payload: RemoteServerInitiationPayload


@dataclass
class TxData:
	"""The main data interchange format between refdoc and controller.

	Interface: Ref Doc -> Payment Gateway Controller

	"""

	amount: float
	currency: str
	reference_doctype: str
	reference_docname: str
	payer_contact: dict  # as: contact.as_dict()
	payer_address: dict  # as: address.as_dict()
	# [Program, Points, Amount]
	loyalty_points: list[str, float, float] | None  # for display purpose only
	discount_amount: float | None  # for display purpose only
	display_reference_doctype: str | None = None
	display_reference_docname: str | None = None
	# TODO: tx data for subscriptions, pre-authorized, require-mandate and other flows


@dataclass(frozen=True)
class GatewayProcessingResponse:
	"""The remote server payload returned during flow processing.

	Interface: Remote Server -> Concrete Gateway Implementation
	           Concrete Gateway Implementation -> Payment Gateway Controller
	           Payment Gateway Controller -> Payment Gateway Controller
	"""

	hash: bytes | None
	message: bytes | None
	payload: dict


class PaymentMandate(Document):
	"""All payment mandate doctypes should inherit from this base class.

	Interface: Concrete Gateway Implementation -> Payment Gateway Controller
	"""


@dataclass
class Proceeded:
	"""The return data structure from a call to proceed() which initiates the flow.

	Interface: Payment Gateway Controller -> calling control flow (backend or frontend)

	integration:
	    The name of the integration (gateway doctype).
	    Exposed so that the controlling business flow can case switch on it.
	"""

	integration: str
	psltype: SessionType
	mandate: PaymentMandate | None  # TODO: will this be serialized when called from the frontend?
	txdata: TxData
	payload: RemoteServerInitiationPayload


@dataclass
class ActionAfterProcessed:
	href: str
	label: str
	redirect_after_milliseconds: int | None = None


@dataclass
class _Processed:
	"""The return data structure after processing gateway response (by a Ref Doc hook).

	Interface: Ref Doc -> Payment Gateway Controller

	Implementation Note:
	If implemented via a server action you may aproximate by using frappe._dict.

	message:
	    a (translated) message to show to the user
	action:
	    an action for the frontend to perfom
	"""

	message: str
	action: dict  # checked against ActionAfterProcessed


@dataclass
class Processed(_Processed):
	"""The return data structure after processing gateway response.

	Interface:
	Payment Gateway Controller -> Calling Buisness Flow (backend or frontend)

	Implementation Note:
	If the Ref Doc exposes a hook method, this should return _Processed, instead.

	message:
	    a (translated) message to show to the user
	action:
	    an action for the frontend to perfom
	status_changed_to:
	    the new status of the payment session after processing
	indicator_color:
	    the new indicator color for visual display of the new status
	payload:
	    a gateway specific payload that is understood by a gateway-specific frontend
	    implementation
	"""

	status_changed_to: str
	indicator_color: str
	payload: GatewayProcessingResponse


# for nicer DX using an LSP


class PSLName(str):
	"""The name of the primary local reference to identify an ongoing payment gateway flow.

	Interface: Payment Gateway Controller -> Ref Doc -> Payment Gateway Controller
	           Payment Gateway Controller -> Remote Server -> Payment Gateway Controller
	           Payment Gateway Controller -> Calling Buisness Flow -> Payment Gateway Controller

	It is first returned by a call to initiate and should be stored on
	the Ref Doc for later reference.
	"""


class PaymentUrl(str):
	"""The payment url in case the gateway implements it.

	Interface: Payment Gateway Controller -> Ref Doc

	It is rendered from the integration log reference and the URL of the current site.
	"""
