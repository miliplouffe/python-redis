
import sys, os

# directory="C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\Systemes\\ImportFile"
# directory="G:\\DeveloppementEnvironnement\\Python\\Systemes\\ImportFile"
directory="/home/pi/python"
sys.path.insert(1,directory)
from time import sleep
from json import JSONEncoder
from dataclasses import dataclass
import threading
from datetime import datetime, timedelta
import socket,jsonpickle,pickle
from time import sleep
import socketIpPort
# import fcntl
import struct


# C:\Users\Michel\Documents\DeveloppementEnvironnement\python\systemeArrosage\ArrosageMontreal
# G:\DeveloppementEnvironnement\Python\Systemes\Montreal\Arrosage
#from pymarshaler.marshal import Marshal
# host ligne 240


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


def initializeDonneesGenerales(**donneesArrosage):
    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="1"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="2"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="3"
    donneesGeneralesRec.TempsArrosage=2
    donneesArrosage[donneesGeneralesRec.NoZone]=donneesGeneralesRec

    donneesGeneralesRec=ARROSAGE_DATA()
    donneesGeneralesRec.ArrosageEnCour=False
    donneesGeneralesRec.ArrosageTermine=False
    donneesGeneralesRec.NoZone="4"
    donneesGeneralesRec.TempsArrosage=2
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


def detecteurDataStructure(dectArduino):
    global Detecteurs

    Detecteurs.DectArrosageZone1=int(dectArduino["DectArrosageZone1"])
    Detecteurs.DectArrosageZone2=int(dectArduino["DectArrosageZone2"])
    Detecteurs.DectArrosageZone3=int(dectArduino["DectArrosageZone3"])
    Detecteurs.DectArrosageZone4=int(dectArduino["DectArrosageZone4"])

    return Detecteurs



def sauvegardeMessageLogs(DataLOG):
    print (DataLOG)


def sauvegardeMessageActivites(DateMessage,NoZone,Message):
    
    messageActivite = MESSAGES_ACTIVITES(DateHeureCourante, NoZone, Message)
    messageActivite.DateMessage=DateMessage
    messageActivite.NoZone=NoZone
    messageActivite.Message=Message
    print (messageActivite)
    with open(directory + '/activiteArrosage.data', 'ab+') as fp:
        pickle.dump(messageActivite,fp)
        print("sauvegarde message activite")
        
def recupereRapportActivitesArrosage():

    activites = []
    with open(directory + '/activiteArrosage.data', 'rb') as fr:
        try:
            while True:
                activites.append(pickle.load(fr))
        except EOFError:
            pass
    SendRapportActivitesArrosage(SendRec["RapportActivitesArrosage"].Ip, SendRec["RapportActivitesArrosage"].Port, activites)

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



def lireIpAddress():
    with open(directory+"/ipaddress.data",'r') as data_file:
        for line in data_file:
            data = line.split(';')
            #print(data)

        for x in data:
            y=x.split(',')
            print (y[0], y[1])
            if y[0]=="HostInterface":
                socketIpPort.HostInterface = y[1]
            if y[0]=="HostSystemeArrosage":
                socketIpPort.HostSystemeArrosage = y[1]
            if y[0]=="HostEcranAlarme":
                socketIpPort.HostEcranAlarme = y[1]
            if y[0]=="HostEcranArrosage":
                socketIpPort.HostEcranArrosage = y[1]
            if y[0]=="HostSystemeAlarme":
                socketIpPort.HostSystemeAlarme = y[1]

# socketIpPort.HostInterface = "192.168.1.210"
# socketIpPort.HostSystemeArrosage="192.168.1.227"
# socketIpPort.HostEcranAlarme = "192.168.1.227"
# socketIpPort.HostEcranArrosage = "192.168.1.227"

# lire les adresse pour les connexions reseaux
lireIpAddress()

SendRec=dict()
SendRec = socketIpPort.initIpPort()

