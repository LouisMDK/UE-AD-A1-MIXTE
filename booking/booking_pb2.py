# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: booking.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rbooking.proto\"3\n\x04\x42ook\x12\x0e\n\x06userid\x18\x01 \x01(\t\x12\x1b\n\x05\x64\x61tes\x18\x02 \x03(\x0b\x32\x0c.BookingDate\"\x16\n\x04User\x12\x0e\n\x06userid\x18\x01 \x01(\t\"=\n\x0c\x42ookingAdder\x12\x0e\n\x06userid\x18\x01 \x01(\t\x12\x0f\n\x07movieid\x18\x02 \x01(\t\x12\x0c\n\x04\x64\x61te\x18\x03 \x01(\t\"+\n\x0b\x42ookingDate\x12\x0c\n\x04\x64\x61te\x18\x01 \x01(\t\x12\x0e\n\x06movies\x18\x02 \x03(\t\"\x11\n\x0f\x45mptyForBooking2\x80\x01\n\x07\x42ooking\x12-\n\x0eGetAllBookings\x12\x10.EmptyForBooking\x1a\x05.Book\"\x00\x30\x01\x12\"\n\x10GetBookingByUser\x12\x05.User\x1a\x05.Book\"\x00\x12\"\n\x10\x41\x64\x64\x42ookingByUser\x12\x05.User\x1a\x05.Book\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'booking_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BOOK']._serialized_start=17
  _globals['_BOOK']._serialized_end=68
  _globals['_USER']._serialized_start=70
  _globals['_USER']._serialized_end=92
  _globals['_BOOKINGADDER']._serialized_start=94
  _globals['_BOOKINGADDER']._serialized_end=155
  _globals['_BOOKINGDATE']._serialized_start=157
  _globals['_BOOKINGDATE']._serialized_end=200
  _globals['_EMPTYFORBOOKING']._serialized_start=202
  _globals['_EMPTYFORBOOKING']._serialized_end=219
  _globals['_BOOKING']._serialized_start=222
  _globals['_BOOKING']._serialized_end=350
# @@protoc_insertion_point(module_scope)
