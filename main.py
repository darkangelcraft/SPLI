# e necessario far partire il programma dal terminale con i seguenti comandi:
# sudo python main.py
#cosi facendo si hanno i permessi di root

import os
import socket
import netifaces as ni

#########################################################################################################

#file = open("configured.txt", "w")
#file.write("null")

#variabile statica globale, mi serve per sapere se ho settato l'ip giusto
file = open("configured.txt", "r")
configured = file.read()

#il mio indirizzo IP
#print 'Name wireless interface:'
wlan = "en1" # <- - - - - - - - - - - - - - -  [MODIFICARE INTERFACCIA WIFI]

#prima configurazione
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
    print '- - - - - - - - - - - - - - - - - - - - - - - - - -'

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

    #########################################################################################################

# gia configurato (configured = 1)
else:
    int_option = None

    print '* you are a '+str(configured)+' *'

    while int_option is None:

        #sono un host
        if str(configured)=="host":

            print "1) Dos Attack (ping flooding)"
            print "2) generate traffic tcp"
            print "3) generate traffic udp"
            print "4) ping"
            print "\n5) open tcpdump"

            try:
                option1 = raw_input()
            except SyntaxError:
                option = None

            #dos attack
            if option1 == '1':
                print "insert ip target:"
                ip = raw_input()
                print os.system('sudo ping -f '+ip)

            #generate traffic tcp with nmap (client)
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
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
                    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

            elif option1 == '4':
                print "insert ip target:"
                ip=raw_input()
                os.system('sudo ping '+ip)

            elif option1 == '5':
                os.system('sudo tcpdump')

            else:
                print '****************** reset configuration *************************'
                file = open("configured.txt", "w")
                file.write("null")

            int_option=None

###########################################################################################################

        # sono un gateway
        else:
            print "IPTABLES FOR BLOCK:"
            print "\t1) block dos Attack"
            print "\t2) block traffic tcp"
            print "\t3) block traffic udp"
            print "IPTABLES FOR NAT:"
            print "\t4) prerouting"
            print "\t5) postrouting"
            print "IPTABLES FOR MANGLE:"
            print "\t6) mangle"
            print "\n7) delete all iptables rules"

            try:
                option2 = raw_input()
            except SyntaxError:
                option = None

            #icmp
            if option2 == '1':
                os.system('sudo iptables -a INPUT -p icmp -i ra0 -j DROP')
                os.system('sudo iptables -a forward -p icmp -i ra0 -s 172.30.1.2 -j DROP')
                os.system('sudo iptables -a forward -p icmp -i ra0 -s 172.30.1.0/24 -j DROP')
                print 'rule iptables ON'

            #server tcp
            elif option2 == '2':
                os.system('')

            # server udp
            elif option2 == '3':
                os.system('sudo iptables -A FORWARD -p udp -m recent --set --name UDP-PORTSCAN -j REJECT --reject-with icmp-port-unreachable')
                print 'rule iptables ON'

            #prerouting (destination)
            elif option2 == '4':
                print 'insert ip target'
                ip=raw_input()
                os.system('sudo iptables -t nat -A PREROUTING -i ra0 -j DNAT --to '+ip)
                print 'rule iptables ON'

            #postrouting (source)
            elif option2 == '5':
                print 'insert ip target'
                ip = raw_input()
                os.system('sudo iptables -t nat -A POSTROUTING -p icmp -j SNAT --to '+ip)
                print 'rule iptables ON'

            #mangle
            elif option2 == '6':
                os.system('sudo iptables -t mangle -A POSTROUTING -j TTL --ttl-inc 10')
                print 'rule iptables ON'

            #cancella sia iptables che nat che mangle
            elif option2 == '7':
                os.system('sudo iptables -F')
                os.system('sudo iptables -t nat -F')
                os.system('sudo iptables -t mangle -F')
                print 'rules iptables OFF'

            else:
                print '****************** reset configuration *************************'
                file = open("configured.txt", "w")
                file.write("null")




#visulizzare regole di nat -> sudo iptables -t nat -L






