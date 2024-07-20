
import sys, os
import RedisInOut as redisInOut
from dataclasses import dataclass
from time import sleep
from json import JSONEncoder

# from pymarshaler.marshal import Marshal
import threading
from datetime import datetime, timedelta
import sys, os
from enum import Enum

import struct

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
    dureMinutesMouvement           = 2
    dureeSauveFichier              = 1
    heureTestMatin                 = 7
    dureeValideCircuit             = 1
    dureeMessageEnvoyeDropBox      = 5  # minutes
    dureeAlerteElectriciteCourriel = 5  # minutes
    dureeAlarme                    = 5 # minutes
    gpioAlarme                     = 19 # alarme
    dureeuploadToScreen            = 1  # nb de seconde pour envoyer a l ecran
    HIGH                           = 1
    LOW                            = 0
    nombreCourrielQuotidien        = 5

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
Requete=""
NoZone=0
Statut=0
Action=0

@dataclass
class DETECTEUR:
    Prop: float = 0.0
    Co: float = 0.0
    Fumee: float = 0.0
    Mouvement: float = 0.0
    EauElectrique: float = 0.0
    EauTraitement: float = 0.0
    PanneElectrique: float = 0.0


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
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte une fuite de propane")
    NomEquipement = "Co"
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte une fuite de CO")
    NomEquipement = "Fumee"
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme de la fumee")
    NomEquipement = "Mouvement"
    Armer = False
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte du mouvement dans le sous-sol")
    NomEquipement = "EauElectrique"
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte de l eau dans la salle electrique")
    NomEquipement = "EauTraitement"
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte de l eau dans la salle de traitement de l eau")
    NomEquipement = "PanneElectrique"
    Armer = True
    Actif = True
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte une panne electrique exterieure")
    NomEquipement = "EauPluie"
    Armer = False
    Actif = False
    Equipement[NomEquipement] = defineEquipementsVariables(NomEquipement, Actif, Armer, "Le systeme detecte la pluie")
     
    return Equipement

# def decodeDataDetecteur(detecteur, **Equipement):
# 
#     recEquipement=EQUIPEMENT()
# 
#     recEquipement = Equipement["Prop"]
#     recEquipement.Valeur = detecteur.Prop
#     recEquipement.DateHeureCourante = datetime.now()
#  
#     recEquipement = Equipement["Co"]
#     recEquipement.Valeur = detecteur.Co
#     recEquipement.DateHeureCourante = datetime.now()
#  
#     recEquipement = Equipement["Fumee"]
#     recEquipement.Valeur = detecteur.Fumee
#     recEquipement.DateHeureCourante = datetime.now()
#  
def decodeDataDetecteur(detecteur, **Equipement):

    recEquipement=EQUIPEMENT()

    recEquipement = Equipement["Prop"]
    recEquipement.Valeur = detecteur.Prop
    recEquipement.DateHeureCourante = datetime.now()
    Equipement["Prop"]=recEquipement

    recEquipement = Equipement["Co"]
    recEquipement.Valeur = detecteur.Co
    recEquipement.DateHeureCourante = datetime.now()
    Equipement["Co"]=recEquipement
 
    recEquipement = Equipement["Fumee"]
    recEquipement.Valeur = detecteur.Fumee
    recEquipement.DateHeureCourante = datetime.now()
    Equipement["Fumee"]=recEquipement
 
    recEquipement = Equipement["Mouvement"]
    recEquipement.Valeur = detecteur.Mouvement
    recEquipement.DateHeureCourante = datetime.now()
    Equipement["Mouvement"]=recEquipement
 
    recEquipement = Equipement["EauElectrique"]
    recEquipement.Valeur = detecteur.EauElectrique
    recEquipement.DateHeureCourante = datetime.now()
    Equipement["EauElectrique"]=recEquipement

    recEquipement = Equipement["EauTraitement"]
    recEquipement.Valeur = detecteur.EauTraitement
    recEquipement.DateHeureCourante = datetime.now()
    Equipement["EauTraitement"]=recEquipement

    recEquipement = Equipement["PanneElectrique"]
    if detecteur.PanneElectrique > 995:
        recEquipement.Valeur = 0
    else:
        recEquipement.Valeur = 1

    recEquipement.DateHeureCourante = datetime.now()
    Equipement["PanneElectrique"]=recEquipement


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
                    leSujet = "Maison de Wentworth-Nord"
                    message =rec.MessageErreur
                    dateHeureAlarme=datetime.now()
                else:
                    rec.Alarme = False
            else:
                #  and rec.NomEquipement.find("Arrosage")==-1
                if (rec.NomEquipement in zoneList and rec.Valeur == 1 and rec.Armer == True):
                    alarmeErreur = True
                    rec.Alarme = True
                    leSujet = "Maison de Wentworth-Nord"
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
            leSujet = "Maison de Wentworth-Nord"
            message = "le systeme est revenue à la normal"
            sendMail(leSujet, message)
            # ecrisMessageAlerte(date + "," + leSujet + "," + message)
            systemeAlarme = False
            courrielEnvoye = False
            ## ecrireAlarmeFichier(Equipements)
            # ser.write(b'AlarmeSonore_OFF')
            # go AvertisseurAlarme.Demarrer(AlarmeSonore_OFF)
    except Exception as ex:
        ii=ex
        # print(ex)

    return systemeArmer,heureCourrielEnvoye,courrielEnvoye,systemeAlarme,dateHeureAlarme,alarmeErreur,Equipement

