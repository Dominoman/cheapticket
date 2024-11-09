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
if [ ! -f .enc ] ; then
  cp .env.template .env
  echo "Default config created!"
fi

#Upgrade the database
if [ -f alembic.ini ] ; then
  alembic upgrade head
fi

#Replace old cron job
currentpath=$(pwd)
crontab -l | grep -v "cheapticket" > newcron
echo "0 */6 * * * $currentpath/bin/python3 $currentpath/main.py >> $currentpath/log.log 2>&1" >> newcron
crontab newcron
rm newcron

deactivate
