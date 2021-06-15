#
#   dev's Twitter : @__MoonLuna__
#   project : handi bot petition for the AAH
#
###################################################
from datetime import date, datetime
import lxml.html
import urllib.request

import error
import utilitaries

def get_online_data(db):
    page = urllib.request.urlopen('https://petitions.assemblee-nationale.fr/initiatives/i-358')  # On vas sur le site de la pétition
    str_dom = page.read()  # On le lit

    root = lxml.html.fromstring(str_dom)  # On le formate en DOM
    for elem in root.xpath("//span"):  # POUR tout élément dans le DOM de type "span" FAIRE
        if "progress__bar__number" in elem.classes:  # SI l'élément courant contient le nombre de signature ALORS
            nb = int(elem.text_content().replace(" ", ""))  # On l'assigne au nombre de signature
    return nb

def get_daly_data(db):
    nb = -1
    today_midnight=datetime.now()
    today_midnight=today_midnight.replace(hour=0, minute=0, second=0, microsecond=0)

    cursor = db.cursor()#On regarde si on a déjà récupérer la date aujourd'hui
    query = "SELECT count(nb) FROM petition WHERE date >= %s"
    cursor.execute(query, (today_midnight, ))
    result = cursor.fetchall()
    if result[0][0] >= 1: #SI il y a déjà un nombre de signature pour aujourd'hui ALORS
        cursor = db.cursor()  # On récupère les données d'aujourd'hui
        query = "SELECT nb, date FROM petition WHERE date >= %s"
        cursor.execute(query, (today_midnight,))
        result = cursor.fetchall()
        error.already_data(result, db) #On gère l'erreur

    else: #SINON
        nb=get_online_data(db)
        cursor = db.cursor()  # On l'ajoute à la base de donnée avec la date du jour
        query = "INSERT INTO petition (nb, date) VALUES(%s, %s)"
        cursor.execute(query, (str(nb), str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        db.commit()


