from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

import threading
import queue
from enum import Enum

import paho.mqtt.client as mqtt

class mqtttype(Enum):
    CONNECTED = 1
    DISCONNECTED = 2
    SUBACK = 3
    PUBLISH = 4

class mqttmsg:
    def __init__(self, mtype, mtopic, mpld):
        self.type = mtype
        self.topic = mtopic
        self.payload = mpld

q = queue.Queue()

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
        q.put(mqttmsg(mqtttype.DISCONNECTED, None, None))
    else:
        print(f"Connected!")
        q.put(mqttmsg(mqtttype.CONNECTED, None, None))

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
        q.put(mqttmsg(mqtttype.DISCONNECTED, None, None))
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")
        q.put(mqttmsg(mqtttype.SUBACK, None, None))

def on_message(client, userdata, message):
    q.put(mqttmsg(mqtttype.PUBLISH, message.topic, message.payload))

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

def mqtt_loop():
    mqttc.loop_forever()
mqtt_loop_thr = threading.Thread(target=mqtt_loop)

is_first_run = True

class MqttTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        broker = tool_parameters["broker"]
        port = tool_parameters["port"]
        topic = tool_parameters["topic"]
        print(f"b{broker} p{port} t{topic}")

        global is_first_run
        if is_first_run == True:
            mqttc.connect(broker, port)
            mqtt_loop_thr.start()
            is_first_run = False

        newmsg = q.get()
        result = ""
        if newmsg.type == mqtttype.DISCONNECTED:
            result = "Disconnected"
        elif newmsg.type == mqtttype.CONNECTED:
            mqttc.subscribe(topic)
            result = "Connected"
        elif newmsg.type == mqtttype.SUBACK:
            result = "Subscribed"
        elif newmsg.type == mqtttype.PUBLISH:
            result = newmsg.payload

        yield self.create_text_message(result)
