#!/bin/bash

cd "$(dirname "$0")"
set -ex

# tmp mappa létrehozása, ha nincs
if [ ! -d tmp ] ; then
  mkdir tmp
fi

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

# Alapértelmezett config létrehozása
if [ ! -f .env ] ; then
  cp env.template .env
  echo "Default config created!"
fi

#Upgrade the database
if [ -f alembic.ini ] ; then
  alembic stamp head
  # alembic upgrade head
fi

#Replace old cron job
currentpath=$(pwd)
crontab -l | grep -v "cheapticket" > newcron
echo "0 */6 * * * $currentpath/bin/python3 $currentpath/main.py >> $currentpath/log.log 2>&1" >> newcron
crontab newcron
rm newcron

deactivate
