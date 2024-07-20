
import sys, os
# sys.path.insert(1, "C:\\Users\\Michel\\Documents\\DeveloppementEnvironnement\\python\\importFile")
sys.path.insert(1, "/home/pi/python")
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtCore  import *
from dataclasses import dataclass
import threading
import time
from datetime import datetime, timedelta
import traceback, sys
import redis
from dialog import Ui_MainWindow
from functools import partial
import pickle, socket, jsonpickle
import socket
import socketIpPort

# C:\Users\Michel\Documents\DeveloppementEnvironnement\python\systemeArrosage\ArrosageMontreal

Refresh=False

format = "02-01-2006 15:04:05"

class const:
    gicleurData             = "GicleurData"
    confGeneralData         = "ConfGeneralData"
    publishDataChange       = "GicleurConfigurationChange"
    publishArrosage          = "arrosageMontreal"
    publishArrosageData      = "arrosageGicleursMontreal"
    clefMessage              = "MessageClef"


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
Host = "192.168.1.240"
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

Host = "192.168.1.142"
HostEcranAlarme = "192.168.1.240"
HostEcranArrosage = "192.168.1.240"

confGeneral=dict()
gicleurs=dict()
gicleursStatut=dict()


class WorkerSignals(QObject):
  

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):

 
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    #@Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        # Retrieve args/kwargs here; and fire processing using them

        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done




