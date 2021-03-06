# e necessario far partire il programma dal terminale con i seguenti comandi:
# sudo python main.py
#cosi facendo si hanno i permessi di root

import sys
import os
import socket
import netifaces as ni

#########################################################################################################

#variabile statica globale presente all interno del file configured.txt che
# in base al valore capisco se non e configurato, e un host o e un gateway
file = open("configured.txt", "r")
configured = file.read()

#print 'Name wireless interface:'
wlan = "en1"  # <- - - - - - - - - - - - - - -  [MODIFICARE INTERFACCIA WIFI]

print '1) start'
print '2) reset'
start = raw_input()
if not start == '1':
    print '****************** reset configuration *************************'
    file = open("configured.txt", "w")
    file.write("null")
    sys.exit(0)

#il mio indirizzo IP
#prima configurazione oppure sono un host
if str(configured) == "null" or str(configured) == "host":
    ni.ifaddresses(wlan)
    myIP = ni.ifaddresses(wlan)[2][0]['addr']
    print '- - - - - - - - - - '+myIP+' - - - - - - - - - - - \n'

    print os.system('iwconfig | grep '+wlan)
    print '- - - - - - - - - - - - - - - - - - - - - - - - - -'
#sono un gateway
else:
    ni.ifaddresses(wlan)
    myIP = ni.ifaddresses(wlan+':1')[2][0]['addr']
    print '- - - - - - - - - - ' + myIP + ' - - - - - - - - - - - \n'

    print os.system('iwconfig | grep ' + wlan)
    print '- - - - - - - - - - - - - - - - - - - - - - - - - - -'

#########################################################################################################

#non sono configurato
if str(configured) == "null":
    print '\nconfiguration:'

    print '0) gateway'
    print '1) host (network 1) 172.30.1.2'
    print '2) host (network 1) 172.30.1.3'
    print '3) host (network 2) 173.30.2.2'
    print '4) host (network 2) 172.30.2.3'

    print '\nchoose configuration:'
    option = raw_input()

    # prima configurazione

    # CONFIGURAZIONE GATEWAY
    if option == '0':
        option = None
        #impostazione indirizzi IP
        os.system('sudo ifconfig -v '+wlan+':1 172.30.1.1/24')
        os.system('sudo ifconfig -v '+wlan+':2 172.30.2.1/24')

        # cancella le route di default
        os.system('sudo route del default')

        # aggiunge route per vedere le reti
        os.system('sudo route add -net 172.30.1.0 netmask 255.255.255.0 gw 172.30.1.1 dev '+wlan+':1')
        os.system('sudo route add -net 172.30.2.0 netmask 255.255.255.0 gw 172.30.2.1 dev '+wlan+':2')

        # abilitare il forwarding dei pacchetti
        os.system('sudo sysctl -w net.ipv4.ip_forward=1')

        # disabilita ICMP redirect
        os.system('sudo sysctl -w net.ipv4.conf.all.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.all.send_redirects=0')

        # default
        os.system('sudo sysctl -w net.ipv4.conf.default.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.default.send_redirects=0')

        # dev wlan
        os.system('sudo sysctl -w net.ipv4.conf.'+wlan+'.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.'+wlan+'.send_redirects=0')

        # lo
        os.system('sudo sysctl -w net.ipv4.conf.lo.accept_redirects=0')
        os.system('sudo sysctl -w net.ipv4.conf.lo.send_redirects=0')

        print 'gateway configured!'
        file = open("configured.txt", "w")
        file.write("gateway")

    # CONFIGURAZIONE HOST
    elif option == '1':
        os.system('ifconfig '+wlan+' 172.30.1.2/24')
        os.system('route add default gw 172.30.1.1')
        print 'host configured!'
        file = open("configured.txt", "w")
        file.write("host")

    elif option == '2':
        os.system('ifconfig '+wlan+' 172.30.1.3/24')
        os.system('route add default gw 172.30.1.1')
        print 'host configured!'
        file = open("configured.txt", "w")
        file.write("host")

    elif option == '3':
        os.system('ifconfig '+wlan+' 172.30.2.2/24')
        os.system('route add default gw 172.30.2.1')
        print 'host configured!'
        file = open("configured.txt", "w")
        file.write("host")

    elif option == '4':
        os.system('ifconfig '+wlan+' 172.30.2.3/24')
        os.system('route add default gw 172.30.2.1')
        print 'host configured!'
        file = open("configured.txt", "w")
        file.write("host")
    else:
        print '****************** reset configuration *************************'
        file = open("configured.txt", "w")
        file.write("null")
        sys.exit(0)

