#!/bin/bash

#Realiza el respaldo de un directorio

#Uso: jsnBackupDir.sh Nombre Path_a_respaldar

if [ $# -eq 2 ]; then
	NAME=$1
	PATHOR=$2

	echo $NAME
	echo $PATHOR

	if [ -d $PATHOR ]; then
		TIMESTAMP=`date +"%Y%m%d%H%M"`

		#Esta es la ruta en donde se dejaran los respaldos
		PATHBACKUP=/root/BACKUP
		#PATHOR=/srv/docker/bind/bind/etc/

		FILE="$PATHBACKUP/$NAME$TIMESTAMP.tgz"

		tar czf $FILE $PATHOR
	else
		echo "ERROR: El directorio no existe $PATHOR"
		exit
	fi
else 
	exit
fi