class MainWindow(QMainWindow):
    
    def __init__(self):
        global code
        global construitCode
        global DataFromRedis
        global Refresh

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.ui.Sauvegarde.clicked.connect(partial(self.clicked_btn_action, "Sauvegarde"))
        self.ui.Reinitialiser.clicked.connect(partial(self.clicked_btn_action, "Reinitialiser"))
        self.ui.OuvrirMessage.clicked.connect(partial(self.clicked_btn_action, "OuvrirMessages"))
        self.ui.FermerMessage.clicked.connect(partial(self.clicked_btn_action, "FermerMessages"))
       

        self.ui.OuvMan1.clicked.connect(partial(self.clicked_btn_Gicleurs, "OuvMan1"))
        self.ui.FermMan1.clicked.connect(partial(self.clicked_btn_Gicleurs, "FermMan1"))
        self.ui.OuvMan2.clicked.connect(partial(self.clicked_btn_Gicleurs, "OuvMan2"))
        self.ui.FermMan2.clicked.connect(partial(self.clicked_btn_Gicleurs, "FermMan2"))
        self.ui.OuvMan3.clicked.connect(partial(self.clicked_btn_Gicleurs, "OuvMan3"))
        self.ui.FermMan3.clicked.connect(partial(self.clicked_btn_Gicleurs, "FermMan3"))
        self.ui.OuvMan4.clicked.connect(partial(self.clicked_btn_Gicleurs, "OuvMan4"))
        self.ui.FermMan4.clicked.connect(partial(self.clicked_btn_Gicleurs, "FermMan4"))
    
        self.ui.GicleurSet1.clicked.connect(partial(self.clicked_btn_Gicleurs, "GicleurSet1"))
        self.ui.GicleurReSet1.clicked.connect(partial(self.clicked_btn_Gicleurs, "GicleurReSet1"))
        self.ui.GicleurSet2.clicked.connect(partial(self.clicked_btn_Gicleurs, "GicleurSet2"))
        self.ui.GicleurReSet2.clicked.connect(partial(self.clicked_btn_Gicleurs, "GicleurReSet2"))
        self.ui.GicleurSet3.clicked.connect(partial(self.clicked_btn_Gicleurs, "GicleurSet3"))
        self.ui.GicleurReSet3.clicked.connect(partial(self.clicked_btn_Gicleurs, "GicleurReSet3"))
        self.ui.GicleurSet4.clicked.connect(partial(self.clicked_btn_Gicleurs, "GicleurSet4"))
        self.ui.GicleurReSet4.clicked.connect(partial(self.clicked_btn_Gicleurs, "GicleurReSet4"))
 
        self.ui.Logs.setVisible(False)

        global gicleurs
        global confGeneral
        global requete

        Refresh=True

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()


    def clicked_btn_Gicleurs(self, value):
        global construitCode
        global valideCode
        global gicleursStatut
        gicleurNO=""

        valide=True

        for recGicleurs in gicleursStatut:
            if gicleursStatut[recGicleurs].Statut==1:
                ZoneArrosageMaintenant=recGicleurs
                valide=False

        if value=="OuvMan1" and valide == True:
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port, gicleurs["1"].ZoneNom+"ON")
            sauvegardeMessageActivites(datetime.now(), "1", "Ouverture manuelle gicleur")

        if value=="FermMan1":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port, gicleurs["1"].ZoneNom+"OFF")
            sauvegardeMessageActivites(datetime.now(), "1", "Fermeture manuelle gicleur")

        if value=="OuvMan2" and valide == True:
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port, gicleurs["3"].ZoneNom+"ON")
            sauvegardeMessageActivites(datetime.now(), "2", "Ouverture manuelle gicleur")

        if value=="FermMan2":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port, gicleurs["2"].ZoneNom+"OFF")
            sauvegardeMessageActivites(datetime.now(), "2", "Fermeture manuelle gicleur")

        if value=="OuvMan3" and valide == True:
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port, gicleurs["3"].ZoneNom+"ON")
            sauvegardeMessageActivites(datetime.now(), "3", "Ouverture manuelle gicleur")

        if value=="FermMan3":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port, gicleurs["3"].ZoneNom+"OFF")
            sauvegardeMessageActivites(datetime.now(), "3", "Fermeture manuelle gicleur")

        if value=="OuvMan4" and valide == True:
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port, gicleurs["4"].ZoneNom+"ON")
            sauvegardeMessageActivites(datetime.now(), "4", "Ouverture manuelle gicleur")

        if value=="FermMan4":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port, gicleurs["4"].ZoneNom+"OFF")
            sauvegardeMessageActivites(datetime.now(), "4", "Fermeture manuelle gicleur")


        if value=="GicleurSet1":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port, "GicleurSet1")
            sauvegardeMessageActivites(datetime.now(), "1", "Set gicleur arrosage complété")

        if value=="GicleurReSet1":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port,  "GicleurReSet1")
            sauvegardeMessageActivites(datetime.now(), "1", "Set gicleur arrosage non fait")

        if value=="GicleurSet2":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port,  "GicleurSet2")
            sauvegardeMessageActivites(datetime.now(), "2", "Set gicleur arrosage complété")

        if value=="GicleurReSet2":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port,  "GicleurReSet2")
            sauvegardeMessageActivites(datetime.now(), "2", "Set gicleur arrosage non fait")

        if value=="GicleurSet3":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port,  "GicleurSet3")
            sauvegardeMessageActivites(datetime.now(), "3", "Set gicleur arrosage complété")

        if value=="GicleurReSet3":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port,  "GicleurReSet3")
            sauvegardeMessageActivites(datetime.now(), "3", "Set gicleur arrosage non fait")

        if value=="GicleurSet4":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port,  "GicleurSet4")
            sauvegardeMessageActivites(datetime.now(), "4", "Set gicleur arrosage complété")

        if value=="GicleurReSet4":
            GicleursSystemeAction(socketIpPort.SendRec["GicleursSystemeAction"].Ip, socketIpPort.SendRec["GicleursSystemeAction"].Port,  "GicleurReSet4")
            sauvegardeMessageActivites(datetime.now(), "4", "Set gicleur arrosage non fait")


        sender = self.sender()


    def clicked_btn_action(self, value):
        global valideCode
        global confGeneral
        global gicleurs
        global Refresh

        if value=="OuvrirMessages":
            longeur=redisClient.llen(const.clefMessage)
            tableData=redisClient.lrange  (const.clefMessage, 0, longeur)
            
            header = self.ui.Logs.horizontalHeader()       
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
 


            #self.ui.Logs.setColumnWidth(0, 150)
            #self.ui.Logs.setColumnWidth(1, 150)
            #self.ui.Logs.setColumnWidth(2, 400)

            self.ui.Logs.setRowCount(0)

            for ligne in tableData:
                rowPosition = self.ui.Logs.rowCount()
                self.ui.Logs.insertRow(rowPosition)
                    
                data = ligne.split(",")
                self.ui.Logs.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(data[0])))
                self.ui.Logs.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(str(data[1])))
                self.ui.Logs.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(str(data[2])))


            self.ui.Logs.update()
            self.ui.Logs.setVisible(True)
        

        if value=="FermerMessages":
            self.ui.Logs.setVisible(False)

        if value=="Sauvegarde":
            confGeneral=CONFIGURATION_GENERALE()
            confGeneral.SystemArrosageActif=self.ui.ArrosageActif.isChecked()
            confGeneral.SondePluieActive=self.ui.DetecteurPluieActif.isChecked()
            confGeneral.HeureDebutArrosage=self.ui.HeureArrosage.value()
            confGeneral.ArrosageJourPairImpair=self.ui.JourArrosage.currentText()
            confGeneral.NombreJourInterval=self.ui.IntervalEntreArrosage.value()

            # recGicleur=GICLEURS()
    
            recGicleur=gicleurs["1"]
            recGicleur.NoZone=self.ui.NoZone1.text()
            recGicleur.ZoneActive=self.ui.Zone1Active.isChecked()
            recGicleur.TempsArrosage=self.ui.Zone1TempsArrosage.text()
            recGicleur.ZonePhysique=self.ui.Zone1Physique.toPlainText()
            gicleurs[recGicleur.NoZone]=recGicleur

            recGicleur=GICLEURS()
            recGicleur=gicleurs["2"]
            recGicleur.NoZone=self.ui.NoZone2.text()
            recGicleur.ZoneActive=self.ui.Zone2Active.isChecked()
            recGicleur.TempsArrosage=self.ui.Zone2TempsArrosage.text()
            recGicleur.ZonePhysique=self.ui.Zone2Physique.toPlainText()
            gicleurs[recGicleur.NoZone]=recGicleur

            recGicleur=GICLEURS()
            recGicleur=gicleurs["3"]
            recGicleur.NoZone=self.ui.NoZone3.text()
            recGicleur.ZoneActive=self.ui.Zone3Active.isChecked()
            recGicleur.TempsArrosage=self.ui.Zone3TempsArrosage.text()
            recGicleur.ZonePhysique=self.ui.Zone3Physique.toPlainText()
            gicleurs[recGicleur.NoZone]=recGicleur

            recGicleur=GICLEURS()
            recGicleur=gicleurs["4"]
            recGicleur.NoZone=self.ui.NoZone4.text()
            recGicleur.ZoneActive=self.ui.Zone4Active.isChecked()
            recGicleur.TempsArrosage=self.ui.Zone4TempsArrosage.text()
            recGicleur.ZonePhysique=self.ui.Zone4Physique.toPlainText()
            gicleurs[recGicleur.NoZone]=recGicleur

            publishDataPourArrosage(const.publishArrosageData, "NouvelleConfiguration")
            sauvegardeConfigurationGeneralGicleurs()
    
            Refresh=True

        if value=="Reinitialiser":
            confGeneral=initialiseConfigurationGenerale()
            gicleurs=initialiaseGicleurs()
            sauvegardeConfigurationGeneralGicleurs()
            publishDataPourArrosage(const.publishArrosageData,"NouvelleConfiguration")
        value=""
        Refresh=True  
        self.update()
        sender = self.sender()

 

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n*100/4)

        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)


    def recurring_timer(self):
        global gicleurs
        global gicleursStatut
        global Refresh
    
        if t2.is_alive==False:
                t2.start()

        if gicleursStatut["1"].Statut==0:
            self.ui.groupBox_2.setStyleSheet("background-color:rgb(255,230,205);")
        else:
            self.ui.groupBox_2.setStyleSheet("background-color:rgb(255,128,0);")
            
        if gicleursStatut["2"].Statut==0:         
            self.ui.groupBox_3.setStyleSheet("background-color:rgb(255,230,205);")
        else:
            self.ui.groupBox_3.setStyleSheet("background-color:rgb(255,128,0);")

        if gicleursStatut["3"].Statut==0:         
            self.ui.groupBox_4.setStyleSheet("background-color:rgb(255,230,205);")
        else:
            self.ui.groupBox_4.setStyleSheet("background-color:rgb(255,128,0);")

        if gicleursStatut["4"].Statut==0:         
            self.ui.groupBox_5.setStyleSheet("background-color:rgb(255,230,205);")
        else:
            self.ui.groupBox_5.setStyleSheet("background-color:rgb(255,128,0);")
            
            #print ("ddddddddddddddddddddddddddddd", recGicleurs)
            #ZoneArrosageMaintenant=recGicleurs
            
        valide=False


        if (Refresh==True):
            try:
                self.ui.ArrosageActif.setChecked(confGeneral.SystemArrosageActif)
                self.ui.DetecteurPluieActif.setChecked(confGeneral.SondePluieActive)
                self.ui.HeureArrosage.setValue(confGeneral.HeureDebutArrosage)
                self.ui.JourArrosage.setCurrentText(confGeneral.ArrosageJourPairImpair)
                self.ui.IntervalEntreArrosage.setValue(confGeneral.NombreJourInterval)

                self.ui.NoZone1.setText(str(gicleurs["1"].NoZone))
                self.ui.Zone1Active.setChecked(gicleurs["1"].ZoneActive)
                self.ui.Zone1TempsArrosage.setValue(int(gicleurs["1"].TempsArrosage))
                self.ui.Zone1Physique.setText(gicleurs["1"].ZonePhysique)

                self.ui.NoZone2.setText(str(gicleurs["2"].NoZone))
                self.ui.Zone2Active.setChecked(gicleurs["2"].ZoneActive)
                self.ui.Zone2TempsArrosage.setValue(int(gicleurs["2"].TempsArrosage))
                self.ui.Zone2Physique.setText(gicleurs["2"].ZonePhysique)

                self.ui.NoZone3.setText(str(gicleurs["3"].NoZone))
                self.ui.Zone3Active.setChecked(gicleurs["3"].ZoneActive)
                self.ui.Zone3TempsArrosage.setValue(int(gicleurs["3"].TempsArrosage))
                self.ui.Zone3Physique.setText(gicleurs["3"].ZonePhysique)

                self.ui.NoZone4.setText(str(gicleurs["4"].NoZone))
                self.ui.Zone4Active.setChecked(gicleurs["4"].ZoneActive)
                self.ui.Zone4TempsArrosage.setValue(int(gicleurs["4"].TempsArrosage))
                self.ui.Zone4Physique.setText(gicleurs["4"].ZonePhysique)

                self.update()

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
                print(exc_type, fname, exc_tb.tb_lineno)

            Refresh=False
        