def valideDetecteurArmerSystemePartiel(**Equipements):
    resultat=False
    
    if Equipements["Mouvement"].Valeur == 0: 
        resultat = False
    else:
        resultat = True

    Requete=""
    return resultat


def assigneStatutArmerPartiel(**Equipement):

    for i in Equipement:
        equipementRec=EQUIPEMENT()
        equipementRec=Equipement[i]
        # and equipementRec.NomEquipement not in zoneList
        if equipementRec.Actif==True  :
            if equipementRec.NomEquipement == "Mouvement" :
                equipementRec.Armer = True
        else:
            equipementRec.Valeur=2
            equipementRec.Armer = False
            
    return Equipement


def valideDetecteurArmerSystemeComplet(**Equipements):
    global zoneList
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
    redisInOut.RequeteAlarme=""
    Requete=""

    return resultat

def assigneStatutArmerComplet(**Equipement):
    global zoneList
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
        if equipementRec.NomEquipement == "Prop" or equipementRec.NomEquipement == "Co" or equipementRec.NomEquipement == "Fumee" or equipementRec.NomEquipement == "EauElectrique"  or equipementRec.NomEquipement == "EauTraitement"  or equipementRec.NomEquipement == "PanneElectrique":
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

        Equipement[i]=equipementRec

    return Equipement
    

