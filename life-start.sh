#!/bin/sh
pgrep -f life.py && echo life already running && exit 1
date >> life.log
python3.8 life.py >> life.log 2>&1 &
echo started new life!
