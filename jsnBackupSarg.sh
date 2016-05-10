#!/bin/bash
# Este programa realiza un respaldo de los archivos SARG

#Definicion de las rutas de origen y destino del respaldo
BASERUTA=/var/www/html/sarg
BASEDEST=/root/BACKUP/sarg

#Archivo temporal
tmpfile=/tmp/jsnBackupSarg

SEARCH=". -maxdepth 1 -mindepth 1 -ctime +90 -type d -print0"
#SEARCH=". -maxdepth 1 -mindepth 1 -type d -print0"

function backup {

        RUTA="$BASERUTA/$1/"
        DEST="$BASEDEST/$1/"

        echo "Iniciando Respaldo de SARG $1..."
        echo $RUTA
        echo $DEST

        #Se cambia al directorio desde donde se realizara el respaldo
        cd $RUTA

        #Deja los directorios resultantes en un archivo temporal
        LISTFILES=()
        find $SEARCH > $tmpfile

        #Coloca el archivo con el listado en un array
        while IFS= read -r -d $'\0'; do
                        LISTFILES+=("$REPLY")
        done < $tmpfile

        echo "Total de carpetas a respaldar: ${#LISTFILES[@]}"

        #El siguiente codigo lista los archivos del array
        #for (( i=0; i<=${#LISTFILES[@]}; i++)); do
        #       echo ${LISTFILES[$i]}
        #done

        # Aqui comprimen los archivos y se mueve a su destino final
        for FILE in ${LISTFILES[@]}; do
                echo "-- $FILE --"
                if [ $FILE != "./images" ]; then
                   echo "Empacando carpeta $FILE..."
                   tar cf - $FILE | pv -L 1m > $FILE.tar
                   echo "comprimiendo..."
                   nice -n 10 gzip $FILE.tar
                   mv $FILE.tar.gz $DEST
                   mv $FILE /root/BACKUP/tmp
                   echo "Esperando 5 minutos..."
                   sleep 300
                fi
        done
}

# Programa principal

backup "monthly"
backup "weekly"
backup "daily"

#echo "$SEARCH"

