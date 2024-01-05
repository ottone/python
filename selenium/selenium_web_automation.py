from selenium.webdriver import ChromiumEdge
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By 
from time import sleep
from pandas import read_csv

NUMBEO_LINK = 'https://it.numbeo.com/'

CATEGORIE = {
    'Criminalità': 'Paura che ci rubino l\'automobile',
    'Assistenza Sanitaria': 'Cordialità e gentilezza del personale sanitario',
    'Inquinamento': 'Insoddisfazione per la Nettezza Urbana'
}

df = read_csv('città_latine.csv', index_col=0, encoding='utf-8')

chrome_driver = EdgeChromiumDriverManager().install()
driver = ChromiumEdge(service=Service(chrome_driver))
driver.maximize_window()
driver.get(NUMBEO_LINK)
sleep(1)
driver.find_element(By.ID, 'accept-choices').click()

for luogo in df.index:
    driver.find_element(By.ID,'city_selector_menu_city_id').send_keys(luogo)
    sleep(2)
    driver.find_element(By.CLASS_NAME,'ui-menu-item').click()
    for categoria, indice in CATEGORIE.items():
        sleep(3)
        driver.find_element(By.XPATH, f'//span[contains(@class, "nobreak")]/a[text()="{categoria}"]').click()
        indice_tr = driver.find_element(By.XPATH,f'//td[text()="{indice}"]/parent::tr')
        valore_td = indice_tr.find_element(By.CLASS_NAME,'indexValueTd')
        df.loc[luogo][categoria] = float(valore_td.text)
df.to_csv('città_latine_compilate.csv')
