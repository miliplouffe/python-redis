#UART communication on Raspberry Pi using Pyhton
#//http://www.electronicwings.com
#//'''
import sys, os
# sys.path.insert(1, "C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\importFile")
sys.path.insert(1, "/home/pi/python")
import serial
from dataclasses import dataclass
from time import sleep
import jsonpickle
from json import JSONEncoder# 
from pymarshaler.marshal import Marshal
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

    clefLog                     = "alarmeLog"


DateHeureCourante =datetime
NomEquipement =str

CourrielValeur=""
courriel7Heures=bool

NoZone=0
Statut=0
Action=0
Requete=""


class DETECTEUR:
    MouvChambrePrincipale: int
    MouvChambreSecondaire: int
    MouvBureau: int
    MouvSalon: int
    MouvSalleBillard: int
    MouvSalleVernis: int
    InterPorteAvant: int
    InterPorteArriere: int
    InterPorteSousSol: int
    DectEauAtelier: int
    DectEauSalleLavage: int
    DectEauPluie: int
    DectFumeeSalleBillard: int
    DectFumeeAtelier: int
    DectArrosageZone1: int
    DectArrosageZone2: int
    DectArrosageZone3: int
    DectArrosageZone4: int

@dataclass
class EQUIPEMENT: 
    DateHeureCourante: datetime = datetime.now()
    NomEquipement: str = ""
    Armer: bool = False
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

@dataclass
class SOCKET_ACCESS:
    Nom: str=""
    Ip: str =""
    Port: int = ""


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

    NomEquipement = ""

    NomEquipement = "PorteEntree"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte une porte ouverte a l'entree")
    NomEquipement = "PorteArriere"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte une porte ouverte a l'arriere")
    NomEquipement = "PorteSousSol"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte une porte ouverte a la porte du sous-sol")
    NomEquipement = "ChambrePrincipale"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte un mouvement dans la chambre principale")
    NomEquipement = "ChambreSecondaire"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte un mouvement dans la chambre secondaire")
    NomEquipement = "ChambreSousSol"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte un mouvement dans la chambre su sous-sol")
    NomEquipement = "SalleBillard"
    Armer = False
    Actif = False
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte du mouvement a la salle de billard")
    NomEquipement = "Salon"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte du mouvement dans le salon")
    NomEquipement = "Bureau"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte un mouvement dans le bureau")
    NomEquipement = "ChauffeEau"
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte de l'eau au chauffe eau")
    
    NomEquipement = "AtelierEau"
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte de l'eau dans l'atelier")

    NomEquipement = "FumeeAtelier"
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte de la fumee dans le sous-sol")

    NomEquipement = "FumeeSalleBillard"
    Armer = False
    Actif = False
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte de la fumee dans l'atelier'")

    NomEquipement = "EauPluie"
    Armer = False
    Actif = False
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Detection de la pluie exterieure")

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

def decodeDataDetecteur(detecteur, **Equipement):

    recEquipement = Equipement["PorteEntree"]
    recEquipement.Valeur = detecteur.InterPorteAvant
    recEquipement.DateHeureCourante = datetime.now()
 
    recEquipement = Equipement["PorteArriere"]
    recEquipement.Valeur = detecteur.InterPorteArriere
    recEquipement.DateHeureCourante = datetime.now()
 
    recEquipement = Equipement["PorteSousSol"]
    recEquipement.Valeur = detecteur.InterPorteSousSol
    recEquipement.DateHeureCourante = datetime.now()
 
    recEquipement = Equipement["ChambrePrincipale"]
    recEquipement.Valeur = detecteur.MouvChambrePrincipale
    recEquipement.DateHeureCourante = datetime.now()
 
    recEquipement = Equipement["ChambreSecondaire"]
    recEquipement.Valeur = detecteur.MouvChambreSecondaire
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["ChambreSousSol"]
    recEquipement.Valeur = detecteur.MouvSalleVernis
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["SalleBillard"]
    recEquipement.Valeur = detecteur.MouvSalleBillard
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["Salon"]
    recEquipement.Valeur = detecteur.MouvSalon
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["Bureau"]
    recEquipement.Valeur = detecteur.MouvBureau
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["ChauffeEau"]
    recEquipement.Valeur = detecteur.DectEauSalleLavage
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["AtelierEau"]
    recEquipement.Valeur = detecteur.DectEauAtelier
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["FumeeAtelier"]
    recEquipement.Valeur = detecteur.DectFumeeAtelier
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["FumeeSalleBillard"]
    recEquipement.Valeur = detecteur.DectFumeeSalleBillard
    recEquipement.DateHeureCourante = datetime.now()

    recEquipement = Equipement["EauPluie"]
    recEquipement.Valeur = detecteur.DectEauPluie
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


def sauvegardeMessageActivites(DataLOG):
    global redisClient
       
    if is_redis_available(redisClient):
        try:
            messageActiviteStr=str(datetime.now())+','+str(DataLOG)
            redisClient.rpush (const.clefLog, messageActiviteStr)
           
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)
    else:
        redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8", decode_responses=True)




sendMail("Systeme alarme Montreal","Le systeme d alarme a redemarre")

def InterfaceArduinoAction():
    global s, hostClient, Requete

    HOST = SendRec["InterfaceArduinoAction"].Ip
    PORT = SendRec["InterfaceArduinoAction"].Port
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
                            print("Requete : ", Requete)
            sleep(1)
            s.close()
            conn.close()
           
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)


def sendSystemeAlarmeDataEquipement(HOST, PORT, **Equipement):
    try:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print ("connection :", HOST, PORT )
        data_string = pickle.dumps(Equipement)
        s.send(data_string)
        s.close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
        print(exc_type, fname, exc_tb.tb_lineno)



# ser = serial.Serial("COM4", 115200, timeout=2)
ser = serial.Serial("/dev/ttyACM0", 115200, timeout=2)    #Open port with baud rate

SendRec=dict()
socketIpPort.HostInterface = "192.168.1.210"
socketIpPort.HostSystemeArrosage="192.168.1.227"
socketIpPort.HostEcranAlarme = "192.168.1.227"
socketIpPort.HostEcranArrosage = "192.168.1.227"
SendRec = socketIpPort.initIpPort()

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
                # print(received_data)
                ser.flushInput() #
            else:
                print (" long 'a recevoir")
            # sleep(0.5)

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

            # print ("---- a ",SendRec["ArrosageSystemeDataGicleurs"].Ip,SendRec["ArrosageSystemeDataGicleurs"].Port,  GicleursStatut["1"].Statut)
            sendSystemeAlarmeDataEquipement(SendRec["AlarmeSystemeDataEquipement"].Ip, SendRec["AlarmeSystemeDataEquipement"].Port, **Equipement )
            # print ("---- b ",SendRec["ArrosageSystemeDataGicleurs"].Ip,SendRec["ArrosageSystemeDataGicleurs"].Port,  GicleursStatut["1"].Statut)
            sendSystemeAlarmeDataEquipement(SendRec["ArrosageSystemeDataGicleurs"].Ip, SendRec["ArrosageSystemeDataGicleurs"].Port, **GicleursStatut )
            # print ("---- c ",GicleursStatut, SendRec["ArrosageSystemeDataGicleurs"].Ip,SendRec["ArrosageSystemeDataGicleurs"].Port,  GicleursStatut["1"].Statut)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)