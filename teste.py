from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

url = 'https://www.camara.leg.br/deputados/quem-sao/resultado?search=&partido=&uf=&legislatura=56&sexo=M'

driver.get(url)
assert 'Busca de Deputados na Câmara dos Deputados - Portal da Câmara dos Deputados' in driver.title



parentElement = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul')
                                                  
                                                
elementList = parentElement.find_elements(By.CLASS_NAME, 'lista-resultados__item')



print(len(elementList)) ##len = 25 (deputados na primeira pagina)

complement = '&pagina='
pagina = 2
while(pagina < 22): ##there is 22 pages for male congressman 
    
    driver.get(url + complement + str(pagina))
    assert 'Busca de Deputados na Câmara dos Deputados - Portal da Câmara dos Deputados' in driver.title

    parentElement = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/main/div[5]/div/div/section/ul')
    elementList += (parentElement.find_elements(By.CLASS_NAME, 'lista-resultados__item'))
    
    pagina+=1
    


print(len(elementList)) ##len = 50? (deputados)
