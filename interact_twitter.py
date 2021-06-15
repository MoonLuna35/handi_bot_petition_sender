#
#   dev's Twitter : @__MoonLuna__
#   project : handi bot petition for the AAH
#
###################################################
from datetime import datetime

import tweepy
import error
from CONST import _Const

class Twitter:
    api = None
    def __init__(self): #constructeur
        CONST = _Const()
        #On mets les paramètre d'authentification
        auth = tweepy.OAuthHandler(CONST.TWITTER_CONSUMER, CONST.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(CONST.TWITTER_ACESS_TOKEN, CONST.TWITTER_ACESS_TOKEN_SECRET)
        try:
            self.api = tweepy.API(auth) #On essaye de se connecter avec l'API
        except tweepy.TweepError as e: #SI ON LEVE UNE EXEPTION ALORS
            error.manage_error(41, e) #On gère l'erreur en envoyant l'exeption

    #Regarder si on a déjà tweeté
    def already_tweeted_today(self):
        today = datetime.today()
        today_str = today.strftime("%d/%m/%Y")
        bot_tweets = self.api.user_timeline() #récupération des derniers tweets du bot
        for (tweet) in bot_tweets: #On passe en revue ses tweetkj
            #SI il a déjà tweeté le point sur la petition ALORS
            if tweet.text.find("A 20h le " + today_str) != -1:
                error.already_tweet() #On gère l'erreur
    #Envoyer le thread avec les infos de la petition. On donne les textes du tweet
    def send_thread(self, tweets):
        CONST = _Const()
        media_ids = []
        tweet_str = "Un amandement à été déposé par LREM et le modem qui supprimerais tout espoir de déconjugalisation. \n\n" + \
                    "On doit se mobiliser"

        try:
            #On upload les graphiques
            pic2 = self.api.media_upload(CONST.IMG_PATH + datetime.now().strftime("%d-%m-%Y")+"/2-global.png")

            #On récupère leurs identifiants
            media_ids.append(pic2.media_id)

            #Accésibilité
            self.api.create_media_metadata(media_ids[0],
                                           "Le graphique des objectifs avec la date où on arrive à 100 000 signatures"
                                           "suivant la médiane sur 7 jours et le ratio signatures/jour d'aujourd'hui")
            #On tweet le premier tweet
            original_tweet = self.api.update_status(status=tweets[0],
                                 )
            self.api.update_status(status=tweet_str,
                                   in_reply_to_status_id=original_tweet.id,
                                   media_ids=media_ids)

            return original_tweet
        except tweepy.TweepError as e: #SI ON LEVE UNE EXEPTION de l'API ALORS
            error.manage_error(41, e) #On gère l'erreur en envoayant l'exeption