DetecteurArduino=""
socArrosageSystemeDataGicleurs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socArrosageSystemeDataGicleurs.bind((SendRec["ArrosageSystemeDataGicleurs"].Ip, SendRec["ArrosageSystemeDataGicleurs"].Port))
def ArrosageSystemeDataGicleurs():
    global DetecteurArduino, socArrosageSystemeDataGicleurs

    while True:
        try:
            print ("ArrosageSystemeDataGicleurs 1 ")
            socArrosageSystemeDataGicleurs.listen()
            print ("ArrosageSystemeDataGicleurs 2 ")
            conn, addr = socArrosageSystemeDataGicleurs.accept()
            # print ("ArrosageSystemeDataGicleurs 3 ",str(addr[0]))
            # SendRec["ArrosageEcranDataEquipement"].Ip = str(addr[0])
            # print ("ArrosageSystemeDataGicleurs 4 ",str(addr[0]))

            with conn:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    else:
                        DetecteurArduino = pickle.loads(data)
                        
        except socket.error as msg:
            print("Socket binding error: " + str(msg) + "\n" + "retrying...ArrosageSystemeDataGicleurs....")   
            socArrosageSystemeDataGicleurs.bind((SendRec["ArrosageSystemeDataGicleurs"].Ip, SendRec["ArrosageSystemeDataGicleurs"].Port))


def ArrosageEcranDataEquipement(HOST, PORT, **gicleursStatut):
    try:
        # recreate the socket and reconnect
        # print ("HOST, PORT", HOST, PORT)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((HOST, PORT))

        data_string = pickle.dumps(gicleursStatut)
        s.send(data_string)
        # print ("ArrosageEcranDataEquipement  ", gicleursStatut["1"].Statut)
        s.close()
        sleep(.2)

    except socket.error as msg:
            print("send ArrosageEcranDataEquipement:: " + str(msg) + "\n" + "retrying....", HOST, PORT)

def InterfaceArduinoAction(HOST, PORT, Requete):

    try:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((HOST, PORT))
        data_string = pickle.dumps(Requete)
        s.send(data_string)
        s.close()
    except socket.error as msg:
            print("send InterfaceArduinoAction: " + str(msg) + "\n" + "retrying...")   

def SendConfigurationsArrosage(HOST, PORT, data):

    try:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((HOST, PORT))
        data_string = pickle.dumps(data)
        # print ("longeur de data  ", len(data_string), HOST,PORT)
        s.send(data_string)
        s.close()
    except socket.error as msg:
            print("SendConfigurationsArrosage : " + str(msg) + "\n" + "retrying...")   

def SendRapportActivitesArrosage(HOST, PORT, data):
    try:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((HOST, PORT))
        data_string = pickle.dumps(data)
        s.send(data_string)
        s.close()
    except socket.error as msg:
            print("SendRapportActivitesArrosage: " + str(msg) + "\n" + "retrying...")   

def SauvegardeConfigurationGeneral():
    global confGeneral

    # open a file, where you ant to store the data
    file = open(directory + '/configurationGeneralArrosage.data', 'wb')

    # dump information to that file
    pickle.dump(confGeneral, file)

    # close the file
    file.close()


def SauvegardeConfigurationGicleurs():
    global gicleurs

    # open a file, where you ant to store the data
    file = open(directory + '/configurationGicleursArrosage.data', 'wb')

    # dump information to that file
    pickle.dump(gicleurs, file)

    # close the file
    file.close()

    return gicleurs
    
def recupereConfigurationGeneral():
    global confGeneral
    # open a file, where you stored the pickled data
    file = open(directory +'/configurationGeneralArrosage.data', 'rb')

    # dump information to that file
    confGeneral = pickle.load(file)

    # close the file
    file.close()
    return confGeneral

def recupereConfigurationGicleurs():
    global gicleurs
    # open a file, where you stored the pickled data
    file = open(directory + '/configurationGicleursArrosage.data', 'rb')

    # dump information to that file
    gicleurs = pickle.load(file)

    # close the file
    file.close()
    return gicleurs

print ("binding 2")

