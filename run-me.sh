#!/bin/bash

cd "$(dirname "$0")"
set -ex

# Virtuális környezet létrehozása
if [ ! -f pyvenv.cfg ] ; then
  python -m venv .
fi

# Aktiváljuk a virtuális környezetet
source bin/activate

# Csomagok installálása
if [ -f requirements.txt ] ; then
  pip install -r requirements.txt
fi

# Create default config
if [ ! -f config.py ] ; then
  cp config.py.template config.py
  echo "Default config created!"
fi

#Upgrade the database
if [ -f alembic.ini ] ; then
  alembic upgrade head
fi

#Replace old cron job
crontab -l | grep -v "cheapticket" > newcron
echo "0 */6 * * * $(dirname "$0")/bin/python3 /home/laca/workspace/cheapticket/main.py >> /home/laca/workspace/cheapticket/log.log 2>&1" >> newcron
crontab newcron
rm newcron
deactivate
