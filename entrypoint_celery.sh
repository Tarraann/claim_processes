#!/bin/bash

# Start the app
exec celery -A claims.worker worker --loglevel=info --concurrency=1
