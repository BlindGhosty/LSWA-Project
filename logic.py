import grpc

class CandidateServicer(debate_pb2_grpc.GenerateFollowers):

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  debate_pb2_grpc.add_CandidateServicer_to_server(
      CandidateServicer(), server)
  server.add_insecure_port('localhost:20426')
  server.start()
