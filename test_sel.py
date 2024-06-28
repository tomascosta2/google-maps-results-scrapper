from selenium import webdriver

# Configurar el navegador
driver = webdriver.Chrome(executable_path='./chromedriver')

# Abrir una página web de prueba
driver.get('http://www.python.org')
print(driver.title)

# Cerrar el navegador
driver.quit()
