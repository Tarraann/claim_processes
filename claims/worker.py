import os
import time
from datetime import timedelta
from asgi_correlation_id.extensions.celery import load_correlation_ids
from celery import Celery
from celery.signals import after_setup_logger
from celery.schedules import crontab
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from claims.config.config import get_config

load_dotenv()
REDIS_URL = get_config("REDIS_URL")
DB_USER = get_config("DB_USER")
DB_PASS = get_config("DB_PASS")
DB_HOST = get_config("DB_HOST")
DB_NAME = get_config("DB_NAME")
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"


def connect_db():
    engine = create_engine(
        DB_URL,
        pool_size=20,  # Maximum number of database connections in the pool
        max_overflow=50,  # Maximum number of connections that can be created beyond the pool_size
        pool_timeout=30,  # Timeout value in seconds for acquiring a connection from the pool
        pool_recycle=1800,  # Recycle connections after this number of seconds (optional)
        pool_pre_ping=False,  # Enable connection health checks (optional)
    )
    connection = engine.connect()
    connection.close()
    return engine


celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)


def create_session():
    engine = connect_db()
    session = sessionmaker(bind=engine)()
    return session


celery_app.conf.beat_schedule = {}

load_correlation_ids()


@celery_app.task
def complex_task(n):
    """
    Simulates a long-running task by sleeping for a specified number of seconds.
    It also calculates the factorial of the number 'n' as an example of a CPU-bound operation.
    """
    # Simulate a time-consuming task
    time.sleep(30)  # Sleeps for 10 seconds

    # Calculate the factorial of 'n' (as an example of a computation)
    result = 1
    for i in range(1, n + 1):
        result *= i

    return {"status": "Task completed", "result": result}