socConfigurationArrosage = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socConfigurationArrosage.bind((SendRec["ConfigurationArrosage"].Ip, SendRec["ConfigurationArrosage"].Port))
def ConfigurationArrosage():
    global socConfigurationArrosage, Equipement, gicleursStatutconfGeneral, gicleurs, confGeneral

    while True:
        try:
            socConfigurationArrosage.listen()
            conn, addr = socConfigurationArrosage.accept()
            with conn:
                while True:
                    data = conn.recv(4096)
                    # print ("len de data", len(data))
                    if not data:
                        break
                    else:
                        if len(data)< 200:
                            confGeneral = pickle.loads(data)
                            SauvegardeConfigurationGeneral()
                        else:
                            gicleurs = pickle.loads(data)
                            SauvegardeConfigurationGicleurs()
        except socket.error as msg:
            print("Socket binding error: " + str(msg) + "\n" + "retrying...ConfigurationArrosage...")  
            socConfigurationArrosage.bind((SendRec["ConfigurationArrosage"].Ip, SendRec["ConfigurationArrosage"].Port))


socGicleursSystemeAction = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socGicleursSystemeAction.bind((SendRec["GicleursSystemeAction"].Ip, SendRec["GicleursSystemeAction"].Port))

def GicleursSystemeAction():
    global  socGicleursSystemeAction, IPAddrLocal, Requete
    global SendRec

    while True:
        try:
            socGicleursSystemeAction.listen()
            conn, addr = socGicleursSystemeAction.accept()

            with conn:
                # SendRec["ArrosageEcranDataEquipement"].Ip = str(addr[0])
                while True:
                    data = conn.recv(4096)
                    # sleep(.25)
                    if not data:
                        break
                    else:
                        Requete = pickle.loads(data)
                    sleep(.25)
        except socket.error as msg:
                print("Socket binding error: " + str(msg) + "\n" + "retrying...GicleursSystemeAction....")
                socGicleursSystemeAction.bind((SendRec["GicleursSystemeAction"].Ip, SendRec["GicleursSystemeAction"].Port))

def FermerGicleurs():
    global donneesArrosage
    for rec in donneesArrosage:
        InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port,gicleurs[rec].ZoneNom+"OFF")
        sleep (2)

def initialiseConfigurationGenerale():
    global GicleurAssocie
    confGeneral=CONFIGURATION_GENERALE()

    confGeneral.ArrosageJourPairImpair="Pair"
    confGeneral.SystemArrosageActif=True
    confGeneral.SondePluieActive=False
    confGeneral.HeureDebutArrosage=10
    confGeneral.NombreJourInterval=1

    return confGeneral


def initialiaseGicleurs(**gicleurs):
    gicleurRec=GICLEURS()
    gicleurRec.NoZone=1
    gicleurRec.ZoneNom="Gicleur_1_"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=1
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Avant près de la rue"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=2
    gicleurRec.ZoneNom="Gicleur_2_"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=2
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Avant près de la maison"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=3
    gicleurRec.ZoneNom="Gicleur_3_"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=2
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="coté de la maison"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=4
    gicleurRec.ZoneNom="Gicleur_4_"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=2
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Arrière de la maison"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    GicleurAssocie={}
    return gicleurs


# hostname=socket.gethostname()  
# SendRec["ArrosageEcranDataEquipement"].Ip=socket.gethostbyname(hostname)  
  
def decodeDataDetecteur(dectArduino, **gicleursStatut):


    recGicleur=GICLEURS_STATUT()

    recGicleur = gicleursStatut["1"]
    recGicleur.Statut = dectArduino.DectArrosageZone1
    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["1"]=recGicleur

    recGicleur = gicleursStatut["2"]
    recGicleur.Statut = dectArduino.DectArrosageZone2
    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["2"]=recGicleur
 
    recGicleur = gicleursStatut["3"]
    recGicleur.Statut = dectArduino.DectArrosageZone3
    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["3"]=recGicleur
 
    recGicleur = gicleursStatut["4"]
    recGicleur.Statut = dectArduino.DectArrosageZone4
    recGicleur.DateHeureCourante = datetime.now()
    gicleursStatut["4"]=recGicleur
 
    return gicleursStatut


Requete=""

confGeneral=dict()
donneesArrosage=dict()
donneesArrosage=initializeDonneesGenerales(**donneesArrosage)
gicleurs=dict()
gicleurEnCour = GICLEUR_EN_COUR()
gicleursStatut=dict()
gicleursStatut = initialiseGicleursStatut()



