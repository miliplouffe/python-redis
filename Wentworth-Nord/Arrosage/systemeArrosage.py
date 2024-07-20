import sys, os
# sys.path.insert(1, "C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\importFile")
sys.path.insert(1, "/home/pi/python")
from time import sleep
import pickle
from json import JSONEncoder
from dataclasses import dataclass
import redis
import threading
from datetime import datetime, timedelta
import socket,jsonpickle
from time import sleep
import socketIpPort

# C:\Users\Michel\Documents\DeveloppementEnvironnement\python\systemeArrosage\ArrosageMontreal
#from pymarshaler.marshal import Marshal
NoZone=0
ZoneNom=""
TempsArrosage=False
ArrosageEnCour=False
ArrosageDemarre=False
ArrosageTermine=False
systemeArrosageEnCour=False
NombreJourInterval=2
ZoneActive=False
ZonePhysique=""
Affichage=False
AffichageWeb=False
MessageErreur=""
ValeurPluie=0
DateHeureCourante =datetime
DateHeureDebutArrosage = datetime
DateHeureDebutIntervalle = datetime
Message=""
reset6Heures = False

class const:
    format = "02-01-2006 15:04:05"
    nombreCourrielEnvoye           = 1
    zoneInactive                   = -1
    zoneActive                     = 1
    valeurNulle                    = -1
    dureeUpload                    = 1  # devrait être 60 minutes
    dureeCourriel                  = 60 #  secondes
    dureeRaspberryErreur           = 5
    dureeSauveFichier              = 1
    heureTestMatin                 = 7
    dureeThreadConnexion           = 15 # 15 minutes
    dureeVerifieThreadConnexion    = 2  # 2 minutes
    dureeuploadToScreen            = 1  # nb de seconde pour envoyer a l ecran
    HIGH                           = 1
    LOW                            = 0
    nombreCourrielQuotidien        = 5

    gicleurData                 = "GicleurData"
    confGeneralData             = "ConfGeneralData"
    clefMessage                 = "MessageClef"
    clefLog                     = "alarmeLog"
  


@dataclass
class MESSAGES_ACTIVITES:
    DateMessage: datetime = datetime.now()
    NoZone: int= 0
    Message: str = ""

@dataclass
class GICLEURS:
    NoZone: int = 0
    ZoneNom: str = ""
    ZonePhysique: str = ""
    ZoneActive: bool = False
    TempsArrosage: int = 0
    Affichage: bool = False
    AffichageWeb: bool = False
    MessageErreur: str = ""

@dataclass
class ARROSAGE_DATA:
    NoZone: int = 0
    TempsArrosage: int = 0
    ArrosageEnCour: bool = False
    ArrosageTermine: bool = False

@dataclass
class CONFIGURATION_GENERALE:
    HeureDebutArrosage: str = ""   
    SystemArrosageActif: bool = False         
    SondePluieActive: bool = False           
    ArrosageJourPairImpair: str = ""
    NombreJourInterval: int = 0    

@dataclass
class GICLEURS_STATUT:  
    NoZone: int = 0
    Statut: bool = False
    Action: str = ""

@dataclass
class GICLEUR_EN_COUR:  
    NoZone: int = 0  
    HeureDepartArrosage: int = 0  

@dataclass
class SOCKET_ACCESS:
    Nom: str=""
    Ip: str =""
    Port: int = ""

Host = "192.168.1.142"
HostEcranAlarme = "192.168.1.240"
HostEcranArrosage = "192.168.1.240"


def initializeDonneesGenerales(**donneesArrosage):
    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="1"
    donneesGeneralesRec.TempsArrosage=40
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="2"
    donneesGeneralesRec.TempsArrosage=40
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="3"
    donneesGeneralesRec.TempsArrosage=40
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="4"
    donneesGeneralesRec.TempsArrosage=40
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    return donneesArrosage

