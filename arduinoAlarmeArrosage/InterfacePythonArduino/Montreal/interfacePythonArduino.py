#UART communication on Raspberry Pi using Pyhton
#//http://www.electronicwings.com
#//'''
import sys, os

import serial
from dataclasses import dataclass
from time import sleep
import threading
from datetime import datetime, timedelta
from enum import Enum
sys.path.append("/home/pi/.local/lib/python3.9/site-packages/")
import jsonpickle
from json import JSONEncoder
import pickle
import RedisInOut as redisInOut


class const:
    format = "02-01-2006 15:04:05"
   
    HIGH                           = 1
    LOW                            = 0
    heureTestMatin                 = 7
    nombreCourrielQuotidien        = 5

    clefLog                     = "alarmeLog"


DateHeureCourante =datetime
NomEquipement =str

CourrielValeur=""
courriel7Heures=bool

NoZone=0
Statut=0
Action=0
Requete=""


@dataclass
class DETECTEUR:
    MouvChambrePrincipale: int = 0
    MouvChambreSecondaire: int = 0
    MouvBureau: int = 0
    MouvSalon: int = 0
    MouvSalleBillard: int = 0
    MouvSalleVernis: int = 0
    InterPorteAvant: int = 0
    InterPorteArriere: int = 0
    InterPorteSousSol: int = 0
    DectEauAtelier: int = 0
    DectEauSalleLavage: int = 0
    DectEauPluie: int = 0
    DectFumeeSalleBillard: int = 0
    DectFumeeAtelier: int = 0
    DectArrosageZone1: int = 0
    DectArrosageZone2: int = 0
    DectArrosageZone3: int = 0
    DectArrosageZone4: int = 0

def sendMail(SUBJECT,TEXT):
    global CourrielValeur
    import smtplib

    gmail_user = 'miliplouffe@gmail.com'
    gmail_password = 'pifewpnxrytkljxv'

    sent_from = gmail_user
    to = ['miliplouffe@outlook.com']
    subject = SUBJECT
    body = TEXT


    email_text = """\
    From: %s
    To: %s
    Subject: %s

    #%s
    #""" % (sent_from, ", ".join(to), subject, body)

    print ("Courriel Valeur ", CourrielValeur)
    try:
        if CourrielValeur=="courrielActif":
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            print ('Email sent!')
    except:
        print ('Something went wrong...')


def detecteurDataStructure(dectArduino):
    detecteurs = DETECTEUR()

    detecteurs.MouvChambrePrincipale=dectArduino["MouvChambrePrincipale"]
    detecteurs.MouvChambreSecondaire=dectArduino["MouvChambreSecondaire"]
    detecteurs.MouvBureau=dectArduino["MouvBureau"]
    detecteurs.MouvSalon=dectArduino["MouvSalon"]
    detecteurs.MouvSalleBillard=dectArduino["MouvSalleBillard"]
    detecteurs.MouvSalleVernis=dectArduino["MouvSalleVernis"]
    detecteurs.InterPorteAvant=dectArduino["InterPorteAvant"]
    detecteurs.InterPorteArriere=dectArduino["InterPorteArriere"]
    detecteurs.InterPorteSousSol=dectArduino["InterPorteSousSol"]
    detecteurs.DectEauAtelier=dectArduino["DectEauAtelier"]
    detecteurs.DectEauSalleLavage=dectArduino["DectEauSalleLavage"]
    detecteurs.DectEauPluie=dectArduino["DectEauPluie"]
    detecteurs.DectFumeeSalleBillard=dectArduino["DectFumeeSalleBillard"]
    detecteurs.DectFumeeAtelier=dectArduino["DectFumeeAtelier"]
    detecteurs.DectArrosageZone1=dectArduino["DectArrosageZone1"]
    detecteurs.DectArrosageZone2=dectArduino["DectArrosageZone2"]
    detecteurs.DectArrosageZone3=dectArduino["DectArrosageZone3"]
    detecteurs.DectArrosageZone4=dectArduino["DectArrosageZone4"]

    return detecteurs



