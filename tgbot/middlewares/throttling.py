import asyncio
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.utils.exceptions import Throttled
from typing import Dict

import random


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 1, key_prefix: str = "antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: Dict):
        handler = current_handler.get()
        dispatcher = self.manager.dispatcher
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")

            try:
                await dispatcher.throttle(key, rate=limit)
            except Throttled as t:
                await self.message_throttled(message, t)
                raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        delta = throttled.rate - throttled.delta
        answers = [f"🫷 А все! \n\nТепер очікуй <b>{delta:.1f}</b> 🕕 секунд.",
                   f"🙅‍♂️Не поспішай! Тепер встановлено ліміти.\n\nСпробуй через <b>{delta:.1f}</b> 🕕 секунд.",
                   f"🙈Частіше тицаєш, рідше отримуєш.\n\nВарто було спробувати через <b>{delta:.1f}</b> 🕕 секунд."]
        answer = random.choice(answers)
        await message.reply(answer)

    @staticmethod
    def rate_limit(limit: int, key: str = None):
        def decorator(func):
            setattr(func, "throttling_rate_limit", limit)
            if key:
                setattr(func, "throttling_key", key)
            return func
        return decorator