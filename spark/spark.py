from pyspark.sql import SparkSession
from pyspark.sql.functions import col  # Import col function
import os

def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("HelloWorld") \
        .master("spark://localhost:7077") \
        .getOrCreate()

    # Example 1: Word Count (Classic Big Data Example)
    text_rdd = spark.sparkContext.parallelize([
        "Spark is amazing",
        "Big Data is powerful",
        "Apache Spark is fast",
        "Big Data and AI are the future"
    ])

    word_counts = (
        text_rdd.flatMap(lambda line: line.split(" "))
        .map(lambda word: (word.lower(), 1))
        .reduceByKey(lambda a, b: a + b)
    )

    print("\n--- Word Count Example ---")
    for word, count in word_counts.collect():
        print(f"{word}: {count}")

    # Example 2: Filtering Even Numbers
    numbers_rdd = spark.sparkContext.parallelize(range(1, 21))
    even_numbers_rdd = numbers_rdd.filter(lambda x: x % 2 == 0)

    print("\n--- Even Numbers Example ---")
    print(f"Even numbers: {even_numbers_rdd.collect()}")

    # Example 3: Using DataFrames
    data = [
        (1, "Alice", 4000),
        (2, "Bob", 5000),
        (3, "Charlie", 6000),
        (4, "David", 7000),
    ]

    df = spark.createDataFrame(data, ["id", "name", "salary"])

    print("\n--- DataFrame Example (Salary > 5000) ---")
    df_filtered = df.filter(col("salary") > 5000)
    df_filtered.show()

    # Stop SparkSession
    spark.stop()

if __name__ == "__main__":
    main()