if __name__ == '__main__':
    global valeurPluie

    DateHeureCourante=datetime.now()
    DateHeureDebutIntervalle=datetime.now() + timedelta(days=-10)
    sauvegardeMessageLogs("Systeme arrosage Montreal :" + "systeme demarre" )



    gicleurs=recupereConfigurationGicleurs()
    confGeneral = recupereConfigurationGeneral()

    # confGeneral=initialiseConfigurationGenerale()
    # SauvegardeConfigurationGeneral()
    # gicleurs = initialiaseGicleurs()
    # SauvegardeConfigurationGicleurs()
# 
    t1 = threading.Thread(target=GicleursSystemeAction)
    t1.start()

    t3=threading.Thread(target=ConfigurationArrosage)
    t3.start()

    t2 = threading.Thread(target=ArrosageSystemeDataGicleurs)
    t2.start()


    FermerGicleurs()
    
    while True :  

        if t2.is_alive==False:
            t2.start()

        if t1.is_alive==False:
            t1.start()
 

        #Detecteurs = detecteurDataStructure(DetecteurArduino)
        gicleursStatut=decodeDataDetecteur(DetecteurArduino, **gicleursStatut)

        if Requete == "NouvelleConfiguration":
            sauvegardeMessageActivites(datetime.now(),"config general et gicleurs", "Changement de configuration")
            InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, "NouvelleConfiguration")
            Requete=""
        elif Requete == "RecupereConfiguration":
            SendConfigurationsArrosage(SendRec["ConfigurationEcranArrosage"].Ip,SendRec["ConfigurationEcranArrosage"].Port, gicleurs)
            sleep(.3)
            SendConfigurationsArrosage(SendRec["ConfigurationEcranArrosage"].Ip,SendRec["ConfigurationEcranArrosage"].Port, confGeneral)
            sleep(.3)
            Requete=""
        elif Requete == "recupereRapportActivitesArrosage":
            recupereRapportActivitesArrosage()
            sleep(.3)
            Requete=""
        elif Requete == "GicleurSet1":
            dataRec=donneesArrosage["1"]
            dataRec.ArrosageTermine=True
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
            Requete=""
        elif Requete == "GicleurReSet1":
            dataRec=donneesArrosage["1"]
            dataRec.ArrosageTermine=False
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
            Requete=""
        elif Requete == "GicleurSet2":
            dataRec=donneesArrosage["2"]
            dataRec.ArrosageTermine=True
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
            Requete=""
        elif Requete == "GicleurReSet2":
            dataRec=donneesArrosage["2"]
            dataRec.ArrosageTermine=False
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
            Requete=""
        elif Requete == "GicleurSet3":
            dataRec=donneesArrosage["3"]
            dataRec.ArrosageTermine=True
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
            Requete=""
        elif Requete == "GicleurReSet3":
            dataRec=donneesArrosage["3"]
            dataRec.ArrosageTermine=False
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
            Requete=""
        elif Requete == "GicleurSet4":
            dataRec=donneesArrosage["4"]
            dataRec.ArrosageTermine=True
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur arrosage termine")
            Requete=""
        elif Requete == "GicleurReSet4":
            dataRec=donneesArrosage["4"]
            dataRec.ArrosageTermine=False
            sauvegardeMessageActivites(datetime.now(),dataRec.NoZone, "Set gicleur près pour arrosage")
            Requete=""
        elif Requete == "Gicleur_1_ON" and ArrosageEnCour==False:
            InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, "Gicleur_1_ON")
            Requete=""
            sauvegardeMessageActivites(datetime.now()," Zone 1 ", "Gicleur_1_ON")
        elif Requete == "Gicleur_1_OFF":
            InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, "Gicleur_1_OFF")
            Requete=""
            sauvegardeMessageActivites(datetime.now()," Zone 1 ", "Gicleur_1_OFF")
        elif Requete == "Gicleur_2_ON" and ArrosageEnCour==False:
            InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, "Gicleur_2_ON")
            Requete=""
            sauvegardeMessageActivites(datetime.now()," Zone 2 ", "Gicleur_2_ON")
        elif Requete == "Gicleur_2_OFF":
            InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, "Gicleur_2_OFF")
            Requete=""
            sauvegardeMessageActivites(datetime.now()," Zone 2 ", "Gicleur_2_OFF")
        elif Requete == "Gicleur_3_ON" and ArrosageEnCour==False:
            InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, "Gicleur_3_ON")
            Requete=""
            sauvegardeMessageActivites(datetime.now()," Zone 3 ", "Gicleur_3_ON")
        elif Requete == "Gicleur_3_OFF":
            InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, "Gicleur_3_OFF")
            Requete=""
            sauvegardeMessageActivites(datetime.now()," Zone 3 ", "Gicleur_3_OFF")
        elif Requete == "Gicleur_4_ON" and ArrosageEnCour==False:
            InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, "Gicleur_4_ON")
            Requete=""
            sauvegardeMessageActivites(datetime.now()," Zone 4 ", "Gicleur_4_ON")
        elif Requete == "Gicleur_4_OFF":
            InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, "Gicleur_4_OFF")
            Requete=""
            sauvegardeMessageActivites(datetime.now()," Zone 4 ", "Gicleur_4_OFF")

 
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
                InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, gicleurs[rec].ZoneNom+"ON")
                sauvegardeMessageActivites(datetime.now(),gicleurEnCour.NoZone, "Arrosage en cours" )
                sleep(1)
                sauvegardeMessageLogs("Systeme arrosage Montreal :" + str(gicleurEnCour.NoZone) + "  Arrosage en cours" )
                donneesArrosage[dataRec.NoZone]=dataRec
                reset6Heures=False
                break
        


            if systemeArrosageEnCour==True and (datetime.now()-gicleurEnCour.HeureDepartArrosage).seconds > 10:
                # if gicleursStatut[str(gicleurEnCour.NoZone)].Statut == 0:
                #      dataRec=ARROSAGE_DATA()
                #      dataRec=donneesArrosage[gicleurEnCour.NoZone]
                #      dataRec.ArrosageTermine=True
                #      dataRec.ArrosageEnCour=False
                #      systemeArrosageEnCour=False
                #      sauvegardeMessageActivites(datetime.now(),gicleurEnCour.NoZone, "L arrosage n a pas lieu. Le detecteur montre 0" )
                #      sleep(1)
                #      sauvegardeMessageLogs("Systeme arrosage Montreal :" + str(gicleurEnCour.NoZone) +"  L arrosage n a pas lieu. Le detecteur montre 0"  )
                #      donneesArrosage[str(gicleurEnCour.NoZone)]=dataRec
