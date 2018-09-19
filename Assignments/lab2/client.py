"""The Python implementation of the GRPC calc client."""

from __future__ import print_function

import grpc

import calc_pb2 as calc
import calc_pb2_grpc as rpc

def run():
    with grpc.insecure_channel('localhost:50050') as channel:
        stub = rpc.CalculatorStub(channel)
        response = stub.Add(calc.AddRequest(digit1 = getinput(), digit2 = getinput()))
        print("Total from digits given : %s" %response.total)

def getinput():
    digit = input("Enter digit to add :")
    return digit



if __name__ == '__main__':
    run()
