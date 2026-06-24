from openai import OpenAI
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContentBlock:
    type: str
    text: str = ""
    id: str = ""
    name: str = ""
    input: dict = field(default_factory=dict)


@dataclass
class OpenAIMessage:
    """Duck-typed wrapper to match Anthropic's Message interface."""
    content: list[ContentBlock]
    stop_reason: str


class OpenAIService:
    def __init__(self, model: str):
        self.client = OpenAI()
        self.model = model

    def add_user_message(self, messages: list, message):
        content = message if isinstance(message, (str, list)) else message
        if isinstance(content, list):
            # Tool result blocks from ToolManager — convert to OpenAI format
            tool_results = []
            for block in content:
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": block["tool_use_id"],
                    "content": block["content"],
                })
            messages.extend(tool_results)
        else:
            messages.append({"role": "user", "content": content})

    def add_assistant_message(self, messages: list, message):
        if isinstance(message, OpenAIMessage):
            tool_calls = [
                b for b in message.content if b.type == "tool_use"
            ]
            if tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": b.id,
                            "type": "function",
                            "function": {
                                "name": b.name,
                                "arguments": __import__("json").dumps(b.input),
                            },
                        }
                        for b in tool_calls
                    ],
                })
            else:
                text = self.text_from_message(message)
                messages.append({"role": "assistant", "content": text})
        else:
            messages.append({"role": "assistant", "content": str(message)})

    def text_from_message(self, message: OpenAIMessage) -> str:
        return "\n".join(
            b.text for b in message.content if b.type == "text"
        )

    def _convert_tools(self, tools: list) -> list:
        """Convert MCP tool format to OpenAI function format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "parameters": t.get("input_schema", {}),
                },
            }
            for t in tools
        ]

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ) -> OpenAIMessage:
        import json

        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})
        all_messages.extend(messages)

        params: dict[str, Any] = {
            "model": self.model,
            "messages": all_messages,
            "temperature": temperature,
            "max_tokens": 8000,
        }

        if stop_sequences:
            params["stop"] = stop_sequences

        openai_tools = None
        if tools:
            openai_tools = self._convert_tools(tools)
            params["tools"] = openai_tools
            params["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**params)
        choice = response.choices[0]
        finish_reason = choice.finish_reason

        content_blocks: list[ContentBlock] = []

        if choice.message.content:
            content_blocks.append(
                ContentBlock(type="text", text=choice.message.content)
            )

        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                content_blocks.append(
                    ContentBlock(
                        type="tool_use",
                        id=tc.id,
                        name=tc.function.name,
                        input=json.loads(tc.function.arguments),
                    )
                )

        stop_reason = "tool_use" if finish_reason == "tool_calls" else "end_turn"
        return OpenAIMessage(content=content_blocks, stop_reason=stop_reason)
