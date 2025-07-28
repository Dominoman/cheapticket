#!/bin/bash

cd "$(dirname "$0")"
set -ex

# tmp mappa létrehozása, ha nincs
if [ ! -d tmp ] ; then
  mkdir tmp
fi

# logos mappa létrehozása, ha nincs
if [ ! -d logos ] ; then
  mkdir logos
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
  alembic upgrade head
fi

#Replace old cron job
currentpath=$(pwd)
crontab -l | grep -v "cheapticket" > newcron
echo "0 */6 * * * $currentpath/bin/python3 $currentpath/main.py >> $currentpath/log.log 2>&1" >> newcron
crontab newcron
rm newcron

currentpath=$(pwd)
username=$(whoami)
groupname=$(id -gn)
servicename="cheapticket-web"

if [ ! -f $servicename.service ] ; then
  cp $servicename.service.template $servicename.service
  sed -i "s|%currentpath%|$currentpath|g; s|%username%|$username|g; s|%groupname%|$groupname|g" $servicename.service
fi

if [ ! -f /etc/systemd/system/$servicename.service ] ; then
  sudo ln -s "$currentpath/$servicename.service" /etc/systemd/system/$servicename.service
fi

# Restart gunicorn
sudo systemctl daemon-reload
sudo systemctl enable $servicename
sudo systemctl restart $servicename

deactivate
