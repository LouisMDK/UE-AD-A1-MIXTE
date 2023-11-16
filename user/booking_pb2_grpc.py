# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import booking_pb2 as booking__pb2


class BookingStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAllBookings = channel.unary_stream(
                '/Booking/GetAllBookings',
                request_serializer=booking__pb2.EmptyForBooking.SerializeToString,
                response_deserializer=booking__pb2.Book.FromString,
                )
        self.GetBookingByUser = channel.unary_unary(
                '/Booking/GetBookingByUser',
                request_serializer=booking__pb2.User.SerializeToString,
                response_deserializer=booking__pb2.Book.FromString,
                )
        self.AddBookingByUser = channel.unary_unary(
                '/Booking/AddBookingByUser',
                request_serializer=booking__pb2.AddBooker.SerializeToString,
                response_deserializer=booking__pb2.Book.FromString,
                )


class BookingServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAllBookings(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBookingByUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddBookingByUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BookingServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAllBookings': grpc.unary_stream_rpc_method_handler(
                    servicer.GetAllBookings,
                    request_deserializer=booking__pb2.EmptyForBooking.FromString,
                    response_serializer=booking__pb2.Book.SerializeToString,
            ),
            'GetBookingByUser': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBookingByUser,
                    request_deserializer=booking__pb2.User.FromString,
                    response_serializer=booking__pb2.Book.SerializeToString,
            ),
            'AddBookingByUser': grpc.unary_unary_rpc_method_handler(
                    servicer.AddBookingByUser,
                    request_deserializer=booking__pb2.AddBooker.FromString,
                    response_serializer=booking__pb2.Book.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Booking', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Booking(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAllBookings(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/Booking/GetAllBookings',
            booking__pb2.EmptyForBooking.SerializeToString,
            booking__pb2.Book.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBookingByUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Booking/GetBookingByUser',
            booking__pb2.User.SerializeToString,
            booking__pb2.Book.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddBookingByUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Booking/AddBookingByUser',
            booking__pb2.AddBooker.SerializeToString,
            booking__pb2.Book.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
