"""The Python implementation of the GRPC calc server."""

from concurrent import futures
import time
import sys

import grpc

import calc_pb2 as calc
import calc_pb2_grpc as rpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Calculator(rpc.CalculatorServicer):

    def Add(self, request, context):
        print(request.digit1)
        return calc.AddTotal(total = request.digit1 + request.digit2)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  rpc.add_CalculatorServicer_to_server(Calculator(), server)
  server.add_insecure_port('[::]:50050')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
