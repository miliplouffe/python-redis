import sys, os
sys.path.insert(1, "G:\DeveloppementEnvironnement\Python\Systemes\ImportFile")
# sys.path.insert(1, "/home/pi/python")
from time import sleep
import threading
import socket,jsonpickle,pickle
from time import sleep
import socketIpPort

SendRec=dict()
socketIpPort.Host = "192.168.1.210"
socketIpPort.HostEcranAlarme = "192.168.1.227"
socketIpPort.HostEcranArrosage = "192.168.1.227"
SendRec = socketIpPort.initIpPort()

def ConfigurationArrosage():
    global s, Equipement, gicleursStatut, gicleurs, confGeneral, Refresh

    HOST = SendRec["ConfigurationEcranArrosage"].Ip
    PORT = SendRec["ConfigurationEcranArrosage"].Port


    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("passe 1",HOST, PORT)
                s.bind((HOST, PORT))

                print("passe 2")
                s.listen(50)
                print("passe 3")
                conn, addr = s.accept()
                print("passe 4")
                with conn:
                    print("passe 5")
                    while True:
                        print("passe 6")
                        data = conn.recv(4096)
                        print("passe 7  ", data)
                        if not data:
                            break
                        else:
                            if len(data)>400:
                                gicleurs = pickle.loads(data)
                                Refresh=True
                            else:
                                confGeneral = pickle.loads(data)
                                # Refresh=True

            
        except socket.error as message:
            print('Bind failed. Error Code : '
                    + str(message[0]) + ' Message '
                    + message[1])

def GicleursSystemeAction(HOST, PORT, Requete):
    try:
        # recreate the socket and reconnect
        print ("asdfasdfasdf0  ",HOST, PORT)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        data_string = pickle.dumps(Requete)
        print ("00000 ", data_string, Requete)
        s.send(data_string)
        s.close()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]    
        print(exc_type, fname, exc_tb.tb_lineno)


if __name__ == '__main__':
    t2 = threading.Thread(target=ConfigurationArrosage)
    t2.start()
    GicleursSystemeAction(SendRec["GicleursSystemeAction"].Ip, SendRec["GicleursSystemeAction"].Port, "RecupereConfiguration")
    while True:
        print ("ok")
        sleep(1)