def initialiseGicleursStatut(**gicleursStatut):
    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 1
    gicleurRec.Statut = 0
    gicleurRec.Action = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 2
    gicleurRec.Statut = 0
    gicleurRec.Action = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 3
    gicleurRec.Statut = 0
    gicleurRec.Action = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    gicleurRec = GICLEURS_STATUT()
    gicleurRec.NoZone = 4
    gicleurRec.Statut = 0
    gicleurRec.Action = 0
    gicleursStatut[str(gicleurRec.NoZone)] = gicleurRec

    return gicleursStatut


def recupereConfigurationGeneralGicleurs():
    global redisClient
    global gicleurs

    if is_redis_available(redisClient):
        try:
            value = redisClient.get(const.gicleurData)
            gicleurs = jsonpickle.decode(value)

            value=redisClient.get(const.confGeneralData)
            confGeneral=jsonpickle.decode(value)
        except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
                    print(exc_type, fname, exc_tb.tb_lineno)
                #redisClient.publish(const.publishNom, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=Host, port=6379, charset="utf-8", decode_responses=True) 

    return gicleurs, confGeneral


def sauvegardeMessageLogs(DataLOG):
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
        redisClient = redis.StrictRedis(host=Host, port=6379, charset="utf-8", decode_responses=True)


def sauvegardeMessageActivites(DateMessage,NoZone,Message):
    global redisClient
    
    messageActivite = MESSAGES_ACTIVITES(DateHeureCourante, NoZone, Message)
    messageActivite.DateMessage=DateMessage
    messageActivite.NoZone=NoZone
    messageActivite.Message=Message
    
    if is_redis_available(redisClient):
        try:
            messageActiviteStr=str(messageActivite.DateMessage)+','+str(messageActivite.NoZone)+','+str(messageActivite.Message)
            redisClient.lpush  (const.clefMessage, messageActiviteStr)
           
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)
    else:
        redisClient = redis.StrictRedis(host=Host, port=6379, charset="utf-8", decode_responses=True)

        

def is_redis_available(r):
    try:
        r.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        return False
    return True


redisClient = redis.StrictRedis(host=Host, port=6379, charset="utf-8",decode_responses=True)


def arrosageValide():
    global ValeurPluie
    global confGeneral
    global DateHeureDebutIntervalle
    global ArrosageDemarre

    valide=False
    jourValide=False
    dateHeureValide=False
    DateHeureCourante=datetime.now()
    pluieValide=False

    if DateHeureCourante.day  % 2 == 0 and confGeneral.ArrosageJourPairImpair=="Pair":
        jourValide=True
    else:
        if DateHeureCourante.day  % 2 != 0 and confGeneral.ArrosageJourPairImpair=="Impair":
            jourValide=True
            #sauvegardeMessageLogs("Systeme arrosage Montreal heure et jour impair pair : " + str(jourValide))
        else:
            jourValide=False

    if confGeneral.SystemArrosageActif==True:
        if confGeneral.SondePluieActive==False:
            pluieValide=True

        if pluieValide==True and confGeneral.HeureDebutArrosage==DateHeureCourante.hour and jourValide==True and (datetime.now() - DateHeureDebutIntervalle).days >= confGeneral.NombreJourInterval:
           valide=True
        else:
            valide=False

        
    # print ("Nombre de jour interval pour l arrosage : ", valide, (datetime.now() - DateHeureDebutIntervalle).days, confGeneral.NombreJourInterval)  

    return valide



def ArrosageSystemeDataGicleurs():
    global s, Equipement, gicleursStatut

    HOST = socketIpPort.SendRec["ArrosageSystemeDataGicleurs"].Ip
    PORT = socketIpPort.SendRec["ArrosageSystemeDataGicleurs"].Port

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen(1)
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(4096)
                        if not data:
                            break
                        else:
                            gicleursStatut = pickle.loads(data)
            s.close()
            conn.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)


def ArrosageEcranDataEquipement(HOST, PORT, **gicleursStatut):
    global s

    try:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        data_string = pickle.dumps(gicleursStatut)
        s.send(data_string)
        s.close()
    except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)

def InterfaceArduinoAction(HOST, PORT, Requete):
    global s
    try:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        data_string = pickle.dumps(Requete)
        s.send(data_string)
        s.close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
        # print(exc_type, fname, exc_tb.tb_lineno)

