import grpc
import backend_pb2
import backend_pb2_grpc

import mysql.connector
import datetime

db_conf = {
    "host" : "127.0.0.1", #needs to be changed when deployed
    "user" : "appserver",
    "password" : "foobarzoot",
    "database" : "scalica"
}
db_connection = mysql.connector.connect(**db_conf)

"""
Your email should include the following (in this order).
Final demo stuff:
1. Link (hostname/ip address) to your running demo. <- GCE instance
2. Any special credentials to use, if that applies. <- which user to log in as Yair - nobodyKnowsWhatIsRush
3. Special things you would like to to do / see in your online demo.
<- no way to check the rpc from a client side, + the batch job is always running.
???

Code submission stuff
4. git link
The code needs to include all the code you wrote, including script files and - if relevant - config files.
Update <- requirements.txt
You will get some bonus points for a well-documented README, in the top-level directory, that explains the code organization.
"""


import time
from concurrent import futures
ONE_DAY_IN_SECONDS = 60 * 60 * 24

class GenerateFollowersServicer(backend_pb2_grpc.GenerateFollowersServicer):
    def logic1(self, request, context):
        print "Request received for recommendation of " + str(request.MainUserId)
        single_recommend(request.MainUserId)
        return backend_pb2.Void()

def batch_wrapper():
    # batch job, runs between day
    while True:
        start_time = time.time()
        print "Starting batch job..."
        batch_recommend()
        print "Finished batch job!"
        diff_time = time.time() - start_time
        if (diff_time < ONE_DAY_IN_SECONDS):
            time.sleep(ONE_DAY_IN_SECONDS - diff_time)

def batch_recommend():
    cursor = db_connection.cursor(buffered=True, dictionary=True)
    initial_query = "SELECT id FROM auth_user"
    cursor.execute(initial_query)
    for id in cursor:
        single_recommend(id['id'])
    cursor.close()
    # TODO: If problem, restart immediately and like warn somebody?

def single_recommend(user_id):
    stale_query = "SELECT gen_date FROM micro_time_recommendation_given where user_id = %s"
    follow_query = "SELECT followee_id FROM micro_following WHERE follower_id = %s"
    add_recommendation = "INSERT INTO micro_recommendation VALUES (%s, %s, %s, %s)"
    insert_stale = "INSERT INTO micro_time_recommendation_given (user_id, gen_date) VALUES (%s, \'%s\')"
    update_stale = "UPDATE micro_time_recommendation_given SET gen_date = '%s' where user_id = %s"

    cursor = db_connection.cursor(buffered=True, dictionary=True)

    # Checks if user got a rec in the last 24 hours--either from batch or req
    cursor.execute(stale_query % user_id)
    date = cursor.fetchone()
    today = datetime.datetime.now()
    if date is None:
        cursor.execute(insert_stale % (user_id, today))
        db_connection.commit()
    else:
        if today - date['gen_date'] < datetime.timedelta(1):
            return
        cursor.execute(update_stale % (today, user_id))
        db_connection.commit()

    cursor.execute(follow_query % user_id)

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

    # Saves user's recommendations
    length = len(recommend_dict)
    for rec_id in recommend_dict:
        cursor = db_connection.cursor()
        cursor.execute("SELECT MAX(id) FROM micro_recommendation")
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        id += 1
        weight = (float) (recommend_dict[rec_id]) / length
        cursor.execute(add_recommendation % (id, user_id, rec_id, weight))
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
