import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Configuration, Sampler, Theme, Instrument, ParamSong

# Configurar la base de datos
DATABASE_PATH = 'pyjama_data.db'
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

def delete_database():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print(f'Database {DATABASE_PATH} has been deleted.')
    else:
        print(f'Database {DATABASE_PATH} does not exist.')

def create_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print('Database has been created.')
    return engine

def seed_data(session):
    # Aquí puedes agregar datos iniciales si es necesario
    print('Seeding data...')
    config1 = Configuration(name='Config1', port='5000', active=True)
    config2 = Configuration(name='Config2', port='5001', active=False)
    session.add(config1)
    session.add(config2)
    session.commit()
    print('Data seeded.')

def main():
    delete_database()
    engine = create_database()
    Session = sessionmaker(bind=engine)
    session = Session()
    seed_data(session)
    session.close()
    print('Done.')

if __name__ == '__main__':
    main()
