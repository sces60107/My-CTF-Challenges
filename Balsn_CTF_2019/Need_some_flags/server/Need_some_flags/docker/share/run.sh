#!/bin/bash
exec 2>/dev/null
python2.7 -u /home/Need_some_flags/pow.py
if [ $? != 57 ] ; then
  exit
fi
tempdir=$(mktemp -d)
cp -r /home/Need_some_flags/server/ $tempdir
cd $tempdir/server
timeout 60 python2.7 -u server.py
rm -rf $tempdir
