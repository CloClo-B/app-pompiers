import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from sqlalchemy import Table, Column, Integer, String, Float, MetaData

# Connexion à PostgreSQL
engine = create_engine(
    "postgresql+psycopg2://postgres:root@192.168.1.184:5432/db_fenalim"
)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

# Définition de la table si nécessaire
points_eau = Table(
    "points_eau", metadata,
    Column("id", Integer, primary_key=True),
    Column("numero_pei", String),
    Column("nom", String),
    Column("statut", String),
    Column("press_deb", Float),
    Column("debit_1_bar", Float),
    Column("geom", Geometry("POINT", srid=2154))  # Lambert 93
)

# Charger le GeoJSON
with open("api/HYDRANTS_56.json", "r") as f:
    data = json.load(f)

for feature in data["features"]:
    props = feature["properties"]
    coords = feature["geometry"]["coordinates"]
    insert_stmt = points_eau.insert().values(
        numero_pei=props.get("NUMERO_PEI"),
        nom=props.get("NOM"),
        statut=props.get("STATUT"),
        press_deb=props.get("PRESS_DEB_"),
        debit_1_bar=props.get("DEBIT_1_BA"),
        geom=f'POINT({coords[0]} {coords[1]})'
    )
    session.execute(insert_stmt)

session.commit()
session.close()
