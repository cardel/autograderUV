from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import time

# Configuración del navegador (Chrome en este caso)
driver = webdriver.Chrome()

# Lista de correos de los usuarios

codigo_usuarios = [
2259606,
2259353,
2059962,
2259606,
2459709,
2159979,
2160364,
2160331,
2059997,
2060174,
2060257,
2160331
]
# Paso 1: Iniciar sesión en Moodle
driver.get("https://campusvirtual.univalle.edu.co/moodle/login/index.php")
driver.find_element(By.ID, "username").send_keys("cedula")
driver.find_element(By.ID, "password").send_keys("password")
driver.find_element(By.ID, "loginbtn").click()

# Esperar que se cargue la página
time.sleep(3)

# Paso 2: Navegar al curso
driver.get("https://campusvirtual.univalle.edu.co/moodle/user/index.php?id=89460")

# Paso 3: Ir a la sección de inscripciones
driver.find_element(By.XPATH, "//input[@value='Matricular usuarios']").click()  # Clic en "Matricular usuarios"
# Esperar que se abra la ventana de inscripciones
time.sleep(2)
wait = WebDriverWait(driver, 10)

# Paso 4: Inscribir usuarios
for codigo in codigo_usuarios:
    # Buscar el campo de búsqueda:
    search_box = driver.find_element(By.CSS_SELECTOR, "input[data-fieldtype='autocomplete']")
    
    # Limpiar el campo de búsqueda
    search_box.clear()
    
    # Escribir el correo del usuario
    search_box.send_keys(codigo)
    
    # Esperar que se carguen los resultados de búsqueda
    time.sleep(2)
    
    # Seleccionar el primer resultado de la lista de sugerencias (si está presente)
    search_box.send_keys(Keys.ARROW_DOWN)
    search_box.send_keys(Keys.ENTER)
    
    # Esperar un momento antes de la siguiente inscripción
    time.sleep(1)

# Paso 5: Confirmar la matriculación de los usuarios
driver.find_element(By.CSS_SELECTOR, "button[data-action='save']").click()  # Clic en "Matricular usuarios"

# Cerrar el navegador al finalizar
time.sleep(2)  # Esperar un momento para confirmar que se realizó la matriculación
driver.quit()
