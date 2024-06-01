#!/bin/bash

# Start the app
exec celery -A claims.worker beat --loglevel=info