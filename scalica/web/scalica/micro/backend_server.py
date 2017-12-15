import grpc
import backend_pb2
import backend_pb2_grpc

import mysql.connector
import datetime

db_conf = {
    "host" : "127.0.0.1", #needs to be changed if deployed
    "user" : "appserver",
    "password" : "foobarzoot",
    "database" : "scalica"
}
db_connection = mysql.connector.connect(**db_conf)

import time
from concurrent import futures
ONE_DAY_IN_SECONDS = 60 * 60 * 24

channel = grpc.insecure_channel('localhost:20426') #also needs to be changed
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
    # batch job downtime in seconds
    while True:
        start_time = time.time()
        print start_time
        batch_recommend()
        diff_time = time.time() - start_time
        if (diff_time < ONE_DAY_IN_SECONDS):
            time.sleep(margin - diff_time)

def batch_recommend():
    cursor = db_connection.cursor(buffered=True, dictionary=True)
    initial_query = "SELECT id FROM auth_user"
    cursor.execute(initial_query)
    for id in cursor:
        single_recommend(id['id'])
    cursor.close()
    # If problem, restart immediately and like warn somebody

def single_recommend(user_id):
    stale_query = "SELECT gen_date FROM micro_time_recommendation_given where user_id = %s"
    follow_query = "SELECT followee_id FROM micro_following WHERE follower_id = %s"
    add_recommendation = "INSERT INTO micro_recommendation VALUES (%s, %s, %s)"
    insert_stale = "INSERT INTO micro_time_recommendation_given (user_id, gen_date) VALUES (%s, \'%s\')" # not sure this will work.
    update_stale = "UPDATE micro_time_recommendation_given SET gen_date = '%s' where user_id = %s"

    cursor = db_connection.cursor(buffered=True, dictionary=True)

    # Checks if user got a rec in the last 24 hours--either from batch or req
    cursor.execute(stale_query % user_id)
    date = cursor.fetchone()
    today = datetime.datetime.now()
    if date is None:
        print insert_stale % (user_id, today)
        cursor.execute(insert_stale % (user_id, today))
        db_connection.commit()
    else:
        if today - date['gen_date'] < datetime.timedelta(1):
            return
        cursor.execute(update_stale % (today, user_id))
        db_connection.commit()

    cursor.execute(follow_query % user_id)

    print user_id
    recommend_dict = {}
    followee_list = cursor.fetchall()
    for id in followee_list:
        cursor.execute(follow_query % id['followee_id'])
        ids = cursor.fetchall()
        for followee_id in ids:
            temp_id = followee_id['followee_id']
            if temp_id is user_id:
                continue
            if (temp_id in recommend_dict.keys()):
                recommend_dict[temp_id] += 1
            else:
                recommend_dict[temp_id] = 1
    print recommend_dict

    # Saves user's recommendations
    for rec_id in recommend_dict:
        cursor = db_connection.cursor()
        cursor.execute("SELECT MAX(id) FROM micro_recommendation")
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        id += 1
        print rec_id
        cursor.execute(add_recommendation % (id, user_id, rec_id))
        db_connection.commit()
       # puts in recommendations one at a time--should be a batch insert?
    cursor.close()


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

"Schedule"
    1. WE add these features...
    2. Then we need to update our deployment
    3. Send email to Yair
    4. pray.
"""
