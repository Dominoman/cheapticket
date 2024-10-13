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
currentpath=$(pwd)
crontab -l | grep -v "cheapticket" > newcron
echo "0 */6 * * * $currentpath/bin/python3 $currentpath/main.py >> $currentpath/log.log 2>&1" >> newcron
crontab newcron
rm newcron

#streamlit
if [ ! -d .streamlit ] ; then
  mkdir .streamlit
fi

if [ ! -f .streamlit/config.toml ] ; then
  streamlit config show > .streamlit/config.toml
fi

if [ ! -f cheapticket-streamlit.service ] ; then
  cp cheapticket-streamlit.service.template cheapticket-streamlit.service
fi

sed -i "s|%currentpath%|$currentpath|g" cheapticket-streamlit.service

if [ ! -f /etc/systemd/system/cheapticket-streamlit.service ] ; then
  echo "zzz"
  # sudo ln -s "$currentpath/cheapticket-streamlit.service" /etc/systemd/system/cheapticket-streamlit.service
fi

deactivate
