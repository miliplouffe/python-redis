from subprocess import check_output
import os
import time


def findProcessOrStart(name, directory):
    trouve = False
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    for pid in pids:
        try:
            if int(pid) > 1700:
                pid=pid

            resultat = (open(os.path.join('/proc', pid, 'cmdline'), 'rb').read())
            if name in str(resultat):
                trouve = True
        except IOError: # proc has already terminated
            continue

    if trouve == False:
        os.system(directory + ' &')



while True:
    findProcessOrStart("alarmeWebApp", "sudo /home/pi/go/./alarmeWebApp")
    time.sleep(2)

