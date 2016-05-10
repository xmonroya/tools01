#!/bin/sh

#Genera un respaldo de las bases de datos dejando como timestamp
PATH=$PATH:/usr/bin/

BACKUPDIR="/root/BACKUP"
USER=root
PASS="dat208."

#Genera timestamp
TIMESTAMP=`date +"%Y%m%d%H%M"`
FILE="$BACKUPDIR/MySQL_backup_$TIMESTAMP.sql"

mysqldump -u $USER --password=$PASS -R -A > $FILE
gzip $FILE
