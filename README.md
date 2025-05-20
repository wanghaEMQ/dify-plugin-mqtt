## MQTT-Tools

**Author:** wangha

**Version:** 0.0.1

**Type:** tool

### Description

The MQTT-Tools provides `SUB` and `PUB` commands which help you to communicate with a MQTT Broker.

`SUB`command: Create a MQTT client and subscribe to a topic. This MQTT-Tools node will end when receive a message from MQTT Broker.

`PUB`command: Create a MQTT client and publish a message to a topic. This MQTT-Tools node will end when publishing is done.

### How to start

Input following parameters.

`type`: sub or pub

`broker`: The address of your broker. for example: broker.emqx.io

`port`: The port of your broker. for example: 1883

`topic`: The topic you wanna to publish or subscribe to.

`payload`: This parameter will be ignored when type is sub.

When all parameters are set.

If the `type` is sub. This node will wait for a message from `topic` from the broker`broker:port`. This node will end when the message arrived.

If the `type` is pub. This node will publish a message to `topic` of broker`broker:port`. This node will end when the message was sent.

If the broker`broker:port` is unavailable. This node will end when timeout and return a error.
