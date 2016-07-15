#!/usr/bin/python

# jsnTrnFiles.py -o RemoteDir -i LocalDir fYesterday
#Este programa realiza la transferencia de archivos por ftp
#Usa como filtro el timestamp generado en el archivo
# Recibe como argumentos el directorio en donde se encuentran los archivos
# El directorio destino
# Flag para determinar si usa la fecha de ayer o la de hoy

from datetime import date, timedelta
from ftplib import FTP
import sys, os, getopt
import glob

#Define unos parametros globales
fYesterday = 0
#Directorio en donde se encuentra los archivos a respaldar
LocalDir = ""
#Directorio remoto (ftp) en donde se debe dejar el respaldo
RemoteDir = ""

def main(argv):
	# Manejo de los parametros de entrada
	global LocalDir, RemoteDir, fYesterday

	try:
		opts, args = getopt.getopt(argv, "hi:o:y")
	except getopt.GetopError:
		print "jsnTrnFiles.py -i <LocalDir> -o <RemoteDir>"
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
        		print "jsnTrnFiles.py -i <LocalDir> -o <RemoteDir>"
		        sys.exit(2)
 		elif opt == "-i":
			LocalDir = arg
		elif opt == "-o":
			RemoteDir = arg
		elif opt == "-y":
			fYesterday = 1
	if LocalDir == "" or RemoteDir == "":
                print "jsnTrnFiles.py -i <LocalDir> -o <RemoteDir>"
                sys.exit(2)




if __name__ == "__main__":

	main(sys.argv[1:])

	# FTP
	username='bckserv'
	password='janssen53'
	ftpServer='10.1.1.214'

	# Construye el filtro de archivos, basado en la fecha yyyymmdd
	# en donde la fecha corresponde al dia de ayer
	today = date.today()

	if fYesterday == 1:
		oneday = timedelta(hours = 24)
		yesterday = today - oneday
		day = yesterday
	else:
		day = today
	
	timespan = '%4d%02d%02d' % (day.year, day.month, day.day)
	filtro   = '*' + timespan + '*'


	#Se obtiene un listado de archivos que cumple con el filtro
	archivos = []
	#Lista el directorio especificado
	for infile in glob.glob( os.path.join (LocalDir, filtro )):
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

