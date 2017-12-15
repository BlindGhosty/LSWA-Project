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
 * Password: josh_homme_innocent
