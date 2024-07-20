from flask import Flask
from flask import request
from flask import render_template, redirect, url_for
import os
from time import sleep
import redis
import jsonpickle
import threading
import time
import os,sys
from functools import partial
import pickle
import socket
import socketIpPort
from dataclasses import dataclass

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

directory="C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\Systemes\\ImportFile"
directoryHtml="C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\Systemes\\systemeArrosageWeb"
# directory="/home/pi/python"
sys.path.insert(1, directory)

@dataclass
class dataWeb:
 
	NoZone0: str
	ZoneActive0: str
	DetecteurUtilise0: str
	TempsArrosage0: str
	ValeurHumidite0: str
	StatutArrosage0: str
	NoZone1: str
	ZoneActive1: str
	DetecteurUtilise1: str
	TempsArrosage1: str
	ValeurHumidite1: str
	StatutArrosage1: str
	NoZone2: str
	ZoneActive2: str
	DetecteurUtilise2: str
	TempsArrosage2: str
	ValeurHumidite2: str
	StatutArrosage2: str
	NoZone3: str
	ZoneActive3: str
	DetecteurUtilise3: str
	TempsArrosage3: str
	ValeurHumidite3: str
	StatutArrosage3: str
	NoZone4: str
	ZoneActive4: str
	DetecteurUtilise4: str
	TempsArrosage4: str
	ValeurHumidite4: str
	StatutArrosage4: str


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
class GICLEURS_STATUT:  
    NoZone: int = 0
    Statut: bool = False
    Action: str = ""

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


NoZone=0
ZoneNom=""
TempsArrosage=False
ArrosageEnCour=False
ArrosageTermine=False
systemeArrosageEnCour=False
ZoneActive=False
ZonePhysique=""
Affichage=False
AffichageWeb=False
MessageErreur=""
Statut=0
Action=0
Host = "192.168.1.210"
HeureDebutArrosage=0
SystemArrosageActif=False
SondePluieActive=False
ArrosageJourPairImpair="Impair"
NombreJourInterval=2
ZoneArrosageMaintenant=0

code="25631"
valideCode=False
construitCode=""
requete=""

confGeneral=dict()
gicleurs=dict()
gicleursStatut=dict()


def initialiseConfigurationGenerale():
    global GicleurAssocie
    confGeneral=CONFIGURATION_GENERALE()

    confGeneral.ArrosageJourPairImpair="Pair"
    confGeneral.SystemArrosageActif=True
    confGeneral.SondePluieActive=False
    confGeneral.HeureDebutArrosage=16
    confGeneral.NombreJourInterval=2

    return confGeneral

    

def initialiseGicleursStatut():
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

    return GicleursStatut

def initialiseConfigurationGenerale():
    global GicleurAssocie
    confGeneral=CONFIGURATION_GENERALE()

    confGeneral.ArrosageJourPairImpair="Pair"
    confGeneral.SystemArrosageActif=False
    confGeneral.SondePluieActive=False
    confGeneral.HeureDebutArrosage=16
    confGeneral.NombreJourInterval=2

    return confGeneral


def initialiaseGicleurs(**gicleurs):
    gicleurRec=GICLEURS()
    gicleurRec.NoZone=1
    gicleurRec.ZoneNom="Gicleur_1_"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=60
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Avant près de la rue"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=2
    gicleurRec.ZoneNom="Gicleur_2_"
    gicleurRec.ZoneActive=False
    gicleurRec.TempsArrosage=60
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Avant près de la maison"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=3
    gicleurRec.ZoneNom="Gicleur_3_"
    gicleurRec.ZoneActive=False
    gicleurRec.TempsArrosage=60
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="coté de la maison"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=4
    gicleurRec.ZoneNom="Gicleur_4_"
    gicleurRec.ZoneActive=False
    gicleurRec.TempsArrosage=60
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Arrière de la maison"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    GicleurAssocie={}
    return gicleurs


@dataclass
class SOCKET_ACCESS:
    Nom: str=""
    Ip: str =""
    Port: int = ""


def copieDataPourWeb():
    global gicleursStatut



def sauvegardeMessageActivites(DateMessage,NoZone,Message):
    print ("sauvegarde a coder ")


def lireIpAddress():
    with open(directory + "/ipaddress.data",'r') as data_file:
        for line in data_file:
            data = line.split(';')

        for x in data:
            y=x.split(',')
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

# lire les adresse pour les connexions reseaux
lireIpAddress()

SendRec=dict()
SendRec = socketIpPort.initIpPort()

