from __future__ import annotations

from typing import AsyncIterable

from fastapi_poe import PoeBot, run
from fastapi_poe.client import MetaMessage, stream_request
from fastapi_poe.types import QueryRequest
from sse_starlette.sse import ServerSentEvent

class ClaudeBot(PoeBot):
    async def get_response(self, query: QueryRequest) -> AsyncIterable[ServerSentEvent]:
        bot = "claude-instant"
        yield self.text_event(f"\n\n**{bot.title()}** says:\n")
        async for msg in stream_request(query, bot, query.api_key):
            if isinstance(msg, MetaMessage):
                continue
            elif msg.is_suggested_reply:
                yield self.suggested_reply_event(msg.text)
            elif msg.is_replace_response:
                yield self.replace_response_event(msg.text)
            else:
                yield self.text_event(msg.text)

if __name__ == "__main__":
    run(ClaudeBot(), api_key="K5uv2GVUaG97ta9jCANn5tHqDdQb1M2F")