redisClient = redis.StrictRedis(host=Host, port=6379, decode_responses=True)

def initialiseConfigurationGenerale():
    global GicleurAssocie
    confGeneral=CONFIGURATION_GENERALE()

    confGeneral.ArrosageJourPairImpair="Pair"
    confGeneral.SystemArrosageActif=True
    confGeneral.SondePluieActive=False
    confGeneral.HeureDebutArrosage=16
    confGeneral.NombreJourInterval=2

    return confGeneral

def is_redis_available(r):
    try:
        r.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        return False
    return True
    

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
    confGeneral.SystemArrosageActif=True
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
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=60
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Avant près de la maison"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=3
    gicleurRec.ZoneNom="Gicleur_3_"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=60
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="coté de la maison"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    gicleurRec=GICLEURS()
    gicleurRec.NoZone=4
    gicleurRec.ZoneNom="Gicleur_4_"
    gicleurRec.ZoneActive=True
    gicleurRec.TempsArrosage=60
    gicleurRec.Affichage=True
    gicleurRec.AffichageWeb=True
    gicleurRec.MessageErreur=True
    gicleurRec.ZonePhysique="Arrière de la maison"
    gicleurs[str(gicleurRec.NoZone)]=gicleurRec

    GicleurAssocie={}
    return gicleurs


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

