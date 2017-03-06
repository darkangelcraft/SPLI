import os
import smtplib

# e necessario far partire il programma dal terminale con i seguenti comandi:
# sudo python main.py
#cosi facendo si hanno i permessi di root

print '\nselection:'
int_option = None
print '1) DOS Attack'
print '2) mail (IMAP)'

while int_option is None:

    try:
        option = raw_input()
    except SyntaxError:
        option = None

    #dos attack
    if option == '1':
        int_option1 = None
        print "1) ATTACKER"
        print "2) IP-TABLES"

        option1 = raw_input()
        if int_option1 == '1':
            print "insert ip target:"
            ip = raw_input()
            print os.system('sudo ping -f '+ip)
        else:
            os.system('sudo iptables -A INPUT -p tcp --dport 80 -m state --state NEW -m limit --limit 50/minute --limit-burst 200 -j ACCEPT')

    elif option == '2':
        int_option2 = None
        print "1) send mail"
        print "2) IP-TABLES"

        option2 = raw_input()
        if option2 == '1':
            print "insert ip target:"
            ip = raw_input()
            print "mail sending..."

            server = smtplib.SMTP('mailfake.gmail.com', 587)
            server.starttls()
            server.login("mailfake@gmail.com", "mailfakepassword")

            msg = "YOUR MESSAGE!"
            server.sendmail("alan.guerzi@gmail.com", "alan.guerzi@gmail.com", msg)
            server.quit()
        else:
            os.system('sudo iptables -A INPUT -s 0.0.0.0 --dport 25 -j DROP')










