from flask import Flask
from flask import request
from flask import render_template
import os
import redis
import jsonpickle
import threading
import time
import os

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

Equipement = dict()


class const:
    subscribeRequestWeb        = "alarmeMtlAction"
    susbscribeRequestData      = "alarmeMtlData"
    publishSystemeAlarmeStatut = "alarmeMtlStatut"
class DATACUMMULATIF:
    def __init__(self, DateHeureCourante,Endroit,Message):
        self.DateHeureCourante=DateHeureCourante
        self.Endroit=Endroit
        self.Message=Message

class EQUIPEMENT:
    def __init__(self, DateHeureCourante,NomEquipement,Armmer,Alarme,Actif,Valeur,Affichage,AffichageWeb, MessageErreur):
       self.DateHeureCourante=DateHeureCourante
       self.NomEquipement=NomEquipement
       self.Armmer=Armmer
       self.Alarme=Alarme
       self.Actif=Actif
       self.Valeur=Valeur
       self.Affichage=Affichage
       self.AffichageWeb=AffichageWeb
       self.MessageErreur=MessageErreur

redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, decode_responses=True)

def is_redis_available(r):
    try:
        r.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        return False
    return True


def publishActionPourWebEtEcran(action):
    global redisClient
    if is_redis_available(redisClient):
        dataToSend = jsonpickle.encode(action)
        #dataToSend = json.dumps(action, cls=CustomJSONEncoder)
        redisClient.publish(const.subscribeRequestWeb, action)
    else:
        redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8", decode_responses=True)


def redisSubscribe():
    global DataFromRedis
    global redisClient
    global Equipement
    print ("redisSubscribe passe 0")
    if is_redis_available(redisClient):
        clientSubscribe = redisClient.pubsub()
        clientSubscribe.subscribe(const.susbscribeRequestData)
        for message in clientSubscribe.listen():
            if message is not None and isinstance(message, dict):
                dataReceived = message.get('data')
                if dataReceived!=1:
                    Equipement = jsonpickle.decode(dataReceived)
                    #Equipement=json.loads(DataFromRedis, cls=EquipementsDecoder)
    else:
        redisClient = redis.StrictRedis(host='192.168.1.210', port=6379, charset="utf-8", decode_responses=True)





t1 = threading.Thread(target=redisSubscribe)
t1.start()

DataCummulatif = dict()

template_dir = os.path.abspath("/home/pi/python")
app = Flask(__name__, template_folder=template_dir)

dateHeure=""
endroit=""
message=""
@app.route("/action", methods=['GET', 'POST'])
def contact():
    if "miseAJour" in str(request.form):
        publishActionPourWebEtEcran("1")
        time.sleep(1)
        return render_template('alarmeWeb.html',data=Equipement)
        pass
    if "shutdown" in str(request.form):
        publishActionPourWebEtEcran("shutdown")
        pass

    if "Redemarrer" in str(request.form):
        publishActionPourWebEtEcran("Redemarrer")
        pass

    if "Rapports" in str(request.form):
        publishActionPourWebEtEcran("Rapports")
        return render_template('alarmeWeb.html',data=Equipement)
        pass
    if "Activation partielle" in str(request.form):
        publishActionPourWebEtEcran("ActivationPartielle")
        time.sleep(1)
        return render_template('alarmeWeb.html',data=Equipement)
        pass

    if "Activation complete" in str(request.form):
        publishActionPourWebEtEcran("ActivationComplete")
        time.sleep(1)
        return render_template('alarmeWeb.html',data=Equipement)
        pass
    if "Désactivation" in str(request.form):
        publishActionPourWebEtEcran("Desactivation")
        time.sleep(1)
        return render_template('alarmeWeb.html',data=Equipement)
        pass
    if "DonneesCummulativesPage" in str(request.form):
        with open("/home/pi/python/alarmeLog.txt",'r') as script:
            speech = script.read().splitlines()
        for line in speech:
            record=DATACUMMULATIF(dateHeure,endroit,message)
            rec = line.strip().split(',')
            record.DateHeureCourante=str(rec[0])
            record.Endroit=str(rec[1])
            record.Message=str(rec[2])
            DataCummulatif[record.DateHeureCourante]=record
          
            #show_DonneesCummulatives()
        time.sleep(1)
        return render_template('DonneesCummulatives.html',data1=DataCummulatif)
        pass

    if "Page précédente" in str(request.form):
        publishActionPourWebEtEcran("1")
        time.sleep(1)
        return render_template('alarmeWeb.html',data=Equipement)
        pass


@app.route('/')
def show_index():
    return render_template('alarmeWeb.html',data=Equipement)

@app.route('/')
def show_DonneesCummulatives():
    return render_template('DonneesCummulatives.html',data1=DataCummulatif)


app.debug = True
if __name__ == '__main__':
    app.run(host='0.0.0.0')