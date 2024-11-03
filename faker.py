# python 3.11

import random
import psycopg2
import json

from psycopg2 import sql
from paho.mqtt import client as mqtt_client

# MQTT Connection Setup
broker = '10.158.66.30'
port = 1883
topic = ["the/topic", "sick/topicbro", "test/topic1", "test/topic2", "test/topic3", "apollo-air-1-87b074/data", "apollo-msr-2-cc0b5c/data"]
client_id = f'The-Big-Boss'
# Optional depending on Broker Security level
username = 'admin'
password = 'admin'

# DB Connection setup
conn = psycopg2.connect(host="10.158.66.30", dbname="postgres", user="admin", password="JXU73zooIoT1", port=32769)

# Establish Broker Connection
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    # Runs whenever the script receives an MQTT message
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
        # Turns the message into a dictionary and save its keys to the variable
        zeus = msg.topic.replace("/data", "")
        oner = json.loads(msg.payload)
        gumayusi = list(oner.keys())
        keria = []

        for i in gumayusi:
                keria.append(oner[i])

        # Establish Connection to the DB
        cur = conn.cursor()
        
        # Input message values to the DB

        # Convert the dictionary into a JSON file and store to the DB (issue is heavier data sent via tcp and more processing on the client side when there are multiple clients)
        cur.execute(f"INSERT INTO devices ({zeus.replace("-", "_")}) VALUES ('{json.dumps(oner, indent = 4)}')")
        # Convert the dictionary into a JSON file and store to the DB

        # Could be used for {device}_{id}:timestamp/{option1}/{option2}/{option3}
        # Where each dictionary key is the same name as the DB column, store the corresponding dictionary value to the key column
        cur.execute(f"INSERT INTO {zeus.replace("-", "_")} ({str(gumayusi).replace("'", "").replace("[", "").replace("]", "")}) VALUES ({str(keria).replace("[", "").replace("]", "")})")
        # Where each dictionary key is the same name as the DB column, store the corresponding dictionary value to the key column

        conn.commit();
        
        

    # Subscribed to all listed topics
    for i in topic:
        client.subscribe(i)

    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

