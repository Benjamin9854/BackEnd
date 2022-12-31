from sqlmodel import SQLModel, create_engine

engine = create_engine("postgresql:///testdb")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine) #crea la base de datos con todas las tablas declaradas anteriormentes