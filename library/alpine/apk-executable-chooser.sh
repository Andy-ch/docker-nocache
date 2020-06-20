#!/bin/sh
set -x
if apk --no-cache list
then
  mv /sbin/apk-nocache /sbin/apk
  rm /sbin/apk-delcache
else
  mv /sbin/apk-delcache /sbin/apk
  rm /sbin/apk-nocache
fi
rm /sbin/apk-executable-chooser.sh