def sauvegardeConfigurationGeneralGicleurs():
    global redisClient

    if is_redis_available(redisClient):
        try:
            dataJson = jsonpickle.encode(gicleurs)
            redisClient.set(const.gicleurData, dataJson)
            dataJson = jsonpickle.encode(confGeneral)
            redisClient.set(const.confGeneralData, dataJson)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)
        #redisClient.publish(const.publishNom, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=Host, port=6379, charset="utf-8", decode_responses=True)

@dataclass
class SOCKET_ACCESS:
    Nom: str=""
    Ip: str =""
    Port: int = ""


# def redisSubscribe():
#    global DataFromRedis
#    global redisClient
#    global Equipement
#    print ("redisSubscribe passe 0")
#    if is_redis_available(redisClient):
#        clientSubscribe = redisClient.pubsub()
#        clientSubscribe.subscribe(const.susbscribeRequestData)
#        for message in clientSubscribe.listen():
#            if message is not None and isinstance(message, dict):
#                xxxxxx = message.get('data')
#                if xxxxxx!=1:
#                    Equipement = jsonpickle.decode(xxxxxx)
#                    #Equipement=json.loads(DataFromRedis, cls=EquipementsDecoder)
#    else:
#        redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8", decode_responses=True)

def sauvegardeMessageActivites(DateMessage,NoZone,Message):
    global redisClient
    
    
    if is_redis_available(redisClient):
        try:
            messageActiviteStr=str(DateMessage)+','+str(NoZone)+','+str(Message)
            redisClient.lpush  (const.clefMessage, messageActiviteStr)
           
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)
    else:
        redisClient = redis.StrictRedis(host=Host, port=6379, charset="utf-8", decode_responses=True)

    