#########################################################################################################

# gia configurato (configured = 1)
else:
    int_option = None

    print '* you are a '+str(configured)+' *'

    while int_option is None:

        #sono un host
        if str(configured) == "host":

            print "1) Dos Attack (ping flooding)"
            print "2) generate traffic tcp"
            print "3) generate traffic udp"
            print "4) ping"
            print "5) ssh connection"

            try:
                option1 = raw_input()
            except SyntaxError:
                option = None

            #dos attack ping flooding
            if option1 == '1':
                print "insert ip target:"
                ip = raw_input()
                print os.system('sudo ping -f '+ip)

            #generate traffic tcp with nmap
            elif option1 == '2':
                print "insert ip target:"
                TCP_IP=raw_input()
                os.system('sudo nmap -sT ' + TCP_IP)

            #generate traffic udp (client)
            elif option1 == '3':
                print "insert ip target:"
                UDP_IP = raw_input()
                UDP_PORT = 5005
                MESSAGE = "Hello, World! (UDP)"
                print "message:", MESSAGE
                while 1:
                    print "message:", MESSAGE
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
                    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                sock.close()

            #ping normale
            elif option1 == '4':
                print "insert ip target:"
                ip=raw_input()
                os.system('sudo ping '+ip)

            #connessione ssh "nome_macchina@ip_destinazione"
            elif option1 == '5':
                print "insert user@ip_address:"
                us_ip=raw_input()
                os.system('sudo ssh '+us_ip)

            else:
                print '****************** reset configuration *************************'
                file = open("configured.txt", "w")
                file.write("null")
                sys.exit(0)

            int_option=None

###########################################################################################################

        # sono un gateway
        else:
            print "IPTABLES: FILTER:"
            print "\t1) block dos Attack"
            print "\t2) block all network 172.30.1.0/24"
            print "\t3) accept for mac address"
            print "\t4) block traffic tcp"
            print "\t5) block traffic udp"
            print "IPTABLES: NAT:"
            print "\t6) prerouting"
            print "\t7) postrouting"
            print "IPTABLES: MANGLE:"
            print "\t8) change ttl"
            print "\n9) delete all iptables rules"

            try:
                option2 = raw_input()
            except SyntaxError:
                option = None

            #ping -f
            if option2 == '1':
                os.system('sudo iptables -A FORWARD -p icmp -i ra0 -m limit --limit 100/s --limit-burst 100 -j DROP')
                print 'rule iptables ON'

            #blocca rete 1
            elif option2 == '2':
                os.system('sudo iptables -A FORWARD -p icmp -i ra0 -s 172.30.1.0/24 -j DROP')
                print 'rule iptables ON'

            #permette solo mac address specificato
            elif option2 == '3':
                os.system('sudo iptables -A FORWARD -p tcp --dport 22 -m mac --mac-source e4:d5:3d:aa:7a:be -j ACCEPT')
                os.system('sudo iptables -A FORWARD -p tcp --dport 22 -j DROP')
                os.system('sudo iptables -A INPUT -p tcp --dport 22 -j DROP')
                print 'rule iptables ON'

            #blocca tcp (nmap)
            elif option2 == '4':
                os.system('sudo iptables -A INPUT -p tcp -m tcp -j DROP')

            # server udp
            elif option2 == '5':
                os.system('sudo iptables -A FORWARD -p udp -m recent --set --name UDP-PORTSCAN -j REJECT --reject-with icmp-port-unreachable')
                print 'rule iptables ON'

            #prerouting (destination)
            elif option2 == '6':
                print 'insert ip target'
                ip=raw_input()
                os.system('sudo iptables -t nat -A PREROUTING -i ra0 -j DNAT --to '+ip)
                print 'rule iptables ON'

            #postrouting (source)
            elif option2 == '7':
                print 'insert ip target'
                ip = raw_input()
                os.system('sudo iptables -t nat -A POSTROUTING -p icmp -j SNAT --to '+ip)
                print 'rule iptables ON'

            #mangle
            elif option2 == '8':
                os.system('sudo iptables -t mangle -A POSTROUTING -j TTL --ttl-inc 10')
                print 'rule iptables ON'

            #cancella sia iptables che nat che mangle
            elif option2 == '9':
                os.system('sudo iptables -F')
                os.system('sudo iptables -t nat -F')
                os.system('sudo iptables -t mangle -F')
                print 'rules iptables OFF'
                
            else:
                print '****************** reset configuration *************************'
                file = open("configured.txt", "w")
                file.write("null")
                sys.exit(0)




#visulizzare regole di nat -> sudo iptables -t nat -L






