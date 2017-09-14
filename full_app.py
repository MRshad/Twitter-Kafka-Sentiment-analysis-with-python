import os
import time

if __name__=="__main__":
	# START KAFKA
	os.system('bin/kafka-server-start.sh config/server.properties')
	# WAIT 10 SEC FOR KAFKA TO START
	time.sleep(10)
	#START THE STREAM = producer
	os.system('$python app.py')
	#START consumers
	os.system('$python twitterStream.py')
