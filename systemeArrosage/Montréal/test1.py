with open("G:\DeveloppementEnvironnement\Python\Systemes\ImportFile\ipaddress.data",'r') as data_file:
    for line in data_file:
        data = line.split(';')
        print(data)

    for x in data:
        y=x.split(',')
        print (y[0], y[1])
        if y[0]=="HostInterface":
            socketIpPort.HostInterface = y[1]
        if y[0]=="HostSystemeArrosage":
            socketIpPort.HostSystemeArrosage = y[1]
        if y[0]==HostEcranAlarme":
            socketIpPort.HostEcranAlarme = y[1]
        if y[0]=="HostEcranArrosage":
            socketIpPort.HostEcranArrosage = y[1]
        if y[0]=="HostSystemeAlarme":
            socketIpPort.HostSystemeAlarme = y[1]
