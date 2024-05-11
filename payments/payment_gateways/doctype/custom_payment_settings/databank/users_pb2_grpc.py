# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import users_pb2 as users__pb2


class userServiceStub(object):
    """UserS service rpc definitions
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetBalance = channel.unary_unary(
                '/users.userService/GetBalance',
                request_serializer=users__pb2.request.SerializeToString,
                response_deserializer=users__pb2.response.FromString,
                )
        self.CreateAccount = channel.unary_unary(
                '/users.userService/CreateAccount',
                request_serializer=users__pb2.request.SerializeToString,
                response_deserializer=users__pb2.response.FromString,
                )


class userServiceServicer(object):
    """UserS service rpc definitions
    """

    def GetBalance(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateAccount(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_userServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetBalance': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBalance,
                    request_deserializer=users__pb2.request.FromString,
                    response_serializer=users__pb2.response.SerializeToString,
            ),
            'CreateAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateAccount,
                    request_deserializer=users__pb2.request.FromString,
                    response_serializer=users__pb2.response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'users.userService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class userService(object):
    """UserS service rpc definitions
    """

    @staticmethod
    def GetBalance(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/users.userService/GetBalance',
            users__pb2.request.SerializeToString,
            users__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/users.userService/CreateAccount',
            users__pb2.request.SerializeToString,
            users__pb2.response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
