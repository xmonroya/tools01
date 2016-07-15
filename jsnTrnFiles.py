#!/usr/bin/python

#Este programa realiza la transferencia de archivo por ftp
# Adaptado para transferir el ultimo respaldo de QAD

from datetime import date, timedelta
from ftplib import FTP
import os
import glob


# Parametros

#Directorio en donde se encuentra los archivos a respaldar
DirOrig = "/root/QADDB/"
#Directorio remoto (ftp) en donde se debe dejar el respaldo
RemoteDir = "/QAD-PROD/BD/"

# FTP
username='bckserv'
password='janssen53'
ftpServer='10.1.1.214'

# Construye el filtro de archivos, basado en la fecha yyyymmdd
# en donde la fecha corresponde al dia de ayer
today = date.today()
oneday = timedelta(hours = 24)
yesterday = today - oneday

timespan = '%4d%02d%02d' % (yesterday.year, yesterday.month, yesterday.day)
filtro   = '*' + timespan + '*'


#Se optiene un listado de archivos que cumple con el filtro
archivos = []
#Lista el directorio especificado
for infile in glob.glob( os.path.join (DirOrig, filtro )):
        archivos.append(infile)

# Sube los archivos al servidor
ftp = FTP(ftpServer)
ftp.login(user=username, passwd=password)

# La siguiente linea debe ser 
ftp.cwd(RemoteDir)
ftp.mkd(timespan)
ftp.cwd(timespan)


for item in archivos:
        aux = os.path.split(item)
        print "Backup filename " + aux[1]
        ftp.storbinary('STOR ' +  aux[1] , open(item,  'rb'))

ftp.quit()