def sendMail(SUBJECT,TEXT):
    global CourrielValeur
    import smtplib

    gmail_user = 'miliplouffe@gmail.com'
    gmail_password = 'pifewpnxrytkljxv'

    sent_from = gmail_user
    to = ['miliplouffe@outlook.com']
    subject = SUBJECT
    body = TEXT


    email_text = """
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



def sauvegardeMessageActivites(Message):
    print ("En construction")


def publishEcranErreur(action):
    print ("En construction")

def recupereCourrielStatut():
    print ("En construction")

def sauvegardeMessageActivites(DataLOG):
    print ("En construction")

def sendSystemeAlarmeEquipement():
    global Equipement
    while True:
        redisInOut.publishSystemeAlarmeEquipement(Equipement)
        sleep(.2)   #Open port with baud rate

# CourrielValeur=recupereCourrielStatut()

zoneList.append("Prop")
zoneList.append("Co")
zoneList.append("Fumee")
zoneList.append("EauElectrique")
zoneList.append("EauTraitement")
zoneList.append("PanneElectrique")


if __name__ == '__main__':

    t1 = threading.Thread(target=sendSystemeAlarmeEquipement)
    t1.start()
    CourrielValeur="courrielActif"
    courriel7Heures = False

    # datetime object containing current date and time
    currentTime = datetime.now()
    dateHeureUpLoadScreen = datetime.now()
    dateHeureDemarreApps = datetime.now()
    dateHeureValideCircuit=datetime.now()
    dateHeureAlarme=datetime.now()
    sendMail("Systeme alarme Wentworth-Nord","Le systeme d alarme a redemarre")
    Detecteur = DETECTEUR()
    Equipement = dict()
    Equipement = initialiseVariables(**Equipement)

    alarmeErreur = False
    systemeArmer = False
    heureCourrielEnvoye=datetime.now()
    courrielEnvoye = False
    DateHeureCourante=datetime.now()
    systemeAlarme=False
    activeCompletTest="non"
    detecteursRec=DETECTEUR()
    # marshal = Marshal()
    mustSendToClient=False
    systemeAlarmeSatut=""

    readAllData=True
    redisInOut.StartArduinoDetecteurs()   
    redisInOut.StartSystemeAlarmeRequete()

    redisInOut.sauvegardeSystemeAlarme(**Equipement)

    while True:
        Requete=redisInOut.getRequeteAlarme()
        redisInOut.RunRedisInOut("StartSystemeAlarmeRequete")   # check if task is running
####        redisInOut.RunRedisInOut("StartArduinoDetecteurs")    # check if task is running

        readAllData=True
        if readAllData==True:
            try:
                Detecteur=redisInOut.getArduinoDetecteur()
                Equipement = decodeDataDetecteur(Detecteur, **Equipement)
                Equipement = changeValeursPinsArmer(**Equipement)
                redisInOut.publishSystemeAlarmeEquipement(Equipement)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
                # print(exc_type, fname, exc_tb.tb_lineno)

        else:
            sleep(.1)

        readAllData=True 
 
        if Requete == str("ActivationPartielle") and valideDetecteurArmerSystemePartiel(**Equipement) == True:
            Equipement = assigneStatutArmerPartiel(**Equipement)
            systemeArmer = True
            mustSendToClient = True
            systemeAlarmeSatut = "ActivationPartielle"
            # sendSystemeAlarmeDataEquipement(SendRec["AlarmeEcranDataEquipement"].Ip, SendRec["AlarmeEcranDataEquipement"].Port,**Equipement)
            sleep(0.5)
            readAllData=False
            sendMail("Systeme alarme Wentworth-Nord","Le systeme d alarme est active partiellement")
            redisInOut.Requete = ""
            Requete=""
            redisInOut.RequeteAlarme=""


        if Requete == "ActivationComplete" and valideDetecteurArmerSystemeComplet(**Equipement) == True:
            # print(" activation est complete  ")
            Equipement = assigneStatutArmerComplet(**Equipement)
            sauvegardeMessageActivites("valideDetecteurArmerSystemeComplet est OK")
            sleep(15)
            systemeArmer = True
            mustSendToClient = True
            systemeAlarmeSatut = "ActivationComplete"
            #writeModeActuelAlarmeFile("Activation complete")
            # sendSystemeAlarmeDataEquipement(SendRec["AlarmeEcranDataEquipement"].Ip, SendRec["AlarmeEcranDataEquipement"].Port,**Equipement)
            sauvegardeMessageActivites(systemeAlarmeSatut)
            sleep(0.5)
            redisInOut.RequeteAlarme=""
            Requete=""
            readAllData=False
            #activeCompletTest = ""
            sendMail("Systeme alarme Wentworth-Nord","Le systeme d alarme est active completement")

        if Requete == "Desactivation":
            print(" desactivation ")
            Equipement = valideDetecteurDesactivation(**Equipement)
            redisInOut.RequeteAlarme=""
            Requete=""
            mustSendToClient = True
            systemeArmer = False
            courrielEnvoye = False
            systemeAlarmeSatut = "Desactivation"
            # sendSystemeAlarmeDataEquipement(SendRec["AlarmeEcranDataEquipement"].Ip, SendRec["AlarmeEcranDataEquipement"].Port,**Equipement)
            sleep(0.5)
            # ser.write(b'AlarmeSonore_OFF')
            readAllData=False
            # go AvertisseurAlarme.Demarrer(AlarmeSonore_OFF)
            # writeModeActuelAlarmeFile("Desactivation")
            sendMail("Systeme alarme Wentworth-Nord","Le systeme d alarme est desactive")
            

        if Requete == "shutdown":
            print("shutdown")
            os.system('sudo shutdown now')
            #cmd := exec.Command("shutdown", "/sbin")
            #cmd.Run()
            #Requete = ""
        if Requete == "Redemarrer":
            print("shutdown")
            redisInOut.Requete=""
            os.system('sudo reboot now')

        
        if Requete == "courrielActif":
            CourrielValeur="courrielActif"
            redisInOut.Requete=""
            Requete=""
            redisInOut.RequeteAlarme=""
        if Requete == "courrielInactif":
            CourrielValeur="courrielInactif"
            redisInOut.Requete=""
            Requete=""
            redisInOut.RequeteAlarme=""

        

        if courriel7Heures == False and const.heureTestMatin== datetime.now().hour:
            courriel7Heures=True
            if alarmeErreur==False:
                message="Le systeme n'est pas en erreur"
                print (alarmeErreur)
            else:
                message="Le systeme est en erreur"
            sendMail("Systeme alarme Wentworth-Nord",message)
        elif datetime.now().hour > 8:
            courriel7Heures=False


                    
        difference = datetime.now()-dateHeureValideCircuit

        if (difference.total_seconds() >= const.dureeValideCircuit):
            systemeArmer,heureCourrielEnvoye,courrielEnvoye,systemeAlarme,dateHeureAlarme,alarmeErreur,Equipement = verifieErreurs(systemeArmer,heureCourrielEnvoye,courrielEnvoye,systemeAlarme,dateHeureAlarme,alarmeErreur,**Equipement)
            dateHeureValideCircuit= datetime.now()
                


                




