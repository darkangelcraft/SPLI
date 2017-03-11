import os
import smtplib
import socket

#BISOGNA INSTALLARE QUESTO PACCHETTO!!!
# sudo apt-get install python2.7
# sudo apt-get install python-pip
# sudo aptitude install python2.7-setuptools
# sudo aptitude install python2.7-dev
# sudo pip install netifaces
import netifaces as ni

# e necessario far partire il programma dal terminale con i seguenti comandi:
# sudo python main.py
#cosi facendo si hanno i permessi di root

#########################################################################################################

#variabile statica globale, mi serve per sapere se ho settato l'ip giusto
configured=0

#il mio indirizzo IP
print 'Name wireless interface:'
wlan = "wlan0" # <- - - - - - - - - - - - - - -  [MODIFICARE INTERFACCIA WIFI]

ni.ifaddresses(wlan)
myIP = ni.ifaddresses(wlan)[2][0]['addr']
print '- - - - - - - - - - '+myIP+' - - - - - - - - - - - \n'

print os.system('iwconfig | grep '+wlan)
print '- - - - - - - - - - - - - - - - - - - - - - - - - -'

#########################################################################################################

if not str(myIP).__contains__('172.30.'):
    print '\nconfiguration:'

    print '0) gateway'
    print '1) host (network 1) 172.30.1.2'
    print '2) host (network 1) 172.30.1.3'
    print '3) host (network 2) 173.30.2.2'
    print '4) host (network 2) 172.30.2.3'

    print '\nchoose configuration:'
    option = raw_input()

    # prima configurazione
    if configured==0:

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

            # cancella tutte le regole di iptables
            os.system('sudo iptables -F')

            print 'gateway configured!'
            configured=1

        # CONFIGURAZIONE HOST
        elif option == '1':
            os.system('ifconfig '+wlan+' 172.30.1.2/24')
            os.system('route add default gw 172.30.1.1')
            print 'host configured!'
            configured = 1
        elif option == '2':
            os.system('ifconfig '+wlan+' 172.30.1.3/24')
            os.system('route add default gw 172.30.1.1')
            print 'host configured!'
            configured = 1
        elif option == '3':
            os.system('ifconfig '+wlan+' 172.30.2.2/24')
            os.system('route add default gw 172.30.2.1')
            print 'host configured!'
            configured = 1
        elif option == '4':
            os.system('ifconfig '+wlan+' 172.30.2.3/24')
            os.system('route add default gw 172.30.2.1')
            print 'host configured!'
            configured = 1
        else:
            print 'selection not exist!'

#########################################################################################################

# gia configurato
else:
    int_option = None

    while int_option is None:

        print '\n1) Attacker'
        print '2) Defender'

        try:
            option = raw_input()
        except SyntaxError:
            option = None

        # attacker
        if option == '1':
            print "1) Dos Attack"
            print "2) traffic tcp"
            print "3) traffic udp"

            option1 = raw_input()

            #dos attack
            if option1 == '1':
                print "insert ip target:"
                ip = raw_input()
                print os.system('sudo ping -f '+ip)

            #generate traffic tcp (client)
            elif option1 == '2':
                print "insert ip target:"

                TCP_IP=raw_input()
                TCP_PORT = 5005
                BUFFER_SIZE = 1024

                while 1:
                    MESSAGE = "Hello, World! (TCP)"
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((TCP_IP, TCP_PORT))
                    s.send(MESSAGE)
                    data = s.recv(BUFFER_SIZE)
                    s.close()
                print "received data:", data

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



            int_option=None

###########################################################################################################

        # defender
        elif option == '2':
            print 'using IPTABLES for:'
            print "1) Dos Attack"
            print "2) block traffic tcp"
            print "3) block traffic udp"

            option2 = raw_input()
            if option2 == '1':
                os.system('sudo iptables -A INPUT -p tcp --dport 80 -m state --state NEW -m limit --limit 50/minute --limit-burst 200 -j ACCEPT')

            #server tcp
            elif option2 == '2':
                print 'insert ip client:'

                TCP_IP = raw_input()
                TCP_PORT = 5005
                BUFFER_SIZE = 20  # Normally 1024, but we want fast response

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((TCP_IP, TCP_PORT))

                while 1:
                    s.listen(1)
                    conn, addr = s.accept()
                    data = conn.recv(BUFFER_SIZE)
                    print "received data:", data
                    conn.send(data)  # echo
                    conn.close()

            # server udp
            elif option2 == '3':
                print 'insert ip client:'

                UDP_IP = raw_input()
                UDP_PORT = 5005
                sock = socket.socket(socket.AF_INET,  # Internet
                socket.SOCK_DGRAM)  # UDP
                sock.bind((UDP_IP, UDP_PORT))

                while True:
                    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
                    print "received message:", data










