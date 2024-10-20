from app.crawler.sse import run as sse_crawler
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()


async def start_scheduler():
    scheduler.add_job(sse_crawler, 'interval', seconds=180)
    scheduler.start()
