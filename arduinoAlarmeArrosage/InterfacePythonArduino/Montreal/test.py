
import RedisInOut as redisInOut
import threading, time
from dataclasses import dataclass
from datetime import datetime, timedelta

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

zoneList = []
NomEquipement =str

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


gicleurTest=dict()

if __name__ == '__main__':
        
    Equipement = dict()
    Equipement = initialiseVariables(**Equipement)
    redisInOut.sauvegardeSystemeAlarme(**Equipement)

    redisInOut.StartArduinoDetecteurs()

    # time.sleep(1)
    Equipement=redisInOut.recupereConfigurationSystemeAlarme()

    # xx=from_dict(data_class=User, data=gicleurConfiguration)
    while True:
        try:
            print ("------------------------------------------------")
            Detecteur=redisInOut.getArduinoDetecteur()
            print ("sdfgsdfgsdfgsdffffffffffffff ", Detecteur['InterPorteSousSol'])
            #time.sleep(.5)
            # if Requete!= "":
            #     print ("asfasdfasdf", Requete)
            #     resetRequete.Requete=""
            # time.sleep(.5) 
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)