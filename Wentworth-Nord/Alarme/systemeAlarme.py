#UART communication on Raspberry Pi using Pyhton
#//http://www.electronicwings.com
#//'''
import sys, os
# sys.path.insert(1, "C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\importFile")
sys.path.insert(1, "\home\pi\python")

from dataclasses import dataclass
from time import sleep
import jsonpickle
from json import JSONEncoder
from pymarshaler.marshal import Marshal
import redis
import threading
from datetime import datetime, timedelta
from enum import Enum
import pickle
import socket
import socketIpPort


#from pymarshaler.marshal import Marshal
# C:\Users\Michel\Documents\DeveloppementEnvironnement\python\systemeAlarmeMontreal\systeme


class const:
    format = "02-01-2006 15:04:05"
    alarmeDureePorteAvant = 20
    alarmeDureeNormale             = 0
    nombreCourrielEnvoye           = 1
    zoneInactive                   = -1
    zoneActive                     = 1
    valeurNulle                    = -1
    alarmeDuree                    = 5  # devrait etre 5
    dureeUpload                    = 1  # devrait être 60 minutes
    dureeCourriel                  = 60 #  minutes
    dureeRaspberryErreur           = 5
    dureMinutesMouvement           = 2
    dureeSauveFichier              = 1
    heureTestMatin                 = 7
    dureeValideCircuit             = 1
    dureeMessageEnvoyeDropBox      = 5  # minutes
    dureeAlerteElectriciteCourriel = 5  # minutes
    dureeThreadConnexion           = 15 # 15 minutes
    dureeVerifieThreadConnexion    = 2  # 2 minutes
    dureeAlarme                    = 5 # minutes
    gpioAlarme                     = 19 # alarme
    dureeuploadToScreen            = 1  # nb de seconde pour envoyer a l ecran
    HIGH                           = 1
    LOW                            = 0
    nombreCourrielQuotidien        = 5

    publishEcranErreur          = "alarmeEcranErreur"
    clefLog                     = "alarmeLog"


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



class DETECTEUR:
    Prop: float
    Co: float
    Fumee: float
    Mouvement: float
    EauElectrique: float
    EauTraitement: float
    PanneElectrique: float
    DectArrosageZone1: int
    DectArrosageZone2: int
    DectArrosageZone3: int
    DectArrosageZone4: int
    Temperature: float

DateHeureCourante =datetime
NomEquipement =str
Armmer = bool 
Alarme=bool
Actif = bool
Valeur=int
Affichage=bool
MessageErreur=str
AffichageWeb=str
zoneList = []
CourrielValeur=""
courriel7Heures=bool
gicleursStatut=dict()
NoZone=0
Statut=0
Action=0



socketIpPort.Host="192.168.1.142"
socketIpPort.HostEcranAlarme="192.168.1.239"
socketIpPort.HostEcranArrosage="192.168.1.239"

def detecteurDataStructure(dectArduino):
    global detecteurs
    # detecteurs = DETECTEUR()

    detecteurs.Prop=dectArduino["Prop"]
    detecteurs.Co=dectArduino["Co"]
    detecteurs.Fumee=dectArduino["Fumee"]
    detecteurs.Mouvement=dectArduino["Mouvement"]
    detecteurs.EauElectrique=dectArduino["EauElectrique"]
    detecteurs.EauTraitement=dectArduino["EauTraitement"]
    detecteurs.EauTraitement=dectArduino["EauPluie"]

    detecteurs.PanneElectrique=dectArduino["PanneElectrique"]
    detecteurs.DectArrosageZone1=dectArduino["DectArrosageZone1"]
    detecteurs.DectArrosageZone2=dectArduino["DectArrosageZone2"]
    detecteurs.DectArrosageZone3=dectArduino["DectArrosageZone3"]
    detecteurs.DectArrosageZone4=dectArduino["DectArrosageZone4"]

    return detecteurs

@dataclass
class Test:
    name: str = ""


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
     
    return Equipement

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


    return Equipement

