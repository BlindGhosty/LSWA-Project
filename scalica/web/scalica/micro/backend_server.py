import grpc
import backend_pb2
import backend_pb2_grpc

import mysql.connector

db_conf = {
    "host" : "127.0.0.1",
    "user" : "appserver",
    "password" : "foobarzoot",
    "database" : "scalica"
}
db_connection = mysql.connector.connect(**db_conf)

import time
from concurrent import futures
ONE_DAY_IN_SECONDS = 60 * 60 * 24

channel = grpc.insecure_channel('localhost:20426')
stub = backend_pb2_grpc.GenerateFollowersStub(channel)

class GenerateFollowersServicer(backend_pb2_grpc.GenerateFollowersServicer):
    # Shouldn't request just send the usedId to gen recs for?
    def logic1(self, request, context):
        single_recommend(request.SubscriptionsId)

        # NO LONGER NEED TO RETURN ANYTHING
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

def batch_wrapper():
    batch_recommend()
    """
    margin = 600000000 # batch job downtime in seconds
    while True:
        start_time = time.time()
        # print "starting batch job"
        batch_recommend()
        end_time = time.time()
        diff_time = end_time - start_time
        if (diff_time < margin):
            time.sleep(diff_time)
    """

def batch_recommend():
    cursor = db_connection.cursor(buffered=True, dictionary=True)
    initial_query = "SELECT id FROM auth_user"
    cursor.execute(initial_query)
    # cursor now holds all the relevant ids

    for id in cursor:
        # check if the id is done first before calling this!
        single_recommend(id['id'])
    cursor.close()
    # If problem, restart immediately and like warn somebod

    """
    theory, you should mark who's been replaced...
    #! At any time, a user could just be like recommended already so skip him
    """

def single_recommend(user_id):
    print "Start"
    print user_id
    follow_query = "SELECT followee_id FROM micro_following WHERE follower_id = %s"
    add_recommendation = "INSERT INTO micro_recommendation VALUES (%s, %s, %s)"

    cursor = db_connection.cursor(buffered=True, dictionary=True)
    cursor.execute(follow_query % user_id)
    # cursor now holds list of users that I follow

    recommend_dict = {}
    for id in cursor:
        temp_cursor = db_connection.cursor(buffered=True)
        temp_cursor.execute(follow_query % user_id)
        temp_ids = temp_cursor.fetchall()
        print temp_ids
        for ids in temp_ids:
            temp_id = ids[0]
            if (temp_id in recommend_dict.keys()):
                print "found"
                # recommend_dict[temp_id] = recommend_dict[temp_id] + 1
            else:
                recommend_dict[temp_id] = 1
        temp_cursor.close()
    print recommend_dict
    # print recommend_dict
    #

    # for rec_id in recommend_set:
    #     cursor = db_connection.cursor()
    #     cursor.execute("SELECT MAX(id) FROM micro_recommendation")
    #     id = cursor.fetchone()[0]
    #     if (id == None):
    #         id = 0
    #     id += 1
    #     cursor.execute(add_recommendation % (id, user_id, rec_id[0]))
    #     db_connection.commit()
    #    puts in recommendations one at a time--should be a batch insert?
    # cursor.close()


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) #Change the max???
  backend_pb2_grpc.add_GenerateFollowersServicer_to_server(
      GenerateFollowersServicer(), server)
  server.add_insecure_port('0.0.0.0:20426') # Needs to be changed
  print "Starting RPC server..."
  server.start()
  try:
      batch_wrapper()
  except KeyboardInterrupt:
      db_connection.close()
      server.stop(0)

serve()

"""
1. Populate
    SIMPLE WITH 3
    then 7
    Simple, just create a test case for 100 users, who all follow one another randomly
    Some way to visualize this???
    Users with 5-10 followers of regular values...
    Simple, do "Left vs Right bubbles"
        (And then we have the libertarian have no friends)
        (And we love pizza)
2. RPC logic (use actual algorithms)
    logic1 <-- this will be our only call!
    USE MAP/REDUCE plz
3. Stale Data Checking / Test RPC on log-in... (look at cursor stuff)
    This is what concerns me...
    (Dumb) ideas:
        1. We add the the USER model
            How this is done, idk
        2. We add to the Follower model
            (becuase we don't care)
        3. We store it the priority queue inside our server...
4. Test RPC on log-in
    Look for login

"Schedule"
    1. WE add these features...
    2. Then we need to update our deployment
    3. Send email to Yair
    4. pray.

"""
