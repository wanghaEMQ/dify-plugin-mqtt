from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

import paho.mqtt.subscribe as subscribe

class MqttTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        topics = [tool_parameters["query"]]
        m = subscribe.simple(topics, hostname="broker.emqx.io", retained=False, msg_count=1)
        yield self.create_json_message({
            "result": m.payload
        })
