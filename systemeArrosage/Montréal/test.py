
from time import sleep
from json import JSONEncoder
from dataclasses import dataclass
import threading
from datetime import datetime, timedelta
import socket,jsonpickle,pickle
from time import sleep

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

def SendConfigurationsArrosage(data):

    try:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect(("192.168.1.125", 10015))
        data_string = pickle.dumps(data)
        # print ("longeur de data  ", len(data_string), HOST,PORT)
        s.send(data_string)
        s.close()
    except socket.error as msg:
            print("SendConfigurationsArrosage : " + str(msg) + "\n" + "retrying...")   

if __name__ == '__main__':
        
    gicleurs=initialiaseGicleurs()
    SendConfigurationsArrosage(gicleurs)




