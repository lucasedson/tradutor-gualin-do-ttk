import requests
from bs4 import BeautifulSoup
from lxml import etree
from auxiliar import session, Hash_table



def inverte_silaba(silaba):
    lista_silaba = silaba.split("-")
    
    silaba = "".join(reversed(lista_silaba))

    return silaba

def insere_palavra_gualin(indice, gualin):
    session.query(Hash_table).filter_by(id=indice).update({"gualin":gualin})
    session.commit()

def atualiza_indice(indice):
    indice = str(indice)
    with open("etl/data/indice.txt", "w") as f:
        f.write(indice)


def transforma_gualin():

    indice_atual = open("etl/data/indice.txt", "r")
    indice = indice_atual.read()
    indice = int(indice)


    for i in range(indice, 100000):


        word_atual = session.query(Hash_table).filter_by(id=indice).first()

        word = word_atual.ptbr

        if len(word) <= 2:
            try:
                insere_palavra_gualin(indice, word)
            except:
                print(f"Erro ao inserir palavra-gualin --> {word}")
        else:

            url = f"https://www.dicio.com.br/{word}"

            r = requests.get(url)

            soup = BeautifulSoup(r.text, "html.parser")

            title = soup.find("title").text
            title = title.split("|")[0].strip()

            sl = soup.select("#content > div.col-xs-12.col-sm-7.col-md-8.p0.mb20 > div.card.card-main.mb10 > div:nth-child(4) > p > b")
            list_sl = []

            silaba = ""
            

            for i in sl:
                list_sl.append(i.text)
            
            try:
                silaba = list_sl[1]
                silaba = inverte_silaba(silaba)
                print(word, "-->" ,silaba)

                insere_palavra_gualin(indice, silaba)
            except:
                pass

            # sl.split("<b>")



        # print(title)
        indice += 1
        atualiza_indice(indice)

transforma_gualin()