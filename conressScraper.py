from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import csv

driver = webdriver.Chrome()

dadosDeputadosNome = []
dadosDeputadosPresenca = []
dadosDeputadosGenero = []
dadosCotaParlamentar = []
dadosCotaGabinete = []



def scraperDeutados(gender):

    def getEveryCongressman(updatedUrl, sizeOfList, gender):
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
                
                nomeArray = nome.split(':')
                justNome = nomeArray[1]

                try:
                    presencaString = driver.find_element( 
                    By.XPATH, '//*[@id="atuacao-section"]/div[2]/ul[2]/li[1]/dl/dd[1]').text
                    
                    presencaNumberArray = presencaString.split(' ')
                    presencaNumber = presencaNumberArray[0]
                    #adicionando nome e presença ao arquivo
                    

                    intPresenca = int(presencaNumber)
                    
                    dadosDeputadosNome.append(justNome)
                    dadosDeputadosPresenca.append(intPresenca)
                    dadosDeputadosGenero.append(gender)  
                except:

                    dadosDeputadosNome.append(justNome)
                    dadosDeputadosPresenca.append(None)
                    dadosDeputadosGenero.append(gender)

                try:
                    # abre o detalhamento dele
                    driver.find_element(
                        By.XPATH, '/html/body/div[2]/div[1]/main/div[3]/div/div/div[1]/div/section[5]/ul/li[1]/div[2]/a').click()

                    totalCotaParlamentarString = driver.find_element(By.ID, 'totalFinalAgregado').text
                    totalCotaParlamentarArray = totalCotaParlamentarString.split(" ")
                    dadosCotaParlamentar.append(totalCotaParlamentarArray[1])
                except:
                    dadosCotaParlamentar.append(None)

                #sai da paginas de detalhes e volta pra pagina do deputado
                driver.back()

                
                try:
                    #abre o detalhamento do gasto de gabinete
                    driver.find_element(
                        By.XPATH, '//*[@id="gastos-section"]/ul/li[2]/div[2]/a').click()
                    
                    verbaString = driver.find_element(By.XPATH, 
                    '/html/body/div[2]/div[1]/main/section/div/table/tbody/tr[1]/td[2]').text

                    
                    verbaString = verbaString.replace('.','')
                    verbaString = verbaString.replace(',','')
                    dadosCotaGabinete.append(int(verbaString))

                except:
                    dadosCotaGabinete.append(None)
                        

            


                    
                           
                

               

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

    getEveryCongressman(url, x, gender)
    
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

        getEveryCongressman(updatedUrl, y, gender)

        pagina += 1

    


homens = 'M'
scraperDeutados(homens)


#mulheres = 'F'
#scraperDeutados(mulheres)



nomes = pd.Series(dadosDeputadosNome)
gender = pd.Series(dadosDeputadosGenero)
presenca = pd.Series(dadosDeputadosPresenca)
cotaParlamentar = pd.Series(dadosCotaParlamentar)
cotaGabinete = pd.Series(dadosCotaGabinete)

df_deputados = pd.DataFrame({ 'Nome': nomes, 'Presenças no ano': presenca, 'Gênero': gender, 'Total cota parlamentar':  cotaParlamentar, 'Cota disponivel gabinete': cotaGabinete})

df_deputados.to_csv('deputados.csv', index=False)

