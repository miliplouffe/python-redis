#UART communication on Raspberry Pi using Pyhton
#//http://www.electronicwings.com
#//'''
import sys, os
sys.path.insert(1, "G:\DeveloppementEnvironnement\Python\Systemes\ImportFile")
# sys.path.insert(1, "C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\importFile")
# sys.path.insert(1, "\home\pi\python")

from dataclasses import dataclass
from time import sleep
import socket,jsonpickle,pickle
from json import JSONEncoder
from pymarshaler.marshal import Marshal
import redis
import threading
from datetime import datetime, timedelta
import sys, os
from enum import Enum
import socketIpPort


#from pymarshaler.marshal import Marshal
# G:\DeveloppementEnvironnement\Python\systemeAlarmeMontreal\systeme


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
    clefRedisalarme            = "AlarmeMtlStructure"
    clefRedisEquipementAlarme  = "EqupementsStructure"
    clefRedisData              = "DataStructure"
    IPadresseServeur           = "192.168.1.210"
    portRedisServeur           = "6379"
    subscribeRequestWeb        = "alarmeMtlAction"
    publishNom                 = "alarmeMtlData"
    subscribeMtlDataInterface  = "alarmeMtlDataInterface"
    publishSystemeAlarmeStatut = "alarmeMtlStatut"
    publishValeurPluie          = "arrosageValeurPluie"
    publishEcranErreur          = "alarmeEcranErreur"
    clefCourriel                = "Courriel"
    clefLog                     = "alarmeLog"
    subscribeInterfaceEquipementsMtl   = "interfaceEquipementsMtl"

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

NoZone=0
Statut=0
Action=0

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



class DETECTEUR_ARROSAGE:
    DectArrosageZone1: int
    DectArrosageZone2: int
    DectArrosageZone3: int
    DectArrosageZone4: int   



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
    zoneList.append(NomEquipement)   
    NomEquipement = "AtelierEau"
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte de l'eau dans l'atelier")
    zoneList.append(NomEquipement)
    NomEquipement = "FumeeAtelier"
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte de la fumee dans le sous-sol")
    zoneList.append(NomEquipement)
    NomEquipement = "FumeeSalleBillard"
    Armer = False
    Actif = False
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme d'alarme a detecte de la fumee dans l'atelier'")

    NomEquipement = "EauPluie"
    Armer = False
    Actif = False
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Detection de la pluie exterieure")
    zoneList.append(NomEquipement)


    return Equipement

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
                # ecrisMessageAlerte(date + "," + leSujet + "," + message)
                courrielEnvoye = True         
            elif alarmeErreur == True and duree.total_seconds() > int(const.dureeCourriel*60):
                sendMail(leSujet, message)
                # ecrisMessageAlerte(date + "," + leSujet + "," + message)
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
            # ecrisMessageAlerte(date + "," + leSujet + "," + message)
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

    requeteWeb=""
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
    requeteWeb=""

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
    
# def ecrisMessageAlerte(message):
#     file_object = open("C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\systemeAlarmeMontreal\\Systeme\\alarmeLog.txt", 'a')
#     # file_object = open("/home/pi/python/alarmeLog.txt", 'a')
#     file_object.write(message+'\n')
#     file_object.close()



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




def is_redis_available(r):
    try:
        r.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        return False
    return True

redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8",decode_responses=True)



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
            print (CourrielValeur)

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
        
def AlarmeSystemeAction():
    global  IPAddrLocal, Requete

    HOST = SendRec["AlarmeSystemeAction"].Ip
    PORT = SendRec["AlarmeSystemeAction"].Port
    while True:
        try:

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen(1)
                conn, addr = s.accept()
                with conn:
                    # print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        else:
                            Requete = pickle.loads(data)
            sleep(1)
            s.close()
            conn.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)

def InterfaceArduinoAlarmeData():
    global s, Equipement, gicleursStatut

    HOST = SendRec["AlarmeSystemeDataEquipement"].Ip
    PORT = SendRec["AlarmeSystemeDataEquipement"].Port

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen(1)
                conn, addr = s.accept()
                with conn:
                    # print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        else:
                            Equipement = pickle.loads(data)
            sleep(1)
            s.close()
            conn.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)

SendRec=dict()
socketIpPort.Host = "192.168.1.210"
socketIpPort.HostEcranAlarme = "192.168.1.227"
socketIpPort.HostEcranArrosage = "192.168.1.227"
SendRec = socketIpPort.initIpPort()



