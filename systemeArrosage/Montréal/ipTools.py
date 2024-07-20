import os

park = []
for i in range(255):
     park.append('192.168.1.' + str(i))

for ip in park:
    response = os.popen(f"ping {ip} ").read()
    # Pinging each IP address 4 times
    
    #saving some ping output details to output file
    if("Request timed out." or "unreachable") in response:
        print(response)
        f = open("ip_output.txt","a")
        f.write(str(ip) + ' link is down'+'\n')
        f.close() 
    else:
        print(response)
        f = open("ip_output.txt","a")  
        f.write(str(ip) + ' is up '+'\n')
        f.close() 
    # print output file to screen
with open("ip_output.txt") as file:
    output = file.read()
    f.close()
    print(output)
with open("ip_output.txt","w") as file:    
	pass