def GicleursSystemeAction():
    global  IPAddrLocal, Requete

    HOST = socketIpPort.SendRec["GicleursSystemeAction"].Ip
    PORT = socketIpPort.SendRec["GicleursSystemeAction"].Port
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen(1)
            conn, addr = s.accept()
            print ('Connected by', addr)
            # hostClient = s.getpeername()
            data = conn.recv(4096)
            Requete = pickle.loads(data)
            s.close()
            conn.close()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)


# hostname=socket.gethostname()  
# socketIpPort.SendRec["ArrosageEcranDataEquipement"].Ip=socket.gethostbyname(hostname)  
  

confGeneral=dict()
donneesArrosage=dict()
donneesArrosage=initializeDonneesGenerales(**donneesArrosage)
gicleurs=dict()
gicleurEnCour = GICLEUR_EN_COUR()
gicleursStatut=dict()
gicleursStatut = initialiseGicleursStatut()
Requete=""



if __name__ == '__main__':
    global valeurPluie

    DateHeureCourante=datetime.now()
    DateHeureDebutIntervalle=datetime.now() + timedelta(days=-10)
    sauvegardeMessageLogs("Systeme arrosage Montreal :" + "systeme demarre" )
    sleep(3)

    gicleurs, confGeneral = recupereConfigurationGeneralGicleurs()

    t3 = threading.Thread(target=ArrosageSystemeDataGicleurs)
    t3.start()

    t1 = threading.Thread(target=GicleursSystemeAction)
    t1.start()


    for rec in donneesArrosage:
        InterfaceArduinoAction(socketIpPort.SendRec["InterfaceArduinoAction"].Ip,socketIpPort.SendRec["InterfaceArduinoAction"].Port,gicleurs[rec].ZoneNom+"OFF")
        sleep (1)

    while True :  

        if t3.is_alive==False:
            t3.start()

        if t1.is_alive==False:
            t1.start()

        if Requete == "NouvelleConfiguration":
           print (" nouvelle configuration -------------------- ", Requete)
           gicleurs, confGeneral = recupereConfigurationGeneralGicleurs()
           sauvegardeMessageActivites(datetime.now(),"config general et gicleurs", "Changement de configuration")
           InterfaceArduinoAction(socketIpPort.SendRec["InterfaceArduinoAction"].Ip,socketIpPort.SendRec["InterfaceArduinoAction"].Port, "NouvelleConfiguration")
        elif Requete == "GicleurSet1":
            dataRec=donneesArrosage["1"]
            dataRec.ArrosageTermine=True
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
        elif Requete == "GicleurReSet1":
            dataRec=donneesArrosage["1"]
            dataRec.ArrosageTermine=False
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
        elif Requete == "GicleurSet2":
            dataRec=donneesArrosage["2"]
            dataRec.ArrosageTermine=True
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
        elif Requete == "GicleurReSet2":
            dataRec=donneesArrosage["2"]
            dataRec.ArrosageTermine=False
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
        elif Requete == "GicleurSet3":
            dataRec=donneesArrosage["3"]
            dataRec.ArrosageTermine=True
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
        elif Requete == "GicleurReSet3":
            dataRec=donneesArrosage["3"]
            dataRec.ArrosageTermine=False
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
        elif Requete == "GicleurSet4":
            dataRec=donneesArrosage["4"]
            dataRec.ArrosageTermine=True
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
        elif Requete == "GicleurReSet4":
            dataRec=donneesArrosage["4"]
            dataRec.ArrosageTermine=False
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
        # Requete en plus de faire des reset, il ouvre et ferme les valves de gicleurs
      
            

        Requete=""

        for rec in donneesArrosage:
            dataRec=ARROSAGE_DATA()
            dataRec=donneesArrosage[rec]
            
            # print (" valeurs : ",  dataRec.NoZone, ArrosageDemarre==True , dataRec.ArrosageTermine==False , dataRec.ArrosageEnCour==False , systemeArrosageEnCour==False , gicleurs[rec].ZoneActive==True)
            if  arrosageValide()==True and dataRec.ArrosageTermine==False and dataRec.ArrosageEnCour==False and systemeArrosageEnCour==False and gicleurs[rec].ZoneActive==True:
                # depart du gicleur
                dataRec.ArrosageEnCour=True
                systemeArrosageEnCour=True
                ArrosageDemarre=True
                gicleurEnCour.HeureDepartArrosage=datetime.now()
                gicleurEnCour.NoZone=dataRec.NoZone
                DateHeureDebutArrosage=datetime.now()
                InterfaceArduinoAction(socketIpPort.SendRec["InterfaceArduinoAction"].Ip,socketIpPort.SendRec["InterfaceArduinoAction"].Port, gicleurs[rec].ZoneNom+"ON")
                sauvegardeMessageActivites(datetime.now(),gicleurEnCour.NoZone, "Arrosage en cours" )
                sleep(1)
                sauvegardeMessageLogs("Systeme arrosage Montreal :" + str(gicleurEnCour.NoZone) + "  Arrosage en cours" )
                donneesArrosage[dataRec.NoZone]=dataRec
                reset6Heures=False
                break
        


            if systemeArrosageEnCour==True and (datetime.now()-gicleurEnCour.HeureDepartArrosage).seconds > 10:
                if gicleursStatut[str(gicleurEnCour.NoZone)].Statut == 0:
                     dataRec=ARROSAGE_DATA()
                     dataRec=donneesArrosage[gicleurEnCour.NoZone]
                     dataRec.ArrosageTermine=True
                     dataRec.ArrosageEnCour=False
                     systemeArrosageEnCour=False
                     sauvegardeMessageActivites(datetime.now(),gicleurEnCour.NoZone, "L arrosage n a pas lieu. Le detecteur montre 0" )
                     sleep(1)
                     sauvegardeMessageLogs("Systeme arrosage Montreal :" + str(gicleurEnCour.NoZone) +"  L arrosage n a pas lieu. Le detecteur montre 0"  )
                     donneesArrosage[str(gicleurEnCour.NoZone)]=dataRec
