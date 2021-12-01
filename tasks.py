from celery import Celery
from cpu_stress import stress
from scraper import get_data

celery = Celery('tasks',
                broker='redis://redis:6379',
                backend='redis://redis:6379')

@celery.task()
def crawl():

    get_data()

    stress()

    return {"message":"Done"}