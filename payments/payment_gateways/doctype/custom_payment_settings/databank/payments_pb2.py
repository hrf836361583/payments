# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: payments.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0epayments.proto\x12\x08payments\"\xf6\x01\n\x08requests\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0e\n\x06\x64omain\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x0f\n\x07\x62\x61lance\x18\x04 \x01(\x01\x12\r\n\x05\x65mail\x18\x05 \x01(\t\x12\x12\n\npackage_id\x18\x06 \x01(\t\x12\r\n\x05token\x18\x07 \x01(\t\x12\x10\n\x08receiver\x18\x08 \x01(\t\x12\x0e\n\x06\x61mount\x18\t \x01(\x01\x12\x12\n\nvoucherPin\x18\n \x01(\t\x12\x11\n\tdebugInfo\x18\x0b \x01(\t\x12\x15\n\rtransactionId\x18\x0c \x01(\t\x12\x13\n\x0b\x62\x61lanceType\x18\r \x01(\t\"\x84\x02\n\x05reply\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0e\n\x06\x64omain\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x0f\n\x07\x62\x61lance\x18\x04 \x01(\x01\x12\r\n\x05\x65mail\x18\x05 \x01(\t\x12 \n\x06status\x18\x06 \x01(\x0e\x32\x10.payments.Status\x12\r\n\x05token\x18\x07 \x01(\t\x12\x1e\n\x05\x65rror\x18\x08 \x01(\x0b\x32\x0f.payments.Error\x12\x1c\n\x04info\x18\t \x01(\x0b\x32\x0e.payments.Info\x12\"\n\x07success\x18\n \x01(\x0b\x32\x11.payments.Success\x12\x14\n\x0c\x62\x61lanceAfter\x18\x0b \x01(\x01\"?\n\x05\x45rror\x12\x1c\n\x14localizedDescription\x18\x01 \x01(\t\x12\x18\n\x10\x64\x65\x62ugDescription\x18\x02 \x01(\t\"A\n\x07Success\x12\x1c\n\x14localizedDescription\x18\x01 \x01(\t\x12\x18\n\x10\x64\x65\x62ugDescription\x18\x02 \x01(\t\"\x1b\n\x04Info\x12\x13\n\x0binformation\x18\x01 \x01(\t*A\n\x06Status\x12\x0f\n\x0bINFORMATION\x10\x00\x12\x0e\n\nSUCCESSFUL\x10\x01\x12\t\n\x05\x45RROR\x10\x02\x12\x0b\n\x07\x46\x41ILURE\x10\x03\x32\x80\x01\n\x0fpaymentsService\x12\x36\n\rCreditAccount\x12\x12.payments.requests\x1a\x0f.payments.reply\"\x00\x12\x35\n\x0c\x44\x65\x62itAccount\x12\x12.payments.requests\x1a\x0f.payments.reply\"\x00\x42&Z$prisons/services/payments/paymentspbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'payments_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z$prisons/services/payments/paymentspb'
  _globals['_STATUS']._serialized_start=701
  _globals['_STATUS']._serialized_end=766
  _globals['_REQUESTS']._serialized_start=29
  _globals['_REQUESTS']._serialized_end=275
  _globals['_REPLY']._serialized_start=278
  _globals['_REPLY']._serialized_end=538
  _globals['_ERROR']._serialized_start=540
  _globals['_ERROR']._serialized_end=603
  _globals['_SUCCESS']._serialized_start=605
  _globals['_SUCCESS']._serialized_end=670
  _globals['_INFO']._serialized_start=672
  _globals['_INFO']._serialized_end=699
  _globals['_PAYMENTSSERVICE']._serialized_start=769
  _globals['_PAYMENTSSERVICE']._serialized_end=897
# @@protoc_insertion_point(module_scope)
