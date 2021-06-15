#
#   dev's Twitter : @__MoonLuna__
#   project : handi bot petition for the AAH
#
###################################################



import datetime
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.dates import drange, DateFormatter, date2num, DayLocator

import CONST
import error
import utilitaries
import os

from CONST import _Const

def generate_plot(cursor):
    CONST = _Const()
    fig, ax = plt.subplots(figsize=(16, 9))
    goal_x = []
    goal_y = []
    values = []
    days = []
    date_obs = []
    c=1
    med_var=[]
    formatter = DateFormatter('%d/%m/%y')
    date1 = datetime(2021, 3, 21)
    date2 = datetime(2021, 6, 18)
    delta = timedelta(days=1)
    dates = drange(date1, date2, delta)
    for (date, nb) in cursor:  # On parcours le curseur
        values.append(nb)
        days.append(c)
        date_obs.append(date.replace(minute=0, hour=0))
        c += 1

    plt.plot(date_obs, values)
    var = utilitaries.calculate_variations(values)

    if var[len(var)-1] > 0: #Si la dernière variation est positive
        days_to_goal_last_var = utilitaries.get_x(var[len(var)-1], values[len(values) - 1], 100000) #Récupérer les jours restant pour atteindre l'objectif avec la dernière variation
        date_to_the_goal_last_var = date_obs[len(date_obs) - 1] + timedelta(days_to_goal_last_var) #On cherche la date où on arrive à 100 000 avec la dernière variation
        plt.plot(# Faire une droite avec la dernière variation en pointillé
            [date_obs[len(date_obs)-1], date_to_the_goal_last_var],
            [values[len(values) - 1], utilitaries.f(var[len(var)-1], days_to_goal_last_var, values[len(values) - 1])],
            "c--", label="ratio signatures/jour comme aujourd'hui")
    else:
        plt.plot(  # Faire une droite avec la dernière variation en pointillé
            [date2num(date_obs[len(date_obs)-1]), dates[len(dates)-1]],
            [values[len(values) - 1], utilitaries.f(var[len(var) - 1], 0, values[len(values) - 1])],
            "c--", label="ratio signatures/jour comme aujourd'hui")
    if len(var) > 7:
        for i in range(len(var) - 8, len(var) - 1):
            med_var.append(var[i])
    else:
        med_var = var
    median = utilitaries.calculate_median(med_var) #Définir la médiane des variations et en faire une droite en pointillé
    days_to_goal = utilitaries.get_x(median, values[len(values)-1], 100000)#définir le nb de jour où on arrive aux 100 000
    date_to_the_goal = date_obs[len(date_obs)-1] + timedelta(days_to_goal) #On défini la date où on arrivera aux 100 000

    plt.plot(
        [date_obs[len(date_obs)-1], date_to_the_goal],
        [values[len(values)-1], utilitaries.f(median, days_to_goal, values[len(values)-1])],
        "m--", label="ratio signatures/jour suivant la médiane") #On trace la courbe en pointillé

    for i in range(0, 89): #Génération de la droite de l'objectif
        goal_x.append(dates[i])
        goal_y.append(100000)
    plt.plot_date(goal_x,  goal_y, "g-" )

    plt.subplots_adjust(left=0.15)

    ax.set(xlabel='jours jusqu\'au 17 Juin (étude de la loi à l\'asssemblée)', ylabel='Signatutres',
       title='Objectifs') #On ajoute les légendes
    ax.grid() #On rajoute une grille pour mieux lire
    ax.set_ylim(0, 125000)#On modifie les limites de l'axe y de 0 à 25 000 de plus que l'objectif
    ax.set_xlim(dates[0], dates[len(dates)-1]) #On modifie les limites de l'axe x du 15-12-20 à la fin de la pétition le 10-03-21
    ax.xaxis.set_major_formatter(formatter) #On formate la date
    plt.margins(10)#On mets une marge
    plt.xticks(rotation=20) #On rotatione les x ticks (sait pas traduire)
    plt.legend(loc='lower right')
    if not os.path.exists(CONST.IMG_PATH+datetime.now().strftime("%d-%m-%Y")):
        os.makedirs(CONST.IMG_PATH+datetime.now().strftime("%d-%m-%Y"))
    fig.savefig(CONST.IMG_PATH+datetime.now().strftime("%d-%m-%Y")+"/2-global.png")


