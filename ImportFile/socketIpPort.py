# import pour assigner les adresses ip et ports
# pour le systeme d alarme et le systeme d arrosage
from dataclasses import dataclass

HostInterface = ""
HostSystemeArrosage=""
HostSystemeAlarme=""
HostEcranAlarme = ""
HostEcranArrosage = ""

@dataclass
class SOCKET_ACCESS:
    Nom: str=""
    Ip: str =""
    Port: int = ""


def initIpPort():
    global HostInterface,HostSystemeArrosage, HostEcranAlarme, HostEcranArrosage, HostSystemeAlarme

    adresse = SOCKET_ACCESS()
    adresse.Nom="InterfaceArduinoDataEquipement"
    adresse.Ip=HostInterface
    adresse.Port=10000
    SendRec["InterfaceArduinoDataEquipement"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="AlarmeEcranDataEquipement"
    adresse.Ip=HostEcranAlarme
    adresse.Port=10001
    SendRec["AlarmeEcranDataEquipement"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="AlarmeSystemeDataEquipement"
    adresse.Ip= HostSystemeAlarme
    adresse.Port=10002
    SendRec["AlarmeSystemeDataEquipement"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="ArrosageSystemeDataGicleurs"
    adresse.Ip= HostSystemeArrosage
    adresse.Port=10003
    SendRec["ArrosageSystemeDataGicleurs"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="InterfaceArduinoAction"
    adresse.Ip=HostInterface
    adresse.Port=10004
    SendRec["InterfaceArduinoAction"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="AlarmeSystemeAction"
    adresse.Ip=HostSystemeAlarme
    adresse.Port=10005
    SendRec["AlarmeSystemeAction"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="GicleursSystemeAction"
    adresse.Ip=HostSystemeArrosage
    adresse.Port=10006
    SendRec["GicleursSystemeAction"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="ArrosageEcranDataEquipement"
    adresse.Ip=HostEcranArrosage
    adresse.Port=10007
    SendRec["ArrosageEcranDataEquipement"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="ConfigurationArrosage"
    adresse.Ip=HostSystemeArrosage
    adresse.Port=10008
    SendRec["ConfigurationArrosage"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="ConfigurationAlarme"
    adresse.Ip=HostSystemeAlarme
    adresse.Port=10009
    SendRec["ConfigurationAlarme"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="ConfigurationEcranArrosage"
    adresse.Ip=HostEcranArrosage
    adresse.Port=10010
    SendRec["ConfigurationEcranArrosage"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="ConfigurationEcranAlarme"
    adresse.Ip=HostEcranArrosage
    adresse.Port=10011
    SendRec["ConfigurationEcranAlarme"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="RapportActivitesArrosage"
    adresse.Ip=HostEcranArrosage
    adresse.Port=10012
    SendRec["RapportActivitesArrosage"]=adresse

    adresse = SOCKET_ACCESS()
    adresse.Nom="RapportActivitesAlarme"
    adresse.Ip=HostEcranArrosage
    adresse.Port=10013
    SendRec["RapportActivitesAlarme"]=adresse   

    adresse = SOCKET_ACCESS()
    adresse.Nom="ArrosageSystemeDataGicleursWeb"
    adresse.Ip=HostSystemeArrosage
    adresse.Port=10015
    SendRec["ArrosageSystemeDataGicleursWeb"]=adresse  

    return SendRec



SendRec=dict()
SendRec = initIpPort()