# Team 13: Follower Recommendation Service

### Project Goals:
 * Follower reccomendation service implemented through offline batchjob
 * Users can accesss reccomendations once they log in via rpc call
 * Every day, the batch job re-calculates "stale reccomendations"

### Calculating Potential Followers:
 * "Bring your friends"
 	* Simple, just recommend those who my friends follow the most
 	* We weight the most popular people my friends follow higher
 * "Follow for follow"
 	* Find those who follow us, but we don't follow back
 * "Bring your friends friends"
 	* Find the people who your friends followers follow the most

### Code Organization:
* models.py
 * time_recommendation_given
 * Recommendation
* populate_test_X.py
 * tests that populate our server (we only use one for the final demo)
* back_end_servery.py
 * where we process reccomendations

### Logging On:
 * Username: Yair
 * Password: josh_homme_INNOCENT!

### Extra stuff:
 * We had problems with cloud deployment--suspect that CloudSQL is the culprit.
 * We had to remove the indirect chain logic and the weighting of our algorithms.
 * In addition, we couldn't get our database cleaning procedure to run properly. That would have fixed the duplication problem.

### Running on Local:
 * Running the ./liveDemo.sh script clears and repopulates the local sql database with sample data to test the rpc server.
 * To see the details of the sample data, look under the populate_test_$(#).py scripts
 * Then, upon running the backend server under micro/rpcCalls with "python backend_server.py", our batch job is initiated.
 * You could see the results either directly in the SQL table or on the scalica website under our recommendation page.
 * Running locally works fully as opposed to the state of our cloud deployment.