# 
                if (datetime.now()-gicleurEnCour.HeureDepartArrosage).seconds/60 >= int(gicleurs[str(gicleurEnCour.NoZone)].TempsArrosage):
                    # arret du gicleur

                    dataRec=ARROSAGE_DATA()
                    dataRec=donneesArrosage[gicleurEnCour.NoZone]
                    dataRec.ArrosageTermine=True
                    dataRec.ArrosageEnCour=False
                    systemeArrosageEnCour=False
                    InterfaceArduinoAction(socketIpPort.SendRec["InterfaceArduinoAction"].Ip,socketIpPort.SendRec["InterfaceArduinoAction"].Port, gicleurs[gicleurEnCour.NoZone].ZoneNom+"OFF")
                    sleep(.5)
                    sauvegardeMessageActivites(datetime.now(),gicleurEnCour.NoZone, "Arrosage terminé" )
                    sleep(2)
                    sauvegardeMessageLogs("Systeme arrosage Montreal :" + str(gicleurEnCour.NoZone) +"  Arrosage terminé")

                    donneesArrosage[dataRec.NoZone]=dataRec

        
        if datetime.now().hour==16 and reset6Heures == False:
            for rec in donneesArrosage:
                dataRec=ARROSAGE_DATA()
                dataRec=donneesArrosage[rec]
                dataRec.ArrosageTermine=False 
                dataRec.ArrosageEnCour=False
                donneesArrosage[rec]=dataRec
            sauvegardeMessageActivites(datetime.now(),1-4, "Reset des gicleurs" )
            sleep(1)
            sauvegardeMessageLogs("Systeme arrosage Montreal :" + " gicleurs reset 6 heures")
            DateHeureDebutIntervalle=datetime.now() + timedelta(days=-1)
            reset6Heures=True
            #sleep(3)
        
        ArrosageEcranDataEquipement(socketIpPort.SendRec["ArrosageEcranDataEquipement"].Ip, socketIpPort.SendRec["ArrosageEcranDataEquipement"].Port,**gicleursStatut)
