import redis
import jsonpickle
import threading,os,sys

ipaddressRedis='192.168.1.142'

class const:
    gicleurData             = "GicleurData"
    confGeneralData         = "ConfGeneralData"
    confSystemeAlarme       = "confSystemeAlarme"
    subscribeSystemeAlarme = "subscribeSystemeAlarme"
    susbscribeGicleursConfiguration = "systemeData"

gicleurConfiguration=dict()
redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8",decode_responses=True)
Requete = str

def is_redis_available(r):
    try:
        r.ping()
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        return False
    return True

def recupereConfigurationSystemeAlarme():
    global redisClient
    global gicleurConfiguration

    if is_redis_available(redisClient):
        try:
            value = redisClient.get(const.confSystemeAlarme)
            gicleurConfiguration = jsonpickle.decode(value)
        except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
                    print(exc_type, fname, exc_tb.tb_lineno)
                #redisClient.publish(const.publishNom, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True) 
    return gicleurConfiguration

def subscribeSystemeAlarme():
    global Requete
    global redisClient

    while True:
        Requete=""
        if is_redis_available(redisClient):
            clientSubscribe = redisClient.pubsub()
            clientSubscribe.subscribe(const.subscribeSystemeAlarme)
            for message in clientSubscribe.listen():
                if message is not None and isinstance(message, dict):
                    Requete = message.get('data')
            
def redisSubscribe():
   global gicleurConfiguration
   global redisClient
   print ("redisSubscribe passe 0")
   if is_redis_available(redisClient):
       clientSubscribe = redisClient.pubsub()
       clientSubscribe.subscribe(const.confSystemeAlarme)
       for message in clientSubscribe.listen():
           if message is not None and isinstance(message, dict):
               xxxxxx = message.get('data')
               if xxxxxx!=1:
                   gicleurConfiguration = jsonpickle.decode(xxxxxx)
                   #Equipement=json.loads(DataFromRedis, cls=EquipementsDecoder)
   else:
       redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)

def getGicleursConfiguration():
    global gicleurConfiguration

    return gicleurConfiguration
def getRequete():
    return Requete
    

def sauvegardeSystemeAlarme(**Equipements):
    global redisClient

    if is_redis_available(redisClient):
        try:
            dataJson = jsonpickle.encode(Equipements)
            redisClient.set(const.confSystemeAlarme, dataJson)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
            print(exc_type, fname, exc_tb.tb_lineno)
        #redisClient.publish(const.publishNom, dataToSend)
    else:
        redisClient = redis.StrictRedis(host=ipaddressRedis, port=6379, charset="utf-8", decode_responses=True)


def startTask():
    t1 = threading.Thread(target=redisSubscribe)
    t1.start()

    t2 = threading.Thread(target=subscribeSystemeAlarme)
    t2.start()