# 
                if (datetime.now()-gicleurEnCour.HeureDepartArrosage).seconds/60 >= int(gicleurs[str(gicleurEnCour.NoZone)].TempsArrosage):
                    # arret du gicleur

                    dataRec=ARROSAGE_DATA()
                    dataRec=donneesArrosage[gicleurEnCour.NoZone]
                    dataRec.ArrosageTermine=True
                    dataRec.ArrosageEnCour=False
                    systemeArrosageEnCour=False
                    FermerGicleurs()
                    # InterfaceArduinoAction(SendRec["InterfaceArduinoAction"].Ip,SendRec["InterfaceArduinoAction"].Port, gicleurs[gicleurEnCour.NoZone].ZoneNom+"OFF")
                    sleep(.5)
                    sauvegardeMessageActivites(datetime.now(),gicleurEnCour.NoZone, "Arrosage terminé" )
                    sleep(2)
                    sauvegardeMessageLogs("Systeme arrosage Montreal :" + str(gicleurEnCour.NoZone) +"  Arrosage terminé")

                    donneesArrosage[dataRec.NoZone]=dataRec

        
        if datetime.now().hour == 3 and reset6Heures == False:
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
        # print (" ip a envoyer  ", SendRec["ArrosageEcranDataEquipement"].Ip)
        ArrosageEcranDataEquipement(SendRec["ArrosageEcranDataEquipement"].Ip, SendRec["ArrosageEcranDataEquipement"].Port,**gicleursStatut)
