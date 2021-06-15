#
#   dev's Twitter : @__MoonLuna__
#   project : handi bot petition for the AAH
#
###################################################
from datetime import datetime

import mysql.connector as connector

from mysql.connector import errorcode

import CONST
import error
import utilitaries
from CONST import _Const


def concet_db():  # On tente d'acceder à la base de donnée
    CONST = _Const()
    config = {
        "user": CONST.DB_NAME,
        "password": CONST.DB_PWD,
        "host": CONST.DB_HOST,
        "database": CONST.DB_DATA_BASE
    }

    try:
        cnx = connector.connect(**config)
        return cnx
    except connector.Error as err:  # SI UNE EXEPTION EST LEVEE ALORS
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:  # Si c'est une erreur de mot de passe
            error.manage_error(22)  # On gère avec le gestionaire d'erreur
        elif err.errno == errorcode.ER_BAD_DB_ERROR:  # Si la base de donnée n'existe pas
            error.manage_error(23)  # On gère avec le gestionaire d'erreur
        else:  # SI c'est une autre erreur
            error.manage_error(21)  # On gère avec le gestionaire d'erreur


def make_backup(db):
    CONST = _Const()
    cursor = db.cursor()
    query = "SELECT * FROM petition"
    c = 1
    cursor.execute(query)
    result = cursor.fetchall()
    str_backup = "-- bakup for handi_bot : " + datetime.now().strftime("%d-%m-%Y %h:%m:%s") + "\n\n" + \
                 "SET SQL_MODE = \"NO_AUTO_VALUE_ON_ZERO\";\n" + \
                 "START TRANSACTION;\n" + \
                 "SET time_zone = \"+00:00\";\n\n" + \
                 "-- Structure of table petition : \n\n" + \
                 "DROP TABLE IF EXISTS petition;\n\n " + \
                 "CREATE TABLE `petition` (\n" + \
                 "`id_petition` int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,\n" + \
                 "`date` datetime NOT NULL DEFAULT current_timestamp(),\n" + \
                 "`nb` int(11) NOT NULL\n" + \
                 ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n" + \
                 "-- Datas : \n\n" + \
                 "INSERT INTO `petition` (`id_petition`, `date`, `nb`) VALUES \n"

    for (identifier, date, nb) in result:  # On parcours le curseur
        str_backup += "(" + str(identifier)+", \'" + date.strftime("%Y-%m-%d %H:%M:%S") + "\', " + str(nb) + ")"
        if c != len(result):
            str_backup += ", \n"
        else:
            str_backup += "; \n\n"
        c += 1
    str_backup += "COMMIT;"
    backup = open(CONST.IMG_PATH + datetime.now().strftime("%d-%m-%Y") + "/backup.sql", "w")
    backup.write(str_backup)
    backup.close()

