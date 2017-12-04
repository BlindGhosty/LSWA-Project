import grpc
import backend_pb2
import backend_pb2_grpc

import time
from concurrent import futures
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

channel = grpc.insecure_channel('localhost:8000')
stub = consulation_pb2_grpc.GenerateFollowersStub(channel)

class GenerateFollowersServicer(backend_pb2_grpc.GenerateFollowersServicer):
    # Shouldn't request just send the usedId to gen recs for?
    def logic1(self, request, context):
        # TODO:
	
        ff_id = stub.logic2()
	
	
        return backend_pb2.RecommendationReply(Users=[request.MainUserId])

    def logic2(self, request, context):
        # TODO:
        return backend_pb2.RecommendationReply(Users=-1)

    def logic3(self, request, context):
        # TODO:
        return backend_pb2.RecommendationReply(Users=-1)

    def logic4(self, request, context):
        # TODO
        return backend_pb2.RecommendationReply(Users=-1)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) #Change the max???
  backend_pb2_grpc.add_GenerateFollowersServicer_to_server(
      GenerateFollowersServicer(), server)
  server.add_insecure_port('localhost:8000') # Needs to be changed
  print "Starting RPC server..."
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

serve()