def publishDataPourArrosage(publishNom, action):
     global redisClient
     if is_redis_available(redisClient):
         try:
             redisClient.publish(publishNom, action)
         except Exception as e:
             exc_type, exc_obj, exc_tb = sys.exc_info()
             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
             print(exc_type, fname, exc_tb.tb_lineno)
     else:
         redisClient = redis.StrictRedis(host=Host, port=6379, charset="utf-8", decode_responses=True)

def ArrosageSystemeDataGicleurs():
    global hostClient, EquipementInterface, gicleursStatut

    HOST = socketIpPort.SendRec["ArrosageEcranDataEquipement"].Ip
    PORT = socketIpPort.SendRec["ArrosageEcranDataEquipement"].Port

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

def GicleursSystemeAction(HOST, PORT, Requete):
    global s
    try:
        # recreate the socket and reconnect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        data_string = pickle.dumps(Requete)
        s.send(data_string)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
        print(exc_type, fname, exc_tb.tb_lineno)


# confGeneral=initialiseConfigurationGenerale()
# gicleurs=initialiaseGicleurs(**gicleurs)
# sauvegardeConfigurationGeneralGicleurs()


gicleursStatut= initialiseGicleursStatut()


t2 = threading.Thread(target=ArrosageSystemeDataGicleurs)
t2.start()

# t1 = threading.Thread(target=redisSubscribe)
# t1.start()

# initialiseConfigurationGenerale()
# gicleurs = initialiaseGicleurs()
gicleurs, confGeneral=recupereConfigurationGeneralGicleurs()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


   
