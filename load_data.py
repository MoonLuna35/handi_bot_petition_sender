#
#   dev's Twitter : @__MoonLuna__
#   project : handi bot petition for the AAH
#
###################################################

from datetime import datetime

import error


def load(db):
    previous_date = -1
    cursor = db.cursor()
    query = ("SELECT date, nb FROM petition ORDER BY date")

    cursor.execute(query) #On récupère les dates et le nombre de signatures
    result = cursor.fetchall()
    if len(result) != 0: #SI On a des données
        for (date, nb) in result: #On parcours le curseur
            if date == datetime(2021, 3, 21, 0, 0):
                previous_date = date
                print(date)
            if (date - previous_date).days > 1:
                error.manage_gap(previous_date, date)
            previous_date = date
    return result
    #On retourne les données dans un tableau