socConfigurationArrosage = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socConfigurationArrosage.bind((SendRec["ConfigurationEcranArrosage"].Ip, SendRec["ConfigurationEcranArrosage"].Port))

def ConfigurationArrosage():
    global socConfigurationArrosage, Equipement, gicleursStatut, gicleurs, confGeneral, Refresh


    while True:
        try:
            socConfigurationArrosage.listen()
            conn, addr = socConfigurationArrosage.accept()
            with conn:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    else:
                        if len(data)>400:
                            gicleurs = pickle.loads(data)
                            Refresh=True
                        else:
                            confGeneral = pickle.loads(data)
                            Refresh=True
        
        except socket.error as msg:
            print("Socket binding error: " + str(msg) + "\n" + "retrying...")
            socConfigurationArrosage.bind((SendRec["ConfigurationEcranArrosage"].Ip, SendRec["ConfigurationEcranArrosage"].Port))


socArrosageSystemeDataGicleurs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socArrosageSystemeDataGicleurs.bind((SendRec["ArrosageEcranDataEquipement"].Ip, SendRec["ArrosageEcranDataEquipement"].Port))
def ArrosageSystemeDataGicleurs():
    global socArrosageSystemeDataGicleurs
    global hostClient, EquipementInterface, gicleursStatut

    while True:
        try:
            socArrosageSystemeDataGicleurs.listen()
            conn, addr = socArrosageSystemeDataGicleurs.accept()
            with conn:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break
                    else:
                        gicleursStatut = pickle.loads(data)
        except socket.error as msg:
                print("Socket binding error: " + str(msg) + "\n" + "retrying...")
                socArrosageSystemeDataGicleurs.bind((SendRec["ArrosageEcranDataEquipement"].Ip, SendRec["ArrosageEcranDataEquipement"].Port))


def GicleursSystemeAction(HOST, PORT, Requete):
    global s
    try:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((HOST, PORT))
        data_string = pickle.dumps(Requete)
        s.send(data_string)
        s.close()
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "retrying...") 


gicleursStatut= initialiseGicleursStatut()

t1 = threading.Thread(target=ArrosageSystemeDataGicleurs)
t1.start()

t2 = threading.Thread(target=ConfigurationArrosage)
t2.start()

# t3 = threading.Thread(target=RapportActivitesArrosage)
# t3.start()

# sleep(1)
# GicleursSystemeAction(SendRec["GicleursSystemeAction"].Ip, SendRec["GicleursSystemeAction"].Port, "RecupereConfiguration")
# sleep(1)
# confGeneral= initialiseConfigurationGenerale()
# gicleurs=initialiaseGicleurs()

# print (confGeneral.ArrosageJourPairImpair)

# template_dir = os.path.abspath("C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\Systemes\\systemeArrosageWeb")
# template_dir = os.path.abspath("/home/pi/python")
# app = Flask(__name__, template_folder=directoryHtml)

dateHeure=""
endroit=""
message=""

gileurStatut = {}
app = Flask(__name__, template_folder=directoryHtml)


@app.route("/action", methods=['GET', 'POST'])
def contact():
    global gicleursStatut

    if "Raffraichir la page" in str(request.form):
        GicleursSystemeAction(SendRec["GicleursSystemeAction"].Ip, SendRec["GicleursSystemeAction"].Port, "1")
        time.sleep(1)
        return render_template('arrosageWeb.html', data=gicleursStatut)
        pass

    if "shutdown" in str(request.form):
        # publishActionPourWebEtEcran("shutdown")
        pass

    if "Redemarrer" in str(request.form):
        # publishActionPourWebEtEcran("Redemarrer")
        pass

    if "Rapports" in str(request.form):
        # publishActionPourWebEtEcran("Rapports")
        return render_template('arrosageWeb.html',data=gileurStatut)
        pass
    
    if "Page précédente" in str(request.form):
        # publishActionPourWebEtEcran("1")
        time.sleep(1)
        return render_template('arrosageWeb.html',data=gileurStatut)
        pass

    return render_template('arrosageWeb.html',data=gileurStatut)

@app.route('/')
def show_index():
    return render_template('arrosageWeb.html',data=gileurStatut)

# @app.route('/')
# def show_DonneesCummulatives():
#     return render_template('DonneesCummulatives.html',data1=DataCummulatif)
# 

if __name__ == '__main__':
    print ("allo")
    app.run(host='0.0.0.0', debug=False, port=8100)

    # t = threading.Thread(target=ArrosageSystemeDataGicleurs)
    # t.daemon = True
    # t.start()
