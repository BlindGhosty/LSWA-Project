import grpc
import backend_pb2
import backend_pb2_grpc

import time
from concurrent import futures
ONE_DAY_IN_SECONDS = 60 * 60 * 24

channel = grpc.insecure_channel('localhost:20426')
stub = backend_pb2_grpc.GenerateFollowersStub(channel)

class GenerateFollowersServicer(backend_pb2_grpc.GenerateFollowersServicer):
    # Shouldn't request just send the usedId to gen recs for?
    def logic1(self, request, context):
        # TODO:

        #pass in the first followee of follower
	      #check if
        """
        ff_ret = []
        for i in request.PossFollowersId:
          if i not in request.SubscriptionsId and i != request.MainUserId:
            ff_ret.append(i)
        """
        toReturn = list(set(request.SubscriptionsId))
        return backend_pb2.RecommendationReply(Users=toReturn)

    def logic2(self, request, context):
        # TODO:
        return backend_pb2.RecommendationReply(Users=ff_list)

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
  server.add_insecure_port('localhost:20426') # Needs to be changed
  print "Starting RPC server..."
  server.start()
  try:
    while True:
      time.sleep(ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

serve()
