# reset_db.py
from common.database import Base, engine

print("Suppression et création des tables...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Base de données réinitialisée.")
