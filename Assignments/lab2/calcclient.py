"""The Python implementation of the GRPC calc client."""

from __future__ import print_function

import grpc

import calc_pb2
import calc_pb2_grpc

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50050') as channel:
        stub = calc_pb2_grpc.CalculatorStub(channel)
        response = stub.Add(calc_pb2.AddRequest(digit1 = getinput(), digit2 = getinput()))
        print(response.total)

def getinput():
    digit = int(input("Enter digit to add :"))
    return digit



if __name__ == '__main__':
    run()