CourrielValeur=recupereCourrielStatut()
sendMail("Systeme alarme Montreal","Le systeme d alarme a redemarre")

if __name__ == '__main__':

    t2 = threading.Thread(target=AlarmeSystemeAction)
    t2.start()


    t1 = threading.Thread(target=InterfaceArduinoAlarmeData)
    t1.start()
   
    courriel7Heures = False
 

    # datetime object containing current date and time
    currentTime = datetime.now()
    dateHeureUpLoadScreen = datetime.now()
    dateHeureDemarreApps = datetime.now()
    dateHeureValideCircuit=datetime.now()
    dateHeureAlarme=datetime.now()

    Equipement = dict()
    Equipement = initialiseVariables(**Equipement)

    alarmeErreur = False
    systemeArmer = False
    heureCourrielEnvoye=datetime.now()
    courrielEnvoye = False
    DateHeureCourante=datetime.now()
    systemeAlarme=False
    activeCompletTest="non"
    requeteWeb=""
    detecteursRec:DETECTEUR
    marshal = Marshal()
    mustSendToClient=False
    systemeAlarmeSatut=""

    readAllData=True


    while True:

        if readAllData==True:

            try:

                # Equipement = decodeDataDetecteur(detecteurs, **Equipement)
                #if systemeAlarmeSatut=="ActivationPartielle" or systemeAlarmeSatut=="ActivationComplete":

                Equipement = changeValeursPinsArmer(**Equipement)
                sendSystemeAlarmeDataEquipement(socketIpPort.SendRec["AlarmeEcranDataEquipement"].Ip, socketIpPort.SendRec["AlarmeEcranDataEquipement"].Port, **Equipement )

                publishDataPourWebEtEcran(const.publishNom, **Equipement)
                publishDataPluie(Equipement)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
                print(exc_type, fname, exc_tb.tb_lineno)

        else:
            sleep(1)
    
        readAllData=True
        if requeteWeb == str("ActivationPartielle") and valideDetecteurArmerSystemePartiel(**Equipement) == True:
            print(" activation partielle  ")
            Equipement = assigneStatutArmerPartiel(**Equipement)
            systemeArmer = True
            mustSendToClient = True
            systemeAlarmeSatut = "ActivationPartielle"
            publishActionPourWebEtEcran(systemeAlarmeSatut)
            sleep(0.5)
            readAllData=False
            sendMail("Systeme alarme Montreal","Le systeme d alarme est active partiellement")
            requeteWeb = ""


        if requeteWeb == "ActivationComplete" and valideDetecteurArmerSystemeComplet(**Equipement) == True:
            # print(" activation est complete  ")
            Equipement = assigneStatutArmerComplet(**Equipement)
            sauvegardeMessageActivites("valideDetecteurArmerSystemeComplet est OK")
            sleep(15)
            systemeArmer = True
            mustSendToClient = True
            systemeAlarmeSatut = "ActivationComplete"
            #writeModeActuelAlarmeFile("Activation complete")
            publishActionPourWebEtEcran(systemeAlarmeSatut)
            sauvegardeMessageActivites(systemeAlarmeSatut)
            sleep(0.5)
            requeteWeb = ""
            readAllData=False
            #activeCompletTest = ""
            sendMail("Systeme alarme Montreal","Le systeme d alarme est active completement")

        if requeteWeb == "Desactivation":
            print(" desactivation ")
            Equipement = valideDetecteurDesactivation(**Equipement)
            requeteWeb = ""
            mustSendToClient = True
            systemeArmer = False
            courrielEnvoye = False
            systemeAlarmeSatut = "Desactivation"
            publishActionPourWebEtEcran(systemeAlarmeSatut)
            sleep(0.5)
            ser.write(b'AlarmeSonore_OFF')
            readAllData=False
            # go AvertisseurAlarme.Demarrer(AlarmeSonore_OFF)
            # writeModeActuelAlarmeFile("Desactivation")
            sendMail("Systeme alarme Montreal","Le systeme d alarme est desactive")
        

        if requeteWeb == "shutdown":
            print("shutdown")
            os.system('sudo shutdown now')
            #cmd := exec.Command("shutdown", "/sbin")
            #cmd.Run()
            #requeteWeb = ""
        if requeteWeb == "Redemarrer":
            print("shutdown")
            os.system('sudo reboot now')

    
        if requeteWeb == "courrielActif":
            CourrielValeur="courrielActif"
        if requeteWeb == "courrielInactif":
            CourrielValeur="courrielInactif"

        

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

                




