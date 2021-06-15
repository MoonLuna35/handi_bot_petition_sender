#
#   dev's Twitter : @__MoonLuna__
#   project : handi bot petition for the AAH
#
###################################################
from datetime import datetime
from email.message import EmailMessage
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import dataBase
from CONST import _Const

#Ajouter une image au mail avec le path du fichier, et l'instance du message
def add_png(file, msg):
    file_name_sp = file.split("/") #On récupère le nom de l'image
    file_name = file_name_sp[len(file_name_sp)-1]

    fp = open(file, 'rb') #On l'ouvre
    img = MIMEImage(fp.read(), name=file_name) #On le lit et on l'assigne à image
    fp.close()

    msg.attach(img) #On attache l'image en pièce jointe


def add_attachments(msg):
    CONST = _Const()
    db = dataBase.concet_db()
    dataBase.make_backup(db)

    add_png(CONST.IMG_PATH + datetime.now().strftime("%d-%m-%Y") + "/2-global.png", msg)

    tweet_txt_file = CONST.IMG_PATH + datetime.now().strftime("%d-%m-%Y") + "/tweet.txt"
    fp = open(tweet_txt_file, 'r')  # On l'ouvre
    tweet_file = MIMEText(str(fp.read()))  # On le lit et on l'assigne à image
    tweet_file.add_header('Content-Disposition', 'attachment', filename="tweet.txt")
    msg.attach(tweet_file)

    backup_txt_file = CONST.IMG_PATH + datetime.now().strftime("%d-%m-%Y") + "/backup.sql"
    fp = open(backup_txt_file, 'r')  # On l'ouvre
    backup_file = MIMEText(str(fp.read()))  # On le lit et on l'assigne à image
    backup_file .add_header('Content-Disposition', 'attachment', filename="backup.sql")
    msg.attach(backup_file)

#Envoyer un mail avec si il y a une erreur, le texte, le texte du tweet, l'instance du premier tweet
def sendMail(error, text="", str_tweets=None, tweet=None):
    CONST = _Const()
    body = ""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #La date et l'heure du moment

    server = smtplib.SMTP(CONST.MAIL_STMP_SERVER, 587) #Ouverture de la connexion à Gmail
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(CONST.MAIL_ADRESS_FROM, CONST.MAIL_ADRESS_FROM_PWD) #On tente de se connecter à gmail
    msg = MIMEMultipart() #On instancie le message qui aura des pièces jointes
    if not error and tweet is not None: #SI il n'y a pas d'erreur et que l'app a tweeté ALORS
        msg['Subject'] = 'Le ' + datetime.now().strftime("%d/%m/%Y") + ' : Tout est bon' #Object pour dire que tout vas bien
        #corp du message
        body = "Coucou patronne,"+\
                         "\n\nMon script viens d\'être executé et tout c\'est bien déroulé." + \
                        "\n\nJe te copie/colle les tweets et je te mets les graphiques en pièces jointes."+\
                        "\n\nTu peut voir le tweet ici https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id) + \
                        "\n\nA demain"+\
                        "\n\nHandi Bot"
        #On ajoute les pièces jointes

        add_attachments(msg)
    elif error: #SI il y a des erreur ALORS
        msg['Subject'] = 'Le ' + datetime.now().strftime("%d/%m/%Y") + ' : Une erreur est survenue !'
        body = "Coucou patronne,\n\n" + \
               "Une erreur c\'est produite\n\n" + \
                text + "\n\n" + \
                "A demain\n\n" + \
                "Handi Bot"
    elif not error and tweet is None: #SI il n'y a pas d'erreur mais que l'application n'a pas tweeter ALORS
        msg['Subject'] = 'Le ' + datetime.now().strftime("%d/%m/%Y") + ' : Aucun Tweet'
        body = "Coucou patronne," + \
               "\n\nMon script viens d\'être executé et tout c\'est bien déroulé. Cependant je n'ai posté aucun tweet." + \
               "\n\nJe te copie/colle les tweets et je te mets les graphiques en pièces jointes." + \
               "\n\nA demain" + \
               "\n\nHandi Bot"
        add_attachments(msg)
    msg.attach(MIMEText(body, 'plain')) #on ajoute le texte


    msg['From'] = CONST.MAIL_ADRESS_FROM_NAME +"<"+CONST.MAIL_ADRESS_FROM+">" #On dit qui envoie le mail
    msg['To'] = CONST.MAIL_ADRESS_TO #et à qui on l'envoie

    server.sendmail(msg['From'], msg['To'], msg.as_string().encode("utf-8")) #On envoie le mail
    server.close()


#On formate les entier
def spacing_int(integer):
    l = list(str(integer))
    i = len(l)
    c = 0 #compteur de chiffre dans le nombre
    output_str=""
    while i >= 0: #TANT qu'il y a des chiffre dans le nombre FAIRE
        if c == 3 and i != 0: #SI le compteur est à 3 ou qu'on est à la fin du nombre
            l.insert(i, " ") #On ajoute un espace
            c = 0 #On remet le compteur à 0
        i -= 1
        c += 1
    for elem in l: #On crée la chaine de retour
        output_str += elem
    return output_str


def calculate_variations(val):
    i = 0
    var = []
    for i in range(0, len(val)-1):#POUR toute valeur jusqu'à l'avant dernière FAIRE
        var.append(val[i+1]-val[i]) #faire la différence et la stocker dans un tableau de variation
    return var


def calculate_median(var):
    var = sorted(var)
    var_len = len(var)
    if var_len < 1:
        return None
    if var_len % 2 == 0:
        return (var[int((var_len-1)/2)] + var[int((var_len+1)/2)]) / 2.0
    else:
        return var[int((var_len-1)/2)]


def get_x(a, b, y):
    return (y - b) / a


def f(a, x, b):
    return a * x + b
