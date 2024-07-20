#!/bin/bash

import sys
sys.path.append("/home/pi/.local/lib/python3.9/site-packages/")
sys.path.append("/home/miliplouffe/.local/lib/python3.11/site-packages/")
import threading,os,sys
from time import sleep
import jsonpickle
import redis

ipaddressRedis='192.168.1.102'
# ipaddressRedis='192.168.1.125'

class const:

    configurationArrosageGicleurs = "configurationArrosageGicleurs"
    configurationArrosageGenerale= "configurationArrosageGenerale"

    gicleurData             = "GicleurData"
    confGeneralData         = "ConfGeneralData"
    confSystemeAlarme       = "confSystemeAlarme"
    InterfaceArduinoRequete = "publishArduinoRequete"
    InterfaceDetecteur = "dataUnite"
    systemeAlarmeRequete = "subscribeSystemeAlarmeRequete"
    systemeAlarmeEquipement = "susbscibeSystemeAlarme"
    systemeArrosageRequete = "subscribeSystemeArrosageRequete"

gicleurConfiguration=dict()
redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8",decode_responses=True)
RequeteInterface = ""
RequeteAlarme = ""
RequeteArrosage=""
Detecteur = dict()
Equipement=dict()
gicleurs= ""
configurationArrosageGenerale = ""
StatutGicleurs=""


def InitialiseRedisClient():
    global gicleurConfiguration, redisClient, RequeteInterface, RequeteAlarme, Detecteur, RequeteArrosage

    redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8",decode_responses=True)
    RequeteInterface = ""
    RequeteAlarme = ""
    RequeteArrosage = ""
    Detecteur = dict()

def is_redis_available():
    global redisClient
    valide = True

    try:
        redisClient.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        InitialiseRedisClient()
        try:
            redisClient.ping()
            valide = True
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            valide = False

    return valide


def subscribeInterfaceArduinoRequete():
    global RequeteInterface
    global redisClient

    while True:
        RequeteInterface=''
        if is_redis_available():
            clientSubscribe = redisClient.pubsub()
            clientSubscribe.subscribe(const.InterfaceArduinoRequete)
            for message in clientSubscribe.listen():
                if message is not None and isinstance(message, dict):
                    RequeteInterface = message.get('data')
 

def subscribeGicleursConfiguration():
   global gicleurConfiguration
   global redisClient
   while True:
        if is_redis_available():
            clientSubscribe = redisClient.pubsub()
            clientSubscribe.subscribe(const.confSystemeAlarme)
            for message in clientSubscribe.listen():
                if message is not None and isinstance(message, dict):
                    xxxxxx = message.get('data')
                    if xxxxxx!=1:
                        gicleurConfiguration = jsonpickle.decode(xxxxxx)
                        
        else:
            redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)
    
def sauvegardeArrosageConfigurationGicleurs(gicleurs):
    global redisClient

    if is_redis_available():
        try:
            dataJson = jsonpickle.encode(gicleurs)
            redisClient.set(const.configurationArrosageGicleurs, dataJson)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)
        #redisClient.publish(const.publishNom, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)

def recupereArrosageConfigurationGicleurs():
    global gicleurs
    global redisClient

    if is_redis_available():
        try:
            value = redisClient.get(const.configurationArrosageGicleurs)
            gicleurConfiguration = jsonpickle.decode(value)
        except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
                    # print(exc_type, fname, exc_tb.tb_lineno)
                #redisClient.publish(const.publishNom, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True) 
    return gicleurConfiguration


def sauvegardeSystemeArrosageConfigurationGenerale(configurationArrosageGenerale):
    global redisClient

    if is_redis_available():
        try:
            dataJson = jsonpickle.encode(configurationArrosageGenerale)
            redisClient.set(const.configurationArrosageGenerale, dataJson)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)
        #redisClient.publish(const.publishNom, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)

