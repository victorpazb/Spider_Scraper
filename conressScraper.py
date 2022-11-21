from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd

driver = webdriver.Chrome()

dadosDeputados = []


def scraperDeutados(gender):

    def getEveryCongressman(updatedUrl, sizeOfList):
        index = 0
        while(index < sizeOfList):

            driver.get(updatedUrl)
            assert 'Busca de Deputados na Câmara dos Deputados - Portal da Câmara dos Deputados' in driver.title

            index += 1

            xpathSFullString = '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul/li[' + str(
                index) + ']/div[1]/h3/a'

            statusXPATH = driver.find_element(
                By.XPATH, '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul/li[' + str(index) + ']/div[1]/h3/span').text

            deputado = driver.find_element(By.XPATH, xpathSFullString)

            # se for ex deputado, a página dele n deve ser aberta, nem seu detalhamento.
            if(statusXPATH == 'Em exercício'):
                # abre cada página individual de cada congressista
                driver.find_element(By.XPATH, xpathSFullString).click()

                # CAPTURAR NOME E PRESENÇA
                nome = driver.find_element(
                    By.XPATH, '//*[@id="identificacao"]/div/div/div[3]/div/div/div[2]/div[1]/ul/li[1]').text
                print(nome)
                presenças = driver.find_element(
                    By.XPATH, '//*[@id="atuacao-section"]/div[2]/ul[2]/li[1]/dl/dd[1]').text

                dadosDeputados.append([nome, presenças])

                # abre o detalhamento dele
                driver.find_element(
                    By.XPATH, '/html/body/div[2]/div[1]/main/div[3]/div/div/div[1]/div/section[5]/ul/li[1]/div[2]/a').click()

                # AQUI COLOCA O FOREACH DE TBODY
                tabela = driver.find_element(By.TAG_NAME, 'tbody')

                for gasto in tabela.find_elements(By.TAG_NAME, 'td')[1:]:
                    dadosDeputados.append(gasto.text)

                # abre a página de gastos de gabinete
                driver.back()
                driver.find_element(
                    By.XPATH, '//*[@id="gastos-section"]/ul/li[2]/div[2]/a').click()

                # AQUI COLOCA O FOREACH DE TBODY
                tabela = driver.find_element(By.TAG_NAME, 'tbody')

                indexGabinete = 1

                for gastos in tabela.find_elements(By.TAG_NAME, 'tr'):
                    dado = gastos.find_element(
                        By.XPATH, '//*[@id="main-content"]/section/div/table/tbody/tr[' + str(indexGabinete) + ']/td[3]')
                    dadosDeputados.append(dado.text)
                    indexGabinete += 1

    url = 'https://www.camara.leg.br/deputados/quem-sao/resultado?search=&partido=&uf=&legislatura=56&sexo='+gender
    driver.get(url)
    assert 'Busca de Deputados na Câmara dos Deputados - Portal da Câmara dos Deputados' in driver.title

    parentElement = driver.find_element(
        By.XPATH, '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul')
    elementList = parentElement.find_elements(
        By.CLASS_NAME, 'lista-resultados__item')

    if(gender == "F"):
        maxPages = 5
    else:
        maxPages = 22

    x = len(elementList)
    getEveryCongressman(url, x)

    complement = '&pagina='
    genString = ""
    pagina = 22
    while(pagina < maxPages):  # there is 22 pages for congressman or 4 pages for congresswoman

        updatedUrl = url + complement + str(pagina)
        driver.get(updatedUrl)
        assert 'Busca de Deputados na Câmara dos Deputados - Portal da Câmara dos Deputados' in driver.title

        parentElement = driver.find_element(
            By.XPATH, '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul')
        elementList = (parentElement.find_elements(
            By.CLASS_NAME, 'lista-resultados__item'))

        y = len(elementList)

        getEveryCongressman(updatedUrl, y)

        pagina += 1

    # return arquivo.csv?


homens = 'M'
scraperDeutados(homens)


""" mulheres = 'F'
scraperDeutados(mulheres) """

excel = pd.DataFrame([dadosDeputados])

excel.to_csv('dadosDeputados.csv', index=False)
