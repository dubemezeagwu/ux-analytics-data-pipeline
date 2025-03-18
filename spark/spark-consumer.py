import sys
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

if __name__ == "__main__":
    # Checking validity of Spark submission command
    if len(sys.argv) != 4:
        print("Wrong number of args.", file=sys.stderr)
        sys.exit(-1)

    # Initializing Spark session
    spark = SparkSession \
        .builder \
        .appName("MySparkSession") \
        .getOrCreate()

    # Setting parameters for the Spark session to read from Kafka
    bootstrapServers = sys.argv[1]  # Kafka bootstrap servers (e.g., localhost:9092)
    subscribeType = sys.argv[2]  # The type of subscription: 'subscribe' or 'subscribePattern'
    topics = sys.argv[3]  # Kafka topics (e.g., "my_topic")

    # Streaming data from Kafka topic as a dataframe
    lines = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrapServers) \
        .option(subscribeType, topics) \
        .load()

    # Expression that reads in raw data from dataframe as a string
    # and names the column "json"
    lines = lines \
        .selectExpr("CAST(value AS STRING) as json")

    # Writing dataframe to console in append mode
    query = lines \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    # Terminate the stream on abort
    query.awaitTermination()