def recupereSystemeArrosageConfigurationGenerale():
    global configurationArrosageGenerale
    global redisClient
    # print ("passe 1")

    if is_redis_available():
        try:
            value = redisClient.get(const.configurationArrosageGenerale)
            configurationArrosageGenerale = jsonpickle.decode(value)
        except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
                    # print(exc_type, fname, exc_tb.tb_lineno)
                #redisClient.publish(const.publishNom, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True) 
    return configurationArrosageGenerale
   

def sauvegardeSystemeAlarme(**Equipements):
    global redisClient

    if is_redis_available():
        try:
            dataJson = jsonpickle.encode(Equipements)
            redisClient.set(const.confSystemeAlarme, dataJson)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)
        #redisClient.publish(const.publishNom, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)


def publishInterfaceArduinoRequete(Requete):
    global redisClient
    if is_redis_available():
        # dataToSend = jsonpickle.encode(Requete)
        #dataToSend = json.dumps(action, cls=CustomJSONEncoder)
        redisClient.publish(const.InterfaceArduinoRequete, Requete)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)   

def recupereArduinoDetecteur():
    global Detecteur
    global redisClient
    redisClient.publish("allo ", 44444444) 
    while True:
        redisClient.publish("allo ", 44444444) 
        if is_redis_available():
            redisClient.publish("allo ", 44444444) 
            clientSubscribe = redisClient.pubsub()
            clientSubscribe.subscribe(const.InterfaceDetecteur)

            for message in clientSubscribe.listen():
                if message is not None and isinstance(message, dict):
                    xxxxxx = message.get('data')
                    redisClient.publish("allo ", xxxxxx) 
                    sleep(.3)
                    if xxxxxx!=1:
                        Detecteur = jsonpickle.decode(xxxxxx)
                        #Equipement=json.loads(DataFromRedis, cls=EquipementsDecoder)
        else:
            redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)


# Envoie les donnes au systeme alarme et systeme arrosage
def publishInterfaceArduinoDetecteur(Detecteur):
    global redisClient
    if is_redis_available():
        try:
            dataToSend = jsonpickle.encode(Detecteur)
            #dataToSend = json.dumps(action, cls=CustomJSONEncoder) 
            redisClient.publish(const.InterfaceDetecteur, dataToSend)    
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            # print(exc_type, fname, exc_tb.tb_lineno)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)

def subscribeSystemeAlarmeEquipement():
   global Equipement
   global redisClient
   while True:
    if is_redis_available():
        clientSubscribe = redisClient.pubsub()
        clientSubscribe.subscribe(const.systemeAlarmeEquipement)
        for message in clientSubscribe.listen():
            if message is not None and isinstance(message, dict):
                xxxxxx = message.get('data')
                if xxxxxx!=1:
                    Equipement = jsonpickle.decode(xxxxxx)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True) 

def subscribeSystemeAlarmeRequete():
    global RequeteAlarme
    global redisClient

    while True:
        RequeteAlarme=""
        if is_redis_available():
            clientSubscribe = redisClient.pubsub()
            clientSubscribe.subscribe(const.systemeAlarmeRequete)
            for message in clientSubscribe.listen():
                if message is not None and isinstance(message, dict):
                    RequeteAlarme = message.get('data')
 

def publishSystemeAlarmeRequete(Requete):
    global redisClient
    if is_redis_available():
        # dataToSend = jsonpickle.encode(Requete)
        #dataToSend = json.dumps(action, cls=CustomJSONEncoder)
        redisClient.publish(const.systemeAlarmeRequete, Requete)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)   

# Envoie les donnes au systeme alarme et systeme arrosage
def publishSystemeAlarmeEquipement(Equipement):
    global redisClient
    if is_redis_available():
        dataToSend = jsonpickle.encode(Equipement)
        #dataToSend = json.dumps(action, cls=CustomJSONEncoder)
        redisClient.publish(const.systemeAlarmeEquipement, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)

