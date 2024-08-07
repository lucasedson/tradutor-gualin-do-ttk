from sqlalchemy import create_engine, Column, String, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///database.db"


Base = declarative_base()

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class Hash_table(Base):
    __tablename__ = "hash_table"
    id = Column(Integer, primary_key=True)
    ptbr = Column(String)
    gualin = Column(String)




def add_words():
    with open("etl/data/all-words.txt", "r", encoding="utf-8") as f:
        for line in f:
            try:
                if line != "\n":
                    session.add(Hash_table(ptbr=line.strip(), gualin=""))
                    print(f"Adicionada palavra {line}")

            except:
                print(f"Erro ao adicionar palavra {line}")
                break
        session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # add_words() 
    # session.close()



