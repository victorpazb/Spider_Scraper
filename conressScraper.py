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
                
                xpathSFullString = '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul/li[' + str(index) + ']/div[1]/h3/a'
                
                statusXPATH = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul/li['+ str(index) + ']/div[1]/h3/span').text
        
                deputado = driver.find_element(By.XPATH, xpathSFullString)
                    
                # se for ex deputado, a página dele n deve ser aberta, nem seu detalhamento. 
                if(statusXPATH == 'Em exercício' or statusXPATH == 'Suplente que exerceu mandato'):
                    driver.find_element(By.XPATH, xpathSFullString).click() #abre cada página individual de cada congressista
                    driver.find_element(By.CLASS_NAME, 'veja-mais__item').click() #abre o detalhamento dele
                                                
                                                
            
                

            #congressMan = driver.find_element(By.XPATH, xpathSFullString).click()
            #congressMan.get_attribute(name)
            #congressMan.get_attribute(id)
            #congressMan.get_attribute(telefone)

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

    
    if(gender == "F"):
        maxPages = 5
    else:
        maxPages = 22
        
    
    x = len(elementList)
    getEveryCongressman(url, x)        
        
    
    
    complement = '&pagina='
    genString = ""    
    pagina = 2
    while(pagina < maxPages): ##there is 22 pages for congressman or 4 pages for congresswoman
        

        updatedUrl = url + complement + str(pagina)
        driver.get(updatedUrl)
        assert 'Busca de Deputados na Câmara dos Deputados - Portal da Câmara dos Deputados' in driver.title

        parentElement = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul')
        elementList = (parentElement.find_elements(By.CLASS_NAME, 'lista-resultados__item')) 
        
        y = len(elementList)
                                                                                                
        getEveryCongressman(updatedUrl, y)                                                                               
        
        pagina+=1
        
        
    #return arquivo.csv?
    
    

        
homens = 'M'    
x = scraperDeutados(homens)


mulheres = 'F'
scraperDeutados(mulheres)

