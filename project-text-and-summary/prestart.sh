#! /usr/bin/env bash

# Let the DB start
python ./start_db_session.py

# Run migrations
alembic upgrade head
