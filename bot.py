import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2  "I don't need redis now"

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter

from tgbot.handlers.admin import register_admin, bot_notification
from tgbot.handlers.user import register_user
from tgbot.handlers.alert import register_alert

from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.middlewares.scheduler import SchedulerMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.handlers.alert import alert_check, ping
from tgbot.handlers.daily import daily_weather, daily_statistic, daily_news, daily_crypto, daily_tuya, weekly_donat

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config, scheduler):
    dp.setup_middleware(EnvironmentMiddleware(config=config))
    dp.setup_middleware(SchedulerMiddleware(scheduler))
    dp.setup_middleware(ThrottlingMiddleware(limit=5))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_alert(dp)


def set_scheduled_jobs(scheduler, bot):
    scheduler.add_job(alert_check, "interval", seconds=15, args=(bot,))
    scheduler.add_job(ping, "interval", minutes=5, args=(bot,))
    scheduler.add_job(daily_news, "interval", hours=6, args=(bot,))
    scheduler.add_job(daily_tuya, "cron", hour=7, minute=0, second=0, args=(bot,))
    scheduler.add_job(daily_weather, "cron", hour=8, minute=0, second=0, args=(bot,))
    scheduler.add_job(daily_statistic, "cron", hour=9, minute=0, second=0, args=(bot,))
    scheduler.add_job(daily_crypto, "cron", hour=10, minute=0, second=0, args=(bot,))
    scheduler.add_job(weekly_donat, "cron", day_of_week="fri", hour=15, minute=0, second=0, args=(bot,))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        encoding='utf-8')
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    scheduler = AsyncIOScheduler()  # create instance scheduler

    bot['config'] = config

    register_all_middlewares(dp, config, scheduler)
    register_all_filters(dp)
    register_all_handlers(dp)
    set_scheduled_jobs(scheduler, bot)
    # start
    try:
        await bot_notification(bot)
        scheduler.start()
        await bot.get_updates(offset=-1)
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped!")
