#UART communication on Raspberry Pi using Pyhton
#//http://www.electronicwings.com
#//'''
# https://devpress.csdn.net/python/62f519d07e66823466189f98.html  pytho 3.9 et autres
import sys, os
# sys.path.insert(1, "C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\importFile")
sys.path.insert(1, "/home/pi/python")
import serial
from dataclasses import dataclass
from time import sleep
import jsonpickle
from json import JSONEncoder# 
from pymarshaler.marshal import Marshal
import redis
import threading
from datetime import datetime, timedelta
from enum import Enum
import pickle
import socket
import socketIpPort

#from pymarshaler.marshal import Marshal
# G:\DeveloppementEnvironnement\Python\systemeAlarmeMontreal\systeme
# C:\Users\Michel\Documents\DeveloppementEnvironnement\python\arduinoAlarmeArrosage\InterfacePythonArduino\Montreal

class const:
    format = "02-01-2006 15:04:05"
   
    HIGH                           = 1
    LOW                            = 0
    heureTestMatin                 = 7
    nombreCourrielQuotidien        = 5


DateHeureCourante =datetime
NomEquipement =str

CourrielValeur=""
courriel7Heures=bool

NoZone=0
Statut=0
Action=0
Requete=""

Host = "192.168.1.142"
HostEcranAlarme = "192.168.1.239"
HostEcranArrosage = "192.168.1.239"

class DETECTEUR:
   Prop: float
   Co: float
   Fumee: float
   Mouvement: float
   EauElectrique: float
   EauTraitement: float
   PanneElectrique: float
   EauPluie: float
   DectArrosageZone1: int
   DectArrosageZone2: int
   DectArrosageZone3: int
   DectArrosageZone4: int
   Temperature: float

@dataclass
class EQUIPEMENT: 
    DateHeureCourante: datetime = datetime.now()
    NomEquipement: str = ""
    Armmer: bool = False
    Alarme: bool = False
    Actif: bool = False
    Valeur: int = 0
    Affichage: bool = False
    AffichageWeb: bool = False
    MessageErreur: str =""

@dataclass
class GICLEURS_STATUT:  
    NoZone: int = 0
    Statut: bool = False
    Action: str = ""

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

def defineEquipementsVariables(nom , Actif, Armer, messageErreur):

    stockRec = EQUIPEMENT()
    stockRec.DateHeureCourante = datetime.now()
    stockRec.NomEquipement = nom
    stockRec.Actif = Actif
    stockRec.Armer = Armer
    stockRec.Alarme = False
    stockRec.Valeur = 1
    stockRec.AffichageWeb="green.png"

    stockRec.Affichage = 0
    stockRec.MessageErreur = messageErreur

    return stockRec


def initialiseVariables(**Equipement):

    #GicleursStatut := make(map[int]structure.GICLEURS_STATUT)

    NomEquipement = ""

    NomEquipement = "Prop"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte une fuite de propane")
    NomEquipement = "Co"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte une fuite de CO")
    NomEquipement = "Fumee"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme de la fumee")
    NomEquipement = "Mouvement"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte du mouvement dans le sous-sol")
    NomEquipement = "EauElectrique"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte de l eau dans la salle electrique")
    NomEquipement = "EauTraitement"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte de l eau dans la salle de traitement de l eau")
    NomEquipement = "PanneElectrique"
    Armer = False
    Actif = False
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte la pluie exterieure")
    NomEquipement = "EauPluie"
    Armer = False
    Actif = False
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte une panne electrique")
     
    GicleursStatut={}
    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 1
    gicleurRec.Statut = 0
    gicleurRec.Action = 0
    GicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 2
    gicleurRec.Statut = 0
    gicleurRec.Action = 0
    GicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 3
    gicleurRec.Statut = 0
    gicleurRec.Action = 0
    GicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 4
    gicleurRec.Statut = 0
    gicleurRec.Action = 0
    GicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    return Equipement, GicleursStatut



