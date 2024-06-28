from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import csv

# Archivo CSV donde se guardarán los datos
archivo_csv = "datos_google_maps.csv"

# Configuración del navegador
driver = webdriver.Chrome()

# URL base de la búsqueda en Google Maps
url_base = 'https://www.google.com/localservices/prolist?g2lbs=AOHF13lV_LkwhH_J3OJ6QQmIOSIlzYqqMCnPe0x_SfpLZtX7BBrHHbNpwj0__0riow9aRTb2_E2sapEVspCXXJjtL93PKgeWQBRMNwl28bol1r73OBYZP1-eckc8s36PE6SsKddwfFVC&hl=es-419&gl=ar&cs=1&ssta=1&q=agencia%20de%20marketing%20chile&oq=agencia%20de%20marketing%20chile&slp=MgBSAggCYACSAakCCg0vZy8xMWJ3NGo0ejB5Cg0vZy8xMXN4MDRrcWM1Cg0vZy8xMWJ3Xzc2M3Z0Cg0vZy8xMWM1c3ZiMXAzCg0vZy8xMWZrbDBzc194Cg0vZy8xMXB2M3FkeWpfCg0vZy8xMWMxdnAyc2x3Cg0vZy8xMWd2c3Ewdmh5Cg0vZy8xMWNqa3Brc19fCgwvZy8xaG0xXzE5MWoKDS9nLzExczBzZG10eDIKDS9nLzExYjgxc2pmbTQKDS9nLzExa25jdnNtMHgKDS9nLzExZ3J2M2xrMV8KDS9nLzExcDc0c3R4MjMKDC9nLzFxNm56OWYyNAoNL2cvMTFnNnd3bjJ2eAoML2cvMXBwMnZjcnp3Cg0vZy8xMXYxOXNnNThnCg0vZy8xMWdzbW1xbHE0mgEGCgIXGRAA&src=2&serdesk=1&sa=X&ved=2ahUKEwiZyMyWwv6GAxVPmZUCHbUvBb0QjGp6BAgmEAE&scp=ChVnY2lkOm1hcmtldGluZ19hZ2VuY3kSMxISCS-vJQRBxWKWER25AhET4QUFIgVDaGlsZSoUDVj4P94VWAtrvh0f9pH1JehudtgwABoUYWdlbmNpYSBkZSBtYXJrZXRpbmciGmFnZW5jaWEgZGUgbWFya2V0aW5nIGNoaWxlKhRBZ2VuY2lhIGRlIG1hcmtldGluZw%3D%3D'

# Abrir el archivo CSV en modo escritura
with open(archivo_csv, mode='w', newline='', encoding='utf-8') as csv_file:
    # Definir los nombres de las columnas
    fieldnames = ['Nombre', 'Teléfono']
    
    # Crear el escritor CSV
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Escribir los encabezados
    writer.writeheader()
    
    # Iterar sobre los índices de página
    for i in range(0, 281, 20):
        url_with_page = url_base + "&lci=" + str(i)
        print(url_with_page)
        
        # Abrir la URL
        driver.get(url_with_page)

        # Esperar a que se cargue la página
        time.sleep(5)  # Ajusta el tiempo de espera según sea necesario

        # Obtener la página fuente y analizarla con BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Buscar los elementos relevantes en la página
        results = soup.find_all('div', class_='E94Gcd')  # Clase ficticia; ajusta según la clase real

        for result in results:
            try:
                name = result.find('div', class_='xYjf2e').text.strip()  # Clase ficticia; ajusta según la clase real
                datos_from_google = result.find_all('span', class_='hGz87c')

                phone = None
                phone_pattern = re.compile(r'\+?[\d\s\-\(\)]{7,}')
                
                for span in datos_from_google:
                    if phone_pattern.match(span.text):
                        phone = span.text
                        break

                if phone:
                    writer.writerow({'Nombre': name, 'Teléfono': phone})
                    print(f'Nombre: {name}, Teléfono: {phone}')
                else:
                    print(f'Nombre: {name}, Teléfono: No encontrado')

            except Exception as e:
                print(f'Error al extraer datos: {e}')

# Cerrar el navegador al finalizar
driver.quit()

print(f"Los datos se han guardado en {archivo_csv}")