def verifieErreurs(systemeArmer,heureCourrielEnvoye,courrielEnvoye,systemeAlarme,dateHeureAlarme,alarmeErreur,**Equipement):
    message =""
    date = datetime.now()
    leSujet = ""

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
    
        for i in Equipement:
            rec=Equipement[i]
            if systemeArmer == True:
                #  and rec.NomEquipement.find("Arrosage")==-1
                if (rec.Armer == True and rec.Valeur == 1):
                    alarmeErreur = True
                    rec.Alarme = True
                    leSujet = "Maison de Montreal"
                    message =rec.MessageErreur
                    dateHeureAlarme=datetime.now()
                else:
                    rec.Alarme = False
            else:
                #  and rec.NomEquipement.find("Arrosage")==-1
                if (rec.NomEquipement in zoneList and rec.Valeur == 1 and rec.Armer == True):
                    alarmeErreur = True
                    rec.Alarme = True
                    leSujet = "Maison de Montreal"
                    message =rec.MessageErreur
                    dateHeureAlarme=datetime.now()

        if alarmeErreur == True: 
            duree=datetime.now()-heureCourrielEnvoye
            duree.total_seconds()
            # ser.write(b'AlarmeSonore_ON')
            if courrielEnvoye == False:
                sendMail(leSujet, message)
                ecrisMessageAlerte(date + "," + leSujet + "," + message)
                courrielEnvoye = True         
            elif alarmeErreur == True and duree.total_seconds() > int(const.dureeCourriel*60):
                sendMail(leSujet, message)
                ecrisMessageAlerte(date + "," + leSujet + "," + message)
                heureCourrielEnvoye = datetime.now()
                systemeAlarme = True      

        delaie=datetime.now()-dateHeureAlarme
        if delaie.total_seconds() > const.dureeAlarme*60:
            alarmeErreur=False
            MessageErreur=""
        
        if alarmeErreur == False and systemeAlarme == True and systemeArmer == True:
            leSujet = "Maison de Montreal"
            message = "le systeme est revenue à la normal"
            sendMail(leSujet, message)
           #  ecrisMessageAlerte(date + "," + leSujet + "," + message)
            systemeAlarme = False
            courrielEnvoye = False
            ## ecrireAlarmeFichier(Equipements)
            # ser.write(b'AlarmeSonore_OFF')
            # go AvertisseurAlarme.Demarrer(AlarmeSonore_OFF)
    except Exception as ex:
        print(ex)

    return systemeArmer,heureCourrielEnvoye,courrielEnvoye,systemeAlarme,dateHeureAlarme,alarmeErreur,Equipement

def valideDetecteurArmerSystemePartiel(**Equipements):
    resultat=False
    
    if Equipements["PorteEntree"].Valeur == 0 and Equipements["PorteArriere"].Valeur == 0 and Equipements["PorteSousSol"].Valeur == 0: 
        resultat = False
    else:
        resultat = True

    Requete=""
    print(Equipements["PorteEntree"].Valeur , Equipements["PorteArriere"].Valeur,Equipements["PorteSousSol"].Valeur)
    return resultat


def assigneStatutArmerPartiel(**Equipement):

    for i in Equipement:
        equipementRec=EQUIPEMENT()
        equipementRec=Equipement[i]
        # and equipementRec.NomEquipement not in zoneList
        if equipementRec.Actif==True  :
            if equipementRec.NomEquipement == "PorteEntree" or equipementRec.NomEquipement == "PorteArriere" or equipementRec.NomEquipement == "PorteSousSol":
                equipementRec.Armer = True
        else:
            equipementRec.Valeur=2
            equipementRec.Armer = False
            
    return Equipement


def valideDetecteurArmerSystemeComplet(**Equipements):
    resultat=False
    for i in Equipement:
        equipementRec=EQUIPEMENT()
        equipementRec=Equipement[i]
        if equipementRec.Actif == True and equipementRec.NomEquipement not in zoneList:     
            if equipementRec.Valeur == 0:
                resultat = False
                break
            else:
                resultat = True
                   
    sauvegardeMessageActivites("le résultat si valide = "+ str(resultat))
    Requete=""

    return resultat

def assigneStatutArmerComplet(**Equipement):
    for i in Equipement:
        equipementRec=EQUIPEMENT()
        equipementRec=Equipement[i]
        #  and equipementRec.NomEquipement not in zoneList
        if equipementRec.Actif==True:
            equipementRec.Armer = True
        else:
            equipementRec.Armer=False

    return Equipement

def valideDetecteurDesactivation(**Equipements):

    for i in Equipement:
        equipementRec=EQUIPEMENT()
        equipementRec=Equipement[i]
        if equipementRec.NomEquipement == "ChauffeEau" or equipementRec.NomEquipement == "AtelierEau" or equipementRec.NomEquipement == "FumeeAtelier" or equipementRec.NomEquipement == "FumeeBas":
            equipementRec.Armer = True
        else:
            equipementRec.Armer = False
            equipementRec.Affichage = 2

    systemeAlarme = False

    return Equipements
