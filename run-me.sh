#!/bin/bash

cd "$(dirname "$0")"
set -ex

# Virtuális környezet létrehozása
if [ ! -x .venv ] ; then
  python -m venv .venv
fi

# Aktiváljuk a virtuális környezetet
source .venv/bin/activate

# Csomagok installálása
if [ -f requirements.txt ] ; then
  pip install -r requirements.txt
fi

if [ ! -f config.py ] ; then
  cp config.py.template config.py
  echo "Default config created!"
fi

if [ -f alembic.ini ] ; then
  alembic upgrade head
fi

deactivate