from subprocess import Popen, PIPE, run
import subprocess
import sys
import time

processName =["interfacePythonArduino","systemeArrosage","systemeAlarme"]
#  processName =["systemeAlarme"]
while True:
    process = Popen(['ps', '-eo' ,'pid,args'], stdout=PIPE, stderr=PIPE)
    stdout, notused = process.communicate()

    for nom in processName:
        trouve=False
        for line in stdout.splitlines():
            print (" process nom ", line.decode())
            if nom+'.py' in line.decode():
                trouve=True
                print (" -------------------------------   trouve  ------------------------ ", nom)
                exit

        if trouve==False:
            p = subprocess.Popen('/home/pi/python/' + nom+'.sh')
            time.sleep(1)
            print ("---------------------------------------------------------------------------repartir le process ", nom)
            trouve=False

    time.sleep(30)
