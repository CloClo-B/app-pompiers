from sqlalchemy.orm import Session
from ..models import Signaler
from geoalchemy2.elements import WKTElement
from sqlalchemy import func, text

# from app import models, schemas
# from typing import Dict, Any

# Récupérer tous les signaler
def get_all_signale(db: Session):
    singale = db.query(
        Signaler.id_point,
        Signaler.probleme,
        Signaler.photo,
    ).all()
    # Transformer les tuples pour que le response_model fonctionne bien
    return [
        {
            "id_point": p.id_point,
            "probleme": p.probleme,
            "photo": p.photo,
 

        }
        for p in singale
    ]


def creer_signale(db: Session, payload):

    new_signale = Signaler(
        id_point=payload.id_point,
        probleme=payload.probleme,
        photo=payload.photo,
    )
    db.add(new_signale)
    db.commit()
    db.refresh(new_signale)
    return new_signale