def sauvegardeMessageActivites(DataLOG):
    print('en construction')

# sendMail("Systeme alarme Montreal","Le systeme d alarme a redemarre")


# ser = serial.Serial("COM4", 115200, timeout=2)
ser = serial.Serial("/dev/ttyACM0", 115200, timeout=2)    #Open port with baud rate
Detecteurs=""

def sendDetecteursAlarmeArrosage():
    global Detecteurs
    while True:
        redisInOut.publishInterfaceArduinoDetecteur(Detecteurs)
        sleep(.2)

if __name__ == '__main__':

    redisInOut.StartInterfaceArduinoRequete()
    courriel7Heures = False

    t1 = threading.Thread(target=sendDetecteursAlarmeArrosage)
    t1.start()

    while True:
        Requete=redisInOut.getRequeteInterface()

        if ser.is_open==True:
            # print (" ser waiting ", ser.inWaiting())
            while ser.inWaiting()==0: pass
            if  ser.inWaiting()>0: 
                received_data=ser.readline()
                ser.flushInput() 
            else:
                print (" long 'a recevoir")
            sleep(0.5)

        try:
            detecteursRec = jsonpickle.decode(received_data)
            Detecteurs = detecteurDataStructure(detecteursRec)

            # Equipement, GicleursStatut = decodeDataDetecteur(detecteurs, **Equipement)
            # sendSystemeAlarmeDataEquipement(SendRec["AlarmeSystemeDataEquipement"].Ip, SendRec["AlarmeSystemeDataEquipement"].Port, Detecteurs )
            # sendSystemeAlarmeDataEquipement(SendRec["ArrosageSystemeDataGicleurs"].Ip, SendRec["ArrosageSystemeDataGicleurs"].Port, Detecteurs )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)


        if Requete == "Gicleur_1_ON":
            ser.write(b'Gicleur_1_ON')
            print ("commande : ", "Gicleur_1_ON")
            sauvegardeMessageActivites("Set gicleur arrosage Ouvert")
            redisInOut.RequeteInterface=""
            Requete=""
            sleep(1)
        elif Requete == "Gicleur_1_OFF":
            ser.write(b'Gicleur_1_OFF')
            sauvegardeMessageActivites("Set gicleur près pour arrosage")
            redisInOut.RequeteInterface=""
            Requete=""
            sleep(1)
        elif Requete == "Gicleur_2_ON":
            ser.write(b'Gicleur_2_ON')
            sauvegardeMessageActivites("Set gicleur arrosage termine")
            redisInOut.RequeteInterface=""
            Requete=""
            sleep(1)
        elif Requete == "Gicleur_2_OFF":
            ser.write(b'Gicleur_2_OFF')
            sauvegardeMessageActivites("Set gicleur près pour arrosage")
            redisInOut.RequeteInterface=""
            Requete=""
            sleep(1)
        elif Requete == "Gicleur_3_ON":
            ser.write(b'Gicleur_3_ON')
            sauvegardeMessageActivites("Set gicleur arrosage termine")
            redisInOut.RequeteInterface=""
            Requete=""
            sleep(1)
        elif Requete == "Gicleur_3_OFF":
            ser.write(b'Gicleur_3_OFF')
            sauvegardeMessageActivites("Set gicleur près pour arrosage")
            redisInOut.RequeteInterface=""
            Requete=""
            sleep(1)
        elif Requete == "Gicleur_4_ON":
            ser.write(b'Gicleur_4_ON')
            sauvegardeMessageActivites("Set gicleur arrosage termine")
            redisInOut.RequeteInterface=""
            Requete=""
            sleep(1)
        elif Requete == "Gicleur_4_OFF":
            ser.write(b'Gicleur_4_OFF')
            sauvegardeMessageActivites("Set gicleur près pour arrosage")
            redisInOut.RequeteInterface=""
            Requete=""
            sleep(.2)
