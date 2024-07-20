import sys, os

from PyQt5.QtWidgets import *
from PyQt5.QtCore  import *

import time
from datetime import datetime, timedelta
import traceback, sys
from alarmeEcranDialog import Ui_MainWindow
from functools import partial
from dataclasses import dataclass

from time import sleep
import RedisInOut as redisInOut

code="25631"
valideCode=False
construitCode=""
requete=""


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
    susbscribeRequestData      = "alarmeMtlData"
    publishSystemeAlarmeStatut = "alarmeMtlStatut"
    publishEcranErreur          = "alarmeEcranErreur"
    clefCourriel                = "Courriel"





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

DateHeureCourante =datetime
NomEquipement =str
Armer = bool 
Alarme=bool
Actif = bool
Valeur=int
Affichage=bool
MessageErreur=str
AffichageWeb=str

DataFromRedis=""

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
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.ui.Bouton1.clicked.connect(partial(self.clicked_btn, "1"))
        self.ui.Bouton2.clicked.connect(partial(self.clicked_btn, "2"))
        self.ui.Bouton3.clicked.connect(partial(self.clicked_btn, "3"))
        self.ui.Bouton4.clicked.connect(partial(self.clicked_btn, "4"))
        self.ui.Bouton5.clicked.connect(partial(self.clicked_btn, "5"))
        self.ui.Bouton6.clicked.connect(partial(self.clicked_btn, "6"))
        self.ui.Bouton7.clicked.connect(partial(self.clicked_btn, "7"))
        self.ui.Bouton8.clicked.connect(partial(self.clicked_btn, "8"))
        self.ui.Bouton9.clicked.connect(partial(self.clicked_btn, "9"))
        self.ui.Bouton0.clicked.connect(partial(self.clicked_btn, "0"))
        self.ui.BoutonStar.clicked.connect(partial(self.clicked_btn, "*"))
        self.ui.BoutonReset.clicked.connect(partial(self.clicked_btn, "#"))

        self.ui.ActivationComplete.clicked.connect(partial(self.clicked_btn_action, "ActivationComplete"))
        self.ui.ActivationPartielle.clicked.connect(partial(self.clicked_btn_action, "ActivationPartielle"))
        self.ui.Desactivation.clicked.connect(partial(self.clicked_btn_action, "Desactivation"))
        self.ui.courriel.clicked.connect(partial(self.radio_btn,  self.ui.courriel))
       

        # if self.ui.courriel.isChecked():

        #    self.clicked_btn_action("courrielActif")
        # else:
        #    self.clicked_btn_action("courrielInactif")

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def radio_btn(self,objet):
        if objet.isChecked()==True:
            sauvegardeMessageActivites("courrielActif")
        else:
            sauvegardeMessageActivites("courrielInactif")
        
    def clicked_btn(self, value):
        global construitCode
        global valideCode
        print (construitCode)
        if len(construitCode) < 5:
            construitCode=construitCode+value      
        if value=="#":
            construitCode=""
            self.ui.codeValideCercle.setStyleSheet("background-color: red")

        if construitCode==code:
            self.ui.codeValideCercle.setStyleSheet("background-color: lightgreen")
            valideCode=True
            construitCode=""
        sender = self.sender()

    def clicked_btn_action(self, value):
        global valideCode
        if valideCode==True and value=="Desactivation":
            redisInOut.publishSystemeAlarmeRequete(value)
            valideCode=False
            self.ui.codeValideCercle.setStyleSheet("background-color: red")
        else:
            if value != "Desactivation":
                redisInOut.publishSystemeAlarmeRequete(value)
                valideCode=False
                self.ui.codeValideCercle.setStyleSheet("background-color: red")

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
        # Pass the function to executesn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)


    def recurring_timer(self):
        global Equipement
        global DataFromRedis
        global valideCode
        global requete
        try:

            # if t1.is_alive()==False:
            #    t1.start()
   
            redisInOut.RunRedisInOut("startSystemeAlarmeEquipement")  # check if task is running
            valeurData=EQUIPEMENT()
            Equipement=redisInOut.getSystemeAlarmeEquipement()
            sleep(.5)
            print (" Equipement  ", Equipement["Mouvement"].Valeur)

            # if CourrielValeur == "courrielActif":
            #     self.ui.courriel.setChecked(True)
            # if CourrielValeur == "courrielInactif":
            #     self.ui.courriel.setChecked(False)

            valeurData=Equipement["Mouvement"].Valeur
            if valeurData==0:
                self.ui.MouvementCercle.setStyleSheet("background-color: lightgreen")
            else:
                if valeurData==1:
                    self.ui.MouvementCercle.setStyleSheet("background-color: red")
                else:
                    self.ui.MouvementCercle.setStyleSheet("background-color: orange")

            valeurData=Equipement["Prop"].Valeur
            if valeurData==0:
                self.ui.PropCercle.setStyleSheet("background-color: lightgreen")
            else:
                if valeurData==1:
                    self.ui.PropCercle.setStyleSheet("background-color: red")
                else:
                    self.ui.PropCercle.setStyleSheet("background-color: orange")

            valeurData=Equipement["Co"].Valeur
            if valeurData==0:
                self.ui.CoCercle.setStyleSheet("background-color: lightgreen")
            else:
                if valeurData==1:
                    self.ui.CoCercle.setStyleSheet("background-color: red")
                else:
                    self.ui.CoCercle.setStyleSheet("background-color: orange")

            valeurData=Equipement["Fumee"].Valeur
            if valeurData==0:
                self.ui.FumeeCercle.setStyleSheet("background-color: lightgreen")
            else:
                if valeurData==1:
                    self.ui.FumeeCercle.setStyleSheet("background-color: red")
                else:
                    self.ui.FumeeCercle.setStyleSheet("background-color: orange")

            valeurData=Equipement["EauElectrique"].Valeur
            if valeurData==0:
                self.ui.EauElectriqueCercle.setStyleSheet("background-color: lightgreen")
            else:
                if valeurData==1:
                    self.ui.EauElectriqueCercle.setStyleSheet("background-color: red")
                else:
                    self.ui.EauElectriqueCercle.setStyleSheet("background-color: orange")

            valeurData=Equipement["EauTraitement"].Valeur
            if valeurData==0:
                self.ui.EauTraitementCercle.setStyleSheet("background-color: lightgreen")
            else:
                if valeurData==1:
                    self.ui.EauTraitementCercle.setStyleSheet("background-color: red")
                else:
                    self.ui.EauTraitementCercle.setStyleSheet("background-color: orange")

            valeurData=Equipement["PanneElectrique"].Valeur
            if valeurData==0:
                self.ui.PanneElectriqueCercle.setStyleSheet("background-color: lightgreen")
            else:
                if valeurData==1:
                    self.ui.PanneElectriqueCercle.setStyleSheet("background-color: red")
                else:
                    self.ui.PanneElectriqueCercle.setStyleSheet("background-color: orange")

            if requete=='"ActivationPartielle"' or requete=='"ActivationComplete"':
                self.ui.SystemeArmeCercle.setStyleSheet("background-color: lightgreen")   
            else:
                self.ui.SystemeArmeCercle.setStyleSheet("background-color: red")
                       
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)
            # valeurData=valeurDataBackup


def sauvegardeMessageActivites(Message):
    print ("En construction")

Equipement = dict()
redisInOut.startSystemeAlarmeEquipement()
# CourrielValeur=recupereCourrielStatut()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())