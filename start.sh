#!/bin/sh
set -e

if [ ! -f .env ]; then
    echo "Configuration file '.env' not found. Copying the template..."
    cp .env.example .env
    chmod 600 .env
    echo "Edit '.env' (set TOKEN at minimum) and run this script again."
    exit 1
fi

if cmp --silent .env.example .env; then
    echo "Don't forget to change the values in '.env' (TOKEN is required)!"
    exit 1
fi

if [ ! -d venv ]; then
    echo "Creating virtualenv and installing dependencies..."
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
else
    . venv/bin/activate
fi

set -a
. ./.env
set +a

exec python -m app.bot
