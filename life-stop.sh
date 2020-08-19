#!/bin/sh
pid=`pgrep -f life.py | awk '{print $1}'`
pgrep -f life.py && echo  running && kill -9 $pid && echo life was stopped

