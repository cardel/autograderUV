from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import csv
import time
import os

# Configura tus datos
USERNAME = os.getenv("MOODLE_USERNAME")
PASSWORD = os.getenv("MOODLE_PASSWORD")
TAREA_ID = "2373158"  # Cambia por el ID real de la tarea
CSV_PATH = "rubrica.csv"  # Ruta al archivo CSV
NIVELES = [0, 5, 10, 15]  # Puntos por nivel
DESCRIPCION = (
    "Proyecto FLP 2025-I Univalle Sede Tulua"
)
NOMBRE_RUBRICA = "Proyecto FLP 2025-1"  # Nombre de la rúbrica

# Inicia navegador
driver = webdriver.Chrome()  # Asegúrate de tener el driver de Chrome instalado
wait = WebDriverWait(driver, 10)

# 1. Iniciar sesión
driver.get("https://campusvirtual.univalle.edu.co/moodle/login/index.php")
wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(USERNAME)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
driver.find_element(By.ID, "loginbtn").click()

# 2. Ir a la tarea
driver.get(
    f"https://campusvirtual.univalle.edu.co/moodle/mod/assign/view.php?id={TAREA_ID}"
)

# 3. Clic en "Calificación avanzada"
wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Calificación avanzada"))).click()

# 3.1 Revisar si rubrica esta activada, si no Cambia
try:
    select_element = wait.until(EC.presence_of_element_located((By.NAME, "setmethod")))
    select = Select(select_element)
    select.select_by_value("rubric")
    time.sleep(2)
finally:
    print("✅ Método de calificación cambiado a Rúbrica.")

# 4. Clic en "Nuevo formulario desde cero"
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".action-text"))).click()

# 5. Insertar título y descripción
wait.until(EC.presence_of_element_located((By.ID, "id_name"))).send_keys(NOMBRE_RUBRICA)
descripcion = wait.until(
    EC.presence_of_element_located((By.ID, "id_description_editoreditable"))
)
descripcion.clear()
descripcion.send_keys(DESCRIPCION)

# 6. Cargar CSV
with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)  # Saltar encabezado
    niveles_csv = headers[1:]  # Nombres de los niveles
    j = 0
    for s, row in enumerate(reader):
        criterio = row[0]
        descripciones_nivel = row[1:]
        i = s + 1

        if i > 1:
            driver.find_element(By.ID, "rubric-criteria-addcriterion").click()
            time.sleep(1)

        # Activar textarea de criterio
        pseudolink = driver.find_element(
            By.CSS_SELECTOR, f"#rubric-criteria-NEWID{i}-description-cell"
        )
        pseudolink.click()
        time.sleep(0.5)

        # Escribir el texto del criterio directamente por JS
        criterio_area = wait.until(
            EC.presence_of_element_located(
                (By.ID, f"rubric-criteria-NEWID{i}-description")
            )
        )
        driver.execute_script(
            f"document.getElementById('rubric-criteria-NEWID{i}-description').value = {
                criterio!r
            };"
        )

        # Ajustar número de niveles si faltan
        niveles_actuales = len(
            driver.find_elements(
                By.CSS_SELECTOR, f"#rubric-criteria-NEWID{i}-levels .level"
            )
        )
        while niveles_actuales < len(NIVELES):
            driver.find_element(
                By.ID, f"rubric-criteria-NEWID{i}-levels-addlevel"
            ).click()
            time.sleep(0.5)
            niveles_actuales += 1

        # Insertar descripciones y puntajes de niveles
        for it, (descripcion_nivel, puntos) in enumerate(
            zip(descripciones_nivel, NIVELES)
        ):
            # Activar textarea del nivel
            nivel_container_id = (
                f"rubric-criteria-NEWID{i}-levels-NEWID{j}-definition-container"
            )
            nivel_pseudolink = driver.find_element(By.ID, nivel_container_id)
            nivel_pseudolink.click()
            time.sleep(0.3)

            # Insertar descripción del nivel vía JS
            # #rubric-criteria-NEWID1-levels-NEWID0-definition
            textarea = wait.until(
                EC.presence_of_element_located(
                    (By.ID, f"rubric-criteria-NEWID{i}-levels-NEWID{j}-definition")
                )
            )
            driver.execute_script(
                "arguments[0].value = arguments[1];", textarea, descripcion_nivel
            )

            # Insertar puntaje
            # #rubric\[criteria\]\[NEWID1\]\[levels\]\[NEWID0\]\[score\]
            score_input = driver.find_element(
                By.NAME, f"rubric[criteria][NEWID{i}][levels][NEWID{j}][score]"
            )
            score_input.clear()
            score_input.send_keys(str(puntos))
            j += 1

# 7. Guardar rúbrica
driver.find_element(By.ID, "id_saverubric").click()
print("✅ Rúbrica creada exitosamente.")

# Cierra el navegador
driver.quit()