# change la couleur de la pin en orange en fonction du systeme armee
def changeValeursPinsArmer(**Equipement):

    for i in Equipement:
        equipementRec=EQUIPEMENT()
        equipementRec=Equipement[i]
        if equipementRec.Actif==True:
            if equipementRec.Armer==False:
                if equipementRec.Valeur == 1:
                    equipementRec.AffichageWeb="static/images/red.png"
                else:
                    if equipementRec.Valeur == 2 or equipementRec.Valeur == 0:
                        equipementRec.AffichageWeb="static/images/orange.png"
                        equipementRec.Valeur = 2

            else:
                if equipementRec.Valeur == 1:
                    equipementRec.AffichageWeb="static/images/red.png"
                else:
                    if equipementRec.Valeur == 0:
                        equipementRec.AffichageWeb="static/images/green.png"
        else:
            equipementRec.Valeur = 2
            equipementRec.AffichageWeb="static/images/orange.png"
       

    return Equipement
    
def ecrisMessageAlerte(message):
    file_object = open("C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\systemeAlarmeMontreal\\Systeme\\alarmeLog.txt", 'a')
    # file_object = open("/home/pi/python/alarmeLog.txt", 'a')
    file_object.write(message+'\n')
    file_object.close()



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




def is_redis_available(r):
    try:
        r.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        return False
    return True

redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8",decode_responses=True)

# def redisSubscribeInterfaceAlarmeMtl():
#     global detecteurs
#     global redisClient
#     global Equipement
# 
#     if is_redis_available(redisClient):
#         clientSubscribe = redisClient.pubsub()
#         clientSubscribe.subscribe(const.subscribeInterfaceEquipementsMtl)
#         for message in clientSubscribe.listen():
#             if message is not None and isinstance(message, dict):
#                 xxxxxx = message.get('data')
#                 if xxxxxx!=1:
#                     Equipement = jsonpickle.decode(xxxxxx)
#                     #Equipement=json.loads(DataFromRedis, cls=EquipementsDecoder)
#     else:
#         redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8", decode_responses=True)

def SystemeAlarmeAction():
    global s, hostClient

    HOST = socketIpPort.SendRec["AlarmeSystemeAction"].Ip
    PORT = socketIpPort.SendRec["AlarmeSystemeAction"].Port

    try:
        while True: 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen(1)
            print (" Requete :")
            conn, addr = s.accept()
            print ('Connected by', addr)
            # hostClient = s.getpeername()
            data = conn.recv(4096)
            Requete = pickle.loads(data)
            print (" Requete :", Requete)
            conn.close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
        print(exc_type, fname, exc_tb.tb_lineno)


def InterfaceArduinoAlarmeData():
    global hostClient, EquipementInterface

    HOST = socketIpPort.SendRec["AlarmeSystemeDataEquipement"].Ip
    PORT = socketIpPort.SendRec["AlarmeSystemeDataEquipement"].Port

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen(5)
            conn, addr = s.accept()
            print ('Connected by', addr)
            #hostClient = s.getpeername()
            data = conn.recv(4096)
            EquipementInterface = pickle.loads(data)
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
        data_string = pickle.dumps(Equipement)
        s.send(data_string)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
        print(exc_type, fname, exc_tb.tb_lineno)


def publishEcranErreur(action):
    global redisClient
    if is_redis_available(redisClient):
        try:
            redisClient.publish(const.publishEcranErreur, action)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)
            publishEcranErreur(" Erreur systeme alarme publishEcranErreur " +  " " + exc_type + " " + fname + " " + exc_tb.tb_lineno)
    else:
        redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8", decode_responses=True)

def recupereCourrielStatut():
    global redisClient
    global CourrielValeur

    if is_redis_available(redisClient):
        try:
            CourrielValeur = redisClient.get(const.clefCourriel)
            redisClient.publish(const.subscribeRequestWeb, CourrielValeur)

        except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
                    print(exc_type, fname, exc_tb.tb_lineno)
                #redisClient.publish(const.publishNom, dataToSend)
    else:
        redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8", decode_responses=True) 
    return CourrielValeur


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
# ser= serial.Serial("COM4", 115200, timeout=2)
# ser= serial.Serial("/dev/ttyACM0", 115200, timeout=2)    #Open port with baud rate

# CourrielValeur=recupereCourrielStatut()
sendMail("Systeme alarme Montreal","Le systeme d alarme a redemarre")



