#
#   dev's Twitter : @__MoonLuna__
#   project : handi bot petition for the AAH
#
###################################################

#!/usr/bin/env python3
from datetime import datetime

import compil_Data
import interact_twitter
import load_data
import get_online_data
import dataBase
import utilitaries
from CONST import _Const

CONST = _Const()
no_tweet = False #True si on veut que l'app ne tweet pas False si on veux qu'elle tweet

twitter = interact_twitter.Twitter() #Instanciaition de Twitter
if not no_tweet: #SI l'app a prévue de tweeter ALORS
    twitter.already_tweeted_today() #on regarde si on a déjà tweeté aujourd'hui

db = dataBase.concet_db() #Connexion à la base de donnée
get_online_data.get_daly_data(db) #On récupère le nombre de signature d'aujourd'hui sur le site du sénat
data = load_data.load(db) #On récupère les signatures pour tout les jours depuis le 16-12-2020
compil_Data.generate_plot(data) #On génère les graphiques
str_tweets = compil_Data.generate_str_tweet(data) #On génère le texte des tweets
db.close()

if no_tweet: #SI l'app ne tweet pas ALORS
    utilitaries.sendMail(False, str_tweets=str_tweets) #On envoie un mail
else: #SION
    tweet = twitter.send_thread(str_tweets) #On envoie les tweets
    utilitaries.sendMail(False, str_tweets=str_tweets, tweet=tweet) #On envoie un mail avec l'adresse du tweet

print (datetime.now().strftime("%d-%m-%Y %H:%M:%S"+" : Tout c'est bien déroulé.")) #On indique que tout c'est bien déroulé
#On l'indique aussi dans le log
now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
log = open(CONST.LOG_PATH + "log.log", "a")
log.write("\n" + now + " : Tout c'est bien déroulé.")
log.close()