def subscribeSystemeArrosageRequete():
    global RequeteArrosage
    global redisClient

    while True:
        RequeteArrosage=""
        if is_redis_available():
            clientSubscribe = redisClient.pubsub()
            clientSubscribe.subscribe(const.systemeArrosageRequete)
            for message in clientSubscribe.listen():
                if message is not None and isinstance(message, dict):
                    RequeteArrosage = message.get('data')

            print ("Requete arrosage 5555 ", RequeteArrosage)

def publishSystemeArrosageRequete(Requete):
    global redisClient
    if is_redis_available():
        # dataToSend = jsonpickle.encode(Requete)
        #dataToSend = json.dumps(action, cls=CustomJSONEncoder)
        redisClient.publish(const.systemeArrosageRequete, Requete)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)   

def publishSystemeStatutGicleurs(statutGicleurs):
    global redisClient
    if is_redis_available():
        dataToSend = jsonpickle.encode(statutGicleurs)
        #dataToSend = json.dumps(action, cls=CustomJSONEncoder)
        redisClient.publish(const.gicleurData, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)

def subscribeSystemeArrosageStatut():
    global StatutGicleurs
    global redisClient
    while True:
        if is_redis_available():
            clientSubscribe = redisClient.pubsub()
            clientSubscribe.subscribe(const.gicleurData)
            for message in clientSubscribe.listen():
                if message is not None and isinstance(message, dict):
                    xxxxxx = message.get('data')
                    if xxxxxx!=1:
                        StatutGicleurs = jsonpickle.decode(xxxxxx)
        else:
            redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True) 

t1 = threading.Thread(target=subscribeInterfaceArduinoRequete)
t2 = threading.Thread(target=subscribeSystemeArrosageRequete)
t3 = threading.Thread(target=subscribeSystemeAlarmeRequete)
t5 = threading.Thread(target=recupereArduinoDetecteur)
t6 = threading.Thread(target=subscribeSystemeAlarmeEquipement)
t7 = threading.Thread(target=subscribeSystemeArrosageStatut)

def getRequeteInterface():
    global RequeteInterface
    return RequeteInterface

def getRequeteAlarme():
    global RequeteAlarme
    return RequeteAlarme

def getRequeteArrosage():
    global RequeteArrosage
    return RequeteArrosage

def setRequeteArrosageNil():
    global RequeteArrosage
    RequeteArrosage=""

def getArduinoDetecteur():
    global Detecteur
    return Detecteur

def getSystemeAlarmeEquipement():
    global Equipement
    return Equipement

def getSystemeArrosageStatut():
    global StatutGicleurs
    return StatutGicleurs

def StartInterfaceArduinoRequete():
    global t1
    t1.start()

def StartSystemeArrosageRequete():
    global t2
    t2.start()

def StartSystemeAlarmeRequete():
    global t3
    t3.start()

# def StartSystemeAlarmeConfiguration():
#     t4 = threading.Thread(target=recupereConfigurationSystemeAlarme)
#     t4.start()
# 

def StartArduinoDetecteurs():
    global t5
    t5.start()

def startSystemeAlarmeEquipement():
    global t6
    t6.start()

def startSystemeStatutGicleur():
    global t7
    t7.start()

def RunRedisInOut(threadingName):
    if threadingName=="StartInterfaceArduinoRequete":
        if t1.is_alive()==False:
            t1.start()

    if threadingName=="StartSystemeArrosageRequete":
        if t2.is_alive()==False:
            t2.start()

    if threadingName=="StartSystemeAlarmeRequete":
        if t3.is_alive()==False:
            t3.start()

    if threadingName=="StartArduinoDetecteurs":
        if t5.is_alive()==False:
            t5.start()

    if threadingName=="startSystemeAlarmeEquipement":
        if t6.is_alive()==False:
            t6.start()

    if threadingName=="startSystemeStatutGicleur":
        if t7.is_alive()==False:
            t7.start()


