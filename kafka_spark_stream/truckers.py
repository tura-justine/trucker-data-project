"""
To execute standalone: /usr/local/spark-2.0.2-bin-hadoop2.7/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 truckers.py

See: https://www.rittmanmead.com/blog/2017/01/getting-started-with-spark-streaming-with-python-and-kafka/
"""
import sys
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

#    Spark
from pyspark import SparkContext
#    Spark Streaming
from pyspark.streaming import StreamingContext
#    Kafka
from pyspark.streaming.kafka import KafkaUtils


#    Create Spark Context
sc = SparkContext(appName="TruckerStream_01")
sc.setLogLevel("WARN")

#    Create Streaming Context
ssc = StreamingContext(sc, 20)

#    Connect to Kafka
kafkaTruckersStream = KafkaUtils.createStream(ssc, 'sandbox.hortonworks.com:2181', 'truck-watchers', {'truckers':1})

#    Isolate the second tuple of each message consisting of the row in string form
lines = kafkaTruckersStream.map(lambda x: x[1])

#    Split the row up by commas to get a list of "columns" (as strings)
lineList = lines.map(lambda line: line.split(","))

#    Grab the trucker name list item "column" by index
truckers = lineList.map(lambda columns: columns[8])

#    Assign each trucker name instance a value of 1
truckersWithValOne = truckers.map(lambda trucker: (trucker,1))

#    Count instances of each trucker by name
truckersCount = truckersWithValOne.reduceByKey(lambda a,b: a+b)

#    Print results
truckersCount.pprint()


ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