def detecteurDataStructure(dectArduino):
    detecteurs = DETECTEUR()

    detecteurs.Prop=dectArduino["Prop"]
    detecteurs.Co=dectArduino["Co"]
    detecteurs.Fumee=dectArduino["Fumee"]
    detecteurs.Mouvement=dectArduino["Mouvement"]
    detecteurs.EauElectrique=dectArduino["EauElectrique"]
    detecteurs.EauTraitement=dectArduino["EauTraitement"]
    detecteurs.PanneElectrique=dectArduino["PanneElectrique"]
    detecteurs.EauPluie=dectArduino["EauPluie"]
    detecteurs.DectArrosageZone1=dectArduino["DectArrosageZone1"]
    detecteurs.DectArrosageZone2=dectArduino["DectArrosageZone2"]
    detecteurs.DectArrosageZone3=dectArduino["DectArrosageZone3"]
    detecteurs.DectArrosageZone4=dectArduino["DectArrosageZone4"]
    detecteurs.DectFumeeSaTemperaturelleBillard=dectArduino["Temperature"]

    return detecteurs

def decodeDataDetecteur(detecteur, **Equipement):

    recEquipement=EQUIPEMENT()

    recEquipement = Equipement["Prop"]
    recEquipement.Valeur = detecteur.Prop
    recEquipement.DateHeureCourante = datetime.now()
 
    recEquipement = Equipement["Co"]
    recEquipement.Valeur = detecteur.Co
    recEquipement.DateHeureCourante = datetime.now()
 
    recEquipement = Equipement["Fumee"]
    recEquipement.Valeur = detecteur.Fumee
    recEquipement.DateHeureCourante = datetime.now()
 
    recEquipement = Equipement["Mouvement"]
    recEquipement.Valeur = detecteur.Mouvement
    recEquipement.DateHeureCourante = datetime.now()
 
    recEquipement = Equipement["EauElectrique"]
    recEquipement.Valeur = detecteur.EauElectrique
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["EauTraitement"]
    recEquipement.Valeur = detecteur.EauTraitement
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["PanneElectrique"]
    recEquipement.Valeur = detecteur.PanneElectrique
    recEquipement.DateHeureCourante = datetime.now()

 
    GicleursStatut = dict()
    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 1
    gicleurRec.Statut = int(detecteur.DectArrosageZone1)
    gicleurRec.Action = 0
    GicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 2
    gicleurRec.Statut = int(detecteur.DectArrosageZone2)
    gicleurRec.Action = 0
    GicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 3
    gicleurRec.Statut = int(detecteur.DectArrosageZone3)
    gicleurRec.Action = 0
    GicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 4
    gicleurRec.Statut = int(detecteur.DectArrosageZone4)
    gicleurRec.Action = 0
    GicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    return Equipement, GicleursStatut

def is_redis_available(r):
    try:
        r.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        return False
    return True

redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8",decode_responses=True)




def sauvegardeMessageActivites(DataLOG):
    global redisClient
       
    if is_redis_available(redisClient):
        try:
            messageActiviteStr=str(datetime.now())+','+str(DataLOG)
            redisClient.rpush (const.clefLog, messageActiviteStr)
           
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)
    else:
        redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8", decode_responses=True)

# ser= serial.Serial('COM4', 115200, timeout=2)


def InterfaceArduinoAction():
    global s, hostClient, Requete

    HOST = socketIpPort.SendRec["InterfaceArduinoAction"].Ip
    PORT = socketIpPort.SendRec["InterfaceArduinoAction"].Port
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        else:
                            Requete = pickle.loads(data)



            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.bind((HOST, PORT))
            # s.listen(1)
            # conn, addr = s.accept()
            # # print ('Connected by', addr)
            # #hostClient = s.getpeername()
            # data = conn.recv(4096)
            # Requete = pickle.loads(data)
            s.close()
            conn.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)


def sendSystemeAlarmeDataEquipement(HOST, PORT, **Equipement):
    try:
        # recreate the socket and reconnect
        print ("passe 1")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("passe 2: ",HOST,PORT)
        s.connect((HOST, PORT))
        print ("passe 3")
        data_string = pickle.dumps(Equipement)
        print ("passe 4")
        s.send(data_string)
        print ("passe 5")
        s.close()
        print ("passe 6")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
        print(exc_type, fname, exc_tb.tb_lineno)



# ser = serial.Serial("COM4", 115200, timeout=2)
ser = serial.Serial("/dev/ttyACM0", 115200, timeout=2)    #Open port with baud rate

