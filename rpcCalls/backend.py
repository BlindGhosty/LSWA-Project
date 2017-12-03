import grpc

class GenerateFollowersServicer(backend_pb2_grpc.GenerateFollowersServicer):
    def logic1(self, request, context):
        # TODO:
        return backend_pb2.RecommendationReply(Users=)

    def logic2(self, request, context):
        # TODO:
        return backend_pb2.RecommendationReply(Users=)

    def logic3(self, request, context):
        # TODO:
        return backend_pb2.RecommendationReply(Users=)

    def logic4(self, request, context):
        # TODO
        return backend_pb2.RecommendationReply(Users=)
    
def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) #Change the max???
  debate_pb2_grpc.add_GenerateFollowersServicer_to_server(
      GenerateFollowersServicer(), server)
  server.add_insecure_port('localhost:20426') # Needs to be changed
  server.start()
