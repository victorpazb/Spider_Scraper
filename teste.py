from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()


def scraperDeutados(gender):


    def getEveryCongressman(updatedUrl, sizeOfList): 
        index = 0
        while(index < sizeOfList):
        
            driver.get(updatedUrl)
            assert 'Busca de Deputados na Câmara dos Deputados - Portal da Câmara dos Deputados' in driver.title

        
            index += 1
            xpathSFulltring = '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul/li[' + str(index) + ']/div[1]/h3/a'
            driver.find_element(By.XPATH, xpathSFulltring).click()

            ### Here is the moment to capture the data of each congressman/ woman

            # ex: x = driver.find_element(By.XPATH, xpathSFulltring).click()
            # for i in x:
            #    x.getBlauFlow
            ##### ==============================================================


            














    url = 'https://www.camara.leg.br/deputados/quem-sao/resultado?search=&partido=&uf=&legislatura=56&sexo='+gender
    driver.get(url)
    assert 'Busca de Deputados na Câmara dos Deputados - Portal da Câmara dos Deputados' in driver.title


    parentElement = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul')
    elementList = parentElement.find_elements(By.CLASS_NAME, 'lista-resultados__item')

    complement = '&pagina='
    genString = ""
    
    if(gender == "F"):
        maxPages = 5
        genString = ' DEPUTADAS'
    else:
        maxPages = 22
        genString = ' DEPUTADOS'

    x = len(elementList)
    getEveryCongressman(url, x)        
        
    
    
    pagina = 2
    while(pagina < maxPages): ##there is 22 pages for congressman or 4 pages for congresswoman
        

        updatedUrl = url + complement + str(pagina)
        driver.get(updatedUrl)
        assert 'Busca de Deputados na Câmara dos Deputados - Portal da Câmara dos Deputados' in driver.title

        parentElement = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul')
        elementList = (parentElement.find_elements(By.CLASS_NAME, 'lista-resultados__item')) ##aqui temos a captura da lista de uma pagina, nesse ponto podemos passar um 
        
        y = len(elementList)
                                                                                                ## loop nessa sublista e tirar o que queremos. e segue normalmente.
        getEveryCongressman(updatedUrl, y)                                                                               ## fiz dessa forma apenas pra ver que esta pegando todos os deputados
        
        pagina+=1
        
        
    #return arquivo.csv
    
    

        
homens = 'M'    
x = scraperDeutados(homens)


mulheres = 'F'
scraperDeutados(mulheres)