sendMail("Systeme alarme Montreal","Le systeme d alarme a redemarre")

Host = "192.168.1.210"
HostEcranAlarme = "192.168.1.240"
HostEcranArrosage = "192.168.1.240"

if __name__ == '__main__':

    Equipement = dict()
    GicleurStatut = dict()
    Equipement, GicleursStatut = initialiseVariables(**Equipement)


    t1 = threading.Thread(target=InterfaceArduinoAction)
    t1.start()
    courriel7Heures = False

    while True:

        if t1.is_alive==False:
            t1.start()

        if ser.is_open==True:
            # print (" ser waiting ", ser.inWaiting())
            while ser.inWaiting()==0: pass
            if  ser.inWaiting()>0: 
                received_data=ser.readline()
                print(received_data)
                ser.flushInput() #
            else:
                print (" long 'a recevoir")
            # sleep(0.5)

            print (" --------------- R ", Requete)
            if Requete == "Gicleur_1_ON":
                ser.write(b'Gicleur_1_ON')
                sauvegardeMessageActivites("Set gicleur arrosage termine")
                Requete=""
                sleep(1)
            elif Requete == "Gicleur_1_OFF":
                ser.write(b'Gicleur_1_OFF')
                sauvegardeMessageActivites("Set gicleur près pour arrosage")
                Requete=""
                sleep(1)
            elif Requete == "Gicleur_2_ON":
                ser.write(b'Gicleur_2_ON')
                sauvegardeMessageActivites("Set gicleur arrosage termine")
                Requete=""
                sleep(1)
            elif Requete == "Gicleur_2_OFF":
                ser.write(b'Gicleur_2_OFF')
                sauvegardeMessageActivites("Set gicleur près pour arrosage")
                Requete=""
                sleep(1)
            elif Requete == "Gicleur_3_ON":
                ser.write(b'Gicleur_3_ON')
                sauvegardeMessageActivites("Set gicleur arrosage termine")
                Requete=""
                sleep(1)
            elif Requete == "Gicleur_3_OFF":
                ser.write(b'Gicleur_3_OFF')
                sauvegardeMessageActivites("Set gicleur près pour arrosage")
                Requete=""
                sleep(1)
            elif Requete == "Gicleur_4_ON":
                ser.write(b'Gicleur_4_ON')
                sauvegardeMessageActivites("Set gicleur arrosage termine")
                Requete=""
                sleep(1)
            elif Requete == "Gicleur_4_OFF":
                ser.write(b'Gicleur_4_OFF')
                sauvegardeMessageActivites("Set gicleur près pour arrosage")
                Requete=""
                sleep(1)

            try:
                detecteursRec = jsonpickle.decode(received_data)
                detecteurs = detecteurDataStructure(detecteursRec) 
                Equipement, GicleursStatut = decodeDataDetecteur(detecteurs, **Equipement)
                # print (received_data)
                # print (detecteurs.Prop)

                print ("---- a ",socketIpPort.SendRec["ArrosageSystemeDataGicleurs"].Ip,socketIpPort.SendRec["ArrosageSystemeDataGicleurs"].Port,  GicleursStatut["1"].Statut)
                sendSystemeAlarmeDataEquipement(socketIpPort.SendRec["AlarmeSystemeDataEquipement"].Ip, socketIpPort.SendRec["AlarmeSystemeDataEquipement"].Port, **Equipement )
                print ("---- b ",socketIpPort.SendRec["ArrosageSystemeDataGicleurs"].Ip,socketIpPort.SendRec["ArrosageSystemeDataGicleurs"].Port,  GicleursStatut["1"].Statut)
                sendSystemeAlarmeDataEquipement(socketIpPort.SendRec["ArrosageSystemeDataGicleurs"].Ip, socketIpPort.SendRec["ArrosageSystemeDataGicleurs"].Port, **GicleursStatut )
                print ("---- c ",GicleursStatut, socketIpPort.SendRec["ArrosageSystemeDataGicleurs"].Ip,socketIpPort.SendRec["ArrosageSystemeDataGicleurs"].Port,  GicleursStatut["1"].Statut)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
                # print(exc_type, fname, exc_tb.tb_lineno)