def generate_str_tweet(y):
    values = []
    days = []
    tweets = []
    med_var = []
    CONST = _Const()
    date_to_goal_last_var_str = ""
    today = datetime.now().strftime("%d/%m/%Y")
    date_end = datetime.strptime("2021-06-17", "%Y-%m-%d")
    date_end_date = datetime(2021, 6, 17)
    print()
    c = 1
    date_to_goal_last_var = 0

    day_before_deb = (date_end_date - datetime.now()).days

    for (d, nb) in y:  # On parcours le curseur
        values.append(nb)
        days.append(c)
        c += 1
    var = utilitaries.calculate_variations(values)
    #espacement des milliers
    nb_sign=utilitaries.spacing_int(str(y[len(y)-1][1])) #nombre de signature
    percent=str(int(y[len(y)-1][1] / 100000 * 100)) #pourcentage
    since_yesterday=utilitaries.spacing_int(str(y[len(y)-1][1] - y[len(y)-2][1])) #signature depuis hier
    to_obj=utilitaries.spacing_int(str(100000 - y[len(y)-1][1])) #signatures restantes pour arriver aux 100 000
    min_rate_to_goal = utilitaries.spacing_int(str(int((100000 - y[len(y)-1][1])/((date_end-datetime.now()).days+1))))#Signature qu'on doit avoir par jours pour atteindre l'objectif
    if var[len(var) - 1] == 0: #SI il n'y a eu aucune signature
        last_var_str = "Aujourd'hui il n'y a eu aucune signature.\n\n"
        error.manage_error(31) #On envoie un mail pour indiqué que la médiane peut pas être à 0
    else: #SINON
        days_to_goal_last_var = utilitaries.get_x(var[len(var) - 1], values[len(values) - 1], 100000) #On calucule le nombre de jours pour arriver à l'objectif avec la dernière variation
        date_to_goal_last_var = datetime.now() + timedelta(days=days_to_goal_last_var) #On calcul la date à laquelle on arrive à l'objectif avec la dernière variration
        date_to_goal_last_var_str = date_to_goal_last_var.strftime("%d/%m/%Y") #on la converti en string
        last_var_str = "Et " + utilitaries.spacing_int(str(var[len(var) - 1])) + " signatures de plus qu'hier\n\n"#On génère le texte
    if len(var) > 7:
        for i in range(len(var) - 8, len(var) - 1):
            med_var.append(var[i])
    else:
        med_var = var

    median = utilitaries.calculate_median(med_var) #On calcule la médiane

    days_to_goal = utilitaries.get_x(median, values[len(values) - 1], 100000) #On calucul le nombre de jours pour arriver à l'objectif avec la médiane
    date_to_goal = datetime.now() + timedelta(days=days_to_goal) #On calcul la date
    date_to_goal_str = date_to_goal.strftime("%d/%m/%Y") #On la converti en string

    sign_med_to_low = "Si on regarde la médiane, on y arrivera après la date du débat. " +\
                      "\n\nIl faut qu'on partage plus la pétition pour avoir plus de signatures\n\n" #Le texte si on dépasse l'objectif avec la médiane

    if date_to_goal >= date_end: #SI on dépasse l'objectif avec la médiane ALORS
        sign_med = sign_med_to_low #On l'indique
    else: #SINON
        sign_med = "Si on continue suivant la médiane, on y arrivera le " + date_to_goal_str + "\n\n" #On inqique à quelle date on ateindra l'objectif
    if (date_to_goal_last_var == 0 or date_to_goal_last_var >= date_end) and sign_med != sign_med_to_low: #SI il n'y a pas eu de signature depuis hier OU qu'on arrive pas à l'objectif avec la dernière variation mais qu'on y arrive avec la médiane ALORS
        sign_last_day = "Il nous faut plus de signatures journalières pour y arriver avant le débat\n\n" #On l'indique
    elif (date_to_goal_last_var == 0 or date_to_goal_last_var >= date_end) and sign_med == sign_med_to_low: #SI il n'y a pas eu de signature depuis hier OU qu'on arrive pas à l'objectif avec la dernière variation et qu'on y arrive pas non plus avec la médiane ALORS
        sign_last_day = "" #On ne marque rien
    else: #SINON (Si on y arrive avec la dernière variation) ALORS
        if sign_med == sign_med_to_low: #SI on n'y arrive pas avec la médiane ALORS
            sign_med = "Si on regarde la médiane, on y arrivera après la date du débat.\n\n"
            sign_last_day = "Mais si on continue comme aujourd'hui, on y arrivera le " + date_to_goal_last_var_str + "\n\n"  # On dit à quelle date on arrivera à l'objectif
        else:
            sign_last_day = "Si on continue comme aujourd'hui, on y arrivera le " + date_to_goal_last_var_str + "\n\n"



    tweets.append( #On génère les deux tweet)
        "A 20h le "+today+" et à " + str(day_before_deb) + " jours du débat pour notre autonomie : \n\n"+\
        nb_sign+" personnes ont signé. \n\n"+\
        "C'est "+percent+"% de l'objectif \n\n"+\
        last_var_str+\
        "Il reste "+to_obj+" signatures.\n\n"+ \
        "#ObjectifAutonomie #SignezPourNotreAutonomie\n\n"+\
        "https://petitions.assemblee-nationale.fr/initiatives/i-358\n\n")
    tweet_txt = open(CONST.IMG_PATH +datetime.now().strftime("%d-%m-%Y")+"/tweet.txt", "w")
    tweet_txt.write(tweets[0])
    tweet_txt.close()

    return tweets