if __name__ == '__main__':

    t1 = threading.Thread(target=SystemeAlarmeAction)
    t1.start()

    t2 = threading.Thread(target=InterfaceArduinoAlarmeData)
    t2.start()

    courriel7Heures = False

    # datetime object containing current date and time
    currentTime = datetime.now()
    dateHeureUpLoadScreen = datetime.now()
    dateHeureDemarreApps = datetime.now()
    dateHeureValideCircuit=datetime.now()
    dateHeureAlarme=datetime.now()

    Equipement = dict()
    GicleurStatut = dict()
    Equipement = initialiseVariables(**Equipement)

    alarmeErreur = False
    systemeArmer = False
    heureCourrielEnvoye=datetime.now()
    courrielEnvoye = False
    DateHeureCourante=datetime.now()
    systemeAlarme=False
    activeCompletTest="non"
    Requete=""
    
    detecteurs=DETECTEUR()
    marshal = Marshal()
    mustSendToClient=False
    systemeAlarmeSatut=""

    readAllData=True


    while True:

        try:
            Equipement = changeValeursPinsArmer(**EquipementInterface)
            sendSystemeAlarmeDataEquipement(socketIpPort.SendRec["AlarmeEcranDataEquipement"].Ip, socketIpPort.SendRec["AlarmeEcranDataEquipement"].Port, **Equipement )

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)

        print (" Requete Web", Requete)

        if Requete == "ActivationComplete" and valideDetecteurArmerSystemeComplet(**Equipement) == True:
            # print(" activation est complete  ")
            Equipement = assigneStatutArmerComplet(**Equipement)
            sauvegardeMessageActivites("valideDetecteurArmerSystemeComplet est OK")
            sleep(15)
            systemeArmer = True
            mustSendToClient = True
            systemeAlarmeSatut = "ActivationComplete"
            #writeModeActuelAlarmeFile("Activation complete")
            sauvegardeMessageActivites(systemeAlarmeSatut)
            sleep(0.5)
            Requete = ""
            readAllData=False
            #activeCompletTest = ""
            sendMail("Systeme alarme Montreal","Le systeme d alarme est active completement")

        if Requete == "Desactivation":
            print(" desactivation ")
            Equipement = valideDetecteurDesactivation(**Equipement)
            Requete = ""
            mustSendToClient = True
            systemeArmer = False
            courrielEnvoye = False
            systemeAlarmeSatut = "Desactivation"
            sleep(0.5)
            # ser.write(b'AlarmeSonore_OFF')
            readAllData=False
            # go AvertisseurAlarme.Demarrer(AlarmeSonore_OFF)
            # writeModeActuelAlarmeFile("Desactivation")
            sendMail("Systeme alarme Montreal","Le systeme d alarme est desactive")
        

 

        if Requete == "courrielActif":
            CourrielValeur="courrielActif"
        if Requete == "courrielInactif":
            CourrielValeur="courrielInactif"

        Requete=""

        if (courriel7Heures == False and const.heureTestMatin== datetime.now().hour) or datetime.now().hour==8:
            if courriel7Heures == False and const.heureTestMatin== datetime.now().hour:
                courriel7Heures=True
                if alarmeErreur==False:
                    message="Le systeme n'est pas en erreur"
                else:
                    message="Le systeme est en erreur"
                sendMail("Systeme alarme Montreal",message)
            else:
                courriel7Heures=False

        if mustSendToClient == True:
            #dataJson, err = json.Marshal(Equipement)
            #dataAlarmeStatut, err2 = json.Marshal(systemeAlarmeSatut)
            
            #fmt.Println("prepare pour envoyer 2 ", err,  Equipement["Bureau"].NomEquipement,  Equipement["Bureau"].Actif,  Equipement["Bureau"].Valeur)
            #fmt.Println("prepare pour envoyer 2 ", err,  Equipement["PorteEntree"].NomEquipement,  Equipement["PorteEntree"].Actif,  Equipement["PorteEntree"].Valeur)
        
            #if err2 is None:
            #    publishDataPourWebEtEcran(**Equipement)
            #    publishActionPourWebEtEcran(dataAlarmeStatut)
            
            mustSendToClient = False
                        

        difference = datetime.now()-dateHeureValideCircuit
        difference.seconds

        if (difference.seconds >= const.dureeValideCircuit):
            systemeArmer,heureCourrielEnvoye,courrielEnvoye,systemeAlarme,dateHeureAlarme,alarmeErreur,Equipement = verifieErreurs(systemeArmer,heureCourrielEnvoye,courrielEnvoye,systemeAlarme,dateHeureAlarme,alarmeErreur,**Equipement)

                




