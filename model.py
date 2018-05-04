from sqlalchemy import *
from sqlalchemy.sql import *

# Connexion a la DB

engine = create_engine('sqlite:///baseRotonde.db', echo=True)
metadata = MetaData()


spectacle = Table('spectacle', metadata,
Column('nom', String, primary_key=True),
Column('resume', String, nullable = True),
Column('photo', String, nullable = True), #lien vers un file upload
Column('liens', String, nullable = True))

calendrier = Table('calendrier', metadata,
Column('date', String, nullable = False),
Column('nom', String, ForeignKey('spectacle.nom')),
Column('placesRestantes', Integer, nullable = False))

place = Table('places', metadata,
Column('idPlace', Integer, autoincrement=True, primary_key=True),
Column('date', String, ForeignKey('calendrier.date')),
Column('nomUser', String, nullable = False))

sessions = Table('sessions', metadata,
Column('login',String,nullable=False),
Column('password',String,nullable=False))

metadata.create_all(engine)

# Ici je definis des wrappers pour toutes les tables de la DB

class Place:
    def __init__(self,idPlace,nom,date,heure,nombre):
        self.idPlace = idPlace
        self.nom = nom
        self.date = date
        self.heure = heure
        self.nombre = nombre

    def setNombre(self,nombre):
        self.nombre = nombre

class Spectacle:
    def __init__(self, nom, resume, photos, liens):
        self.nom = nom
        self.resume = resume
        # self.prix = prix
        self.photos = photos
        self.liens = liens

    def __repr__(self):
        return "<Spectacle: %s, %s, %s>"%(self.nom, self.resume, self.prix)

class Session:
    def __init__(self, login, password):
        self.login = login
        self.password = password

    def __repr__(self):
        return "<Session: %s, %s>"%(self.login, self.password)

def connect():
    conn = engine.connect()
    return conn


# Renvoie une liste contenant tous les spectacles.
def get_spectacles():
    conn = connect()
    query = 'SELECT nom, resume, photo, liens FROM spectacle'
    result = conn.execute(query)

    spectacles = []

    for row in result:
        spectacle = Spectacle(row["nom"], row["resume"], row["photo"], row["liens"])
        spectacles.append(spectacle)

    conn.close()

    return spectacles

def get_sessions():
    conn = connect()
    query = 'select login, password from sessions'
    result = conn.execute(query)

    sessions = []

    for row in result:
        sess = Session(row["login"], row["password"])
        sessions.append(sess)

    conn.close()

    return sessions