import logging
from json import dumps, loads
from random import random

import matplotlib.pyplot as plt
import psycopg2
import seaborn as sns
from django.http import HttpResponse
from django.shortcuts import render
from kafka import KafkaConsumer, KafkaProducer

from .utils import plot_graph

# Create your views here.

# creating the kafka produnce to push the data into kafka stream

logger = logging.getLogger(__name__)



def genarate_data(request):
    poc_producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=lambda x: dumps(x).encode("utf-8"),
    )
    # genarate random power consumption values between 0.1 to 1.0
    while True:
        power_consumption_data = {"consumption_value": f"{random():.2f}"}
        poc_producer.send("poc_power_consumption", value=power_consumption_data)
        return HttpResponse("Data inserted into kafka stream")


def get_db_connection():
    conn = psycopg2.connect(
        host="postgres",
        database="power_stats",
        user="debug",
        password="debug",
        port="5432",
    )
    return conn


def store_data(request):
    consumption_value = KafkaConsumer(  
    'poc_power_consumption',  
    bootstrap_servers = ['localhost:9092'],  
    auto_offset_reset = 'earliest',  
    enable_auto_commit = True,  
    group_id = 'poc-group',  
    value_deserializer = lambda x:loads(x.decode('utf-8'))  
    )

    poc_table = "CREATE TABLE IF NOT EXISTS power_consumption (time TIMESTAMPTZ NOT NULL, consumption_value DOUBLE PRECISION);"
    pc_hypertable = "SELECT create_hypertable('power_consumption', 'time');"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(poc_table)
    cursor.execute(pc_hypertable)
    conn.commit()

    for consumption in consumption_value:
        try:
            value = consumption.value["consumption_value"]
            cursor.execute(
                f"INSERT INTO power_consumption (time, consumption_value) VALUES (NOW(), {value});"
            )
            conn.commit()

        except Exception as e:
            logger.info(f"database error - {e}")
    query = "SELECT time_bucket('5 minutes', time) AS five_min, max(consumption_value) FROM power_consumption;"
    cursor.execute(query)
    conn.close()


def plot_graph(request):
    
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT time_bucket('5 minutes', time) AS five_min, avg(consumption_value) FROM power_consumption GROUP BY five_min ORDER BY five_min DESC;"
    cursor.execute(query)
    query_set = cursor.fetchall()
    x = []
    y = []
    for i in range(len(query_set)):
        x.append(query_set[i][0])
        y.append(query_set[i][1])
    # ax = sns.stripplot(x=x, y=y)
    # ax.set(xlabel ='time', ylabel ='power consumption')
    # plt.title('power')
    # plt.savefig('./power_stats/power_stats/static/images/readings.png')
    chart = plot_graph(x, y)
    return render(request, )
    
    buffer = BytesIO()
    
    