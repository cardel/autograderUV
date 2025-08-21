from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import time
import os

# Configuración del navegador (Chrome en este caso)
driver = webdriver.Chrome()

# Lista de correos de los usuarios

cod_curso = "98446"

codigo_usuarios = [
    2160253,
    2459537,
    2359660,
    2569453,
    2459411,
    2379918,
    2380581,
    2380661,
    2459437,
    2359494,
    2459519,
    2067621,
    2459503,
    2510208,
    2559711,
    2569459,
    2266033,
    2459486,
    2559710,
    2459662,
    2359397,
    2569134,
    2569068,
    2459608,
    2380766,
    2510206,
    2569104,
    2380741,
    2459542,
]
# Get enviromental variables
username = os.getenv("MOODLE_USERNAME")
password = os.getenv("MOODLE_PASSWORD")

# Paso 1: Iniciar sesión en Moodle
driver.get("https://campusvirtual.univalle.edu.co/moodle/login/index.php")
driver.find_element(By.ID, "username").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.ID, "loginbtn").click()

# Esperar que se cargue la página
time.sleep(3)

# Paso 2: Navegar al curso
driver.get(
    "https://campusvirtual.univalle.edu.co/moodle/user/index.php?id=" + cod_curso
)

# Paso 3: Ir a la sección de inscripciones
driver.find_element(
    By.XPATH, "//input[@value='Matricular usuarios']"
).click()  # Clic en "Matricular usuarios"
# Esperar que se abra la ventana de inscripciones
time.sleep(2)
wait = WebDriverWait(driver, 10)

# Paso 4: Inscribir usuarios
for codigo in codigo_usuarios:
    # Buscar el campo de búsqueda:
    search_box = driver.find_element(
        By.CSS_SELECTOR, "input[data-fieldtype='autocomplete']"
    )

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
driver.find_element(
    By.CSS_SELECTOR, "button[data-action='save']"
).click()  # Clic en "Matricular usuarios"

# Cerrar el navegador al finalizar
time.sleep(2)  # Esperar un momento para confirmar que se realizó la matriculación
driver.quit()
