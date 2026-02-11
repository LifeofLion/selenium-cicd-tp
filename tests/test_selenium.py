import pytest 
import time 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service 
import os 

class TestCalculator:        
    @pytest.fixture(scope="class") 
    def driver(self): 
        """Configuration du driver Chrome pour les tests""" 
        chrome_options = Options() 

        # Configuration pour environnement CI/CD 
        if os.getenv('CI'): 
            chrome_options.add_argument('--headless') 
            chrome_options.add_argument('--no-sandbox') 
            chrome_options.add_argument('--disable-dev-shm-usage') 
            chrome_options.add_argument('--disable-gpu') 
            chrome_options.add_argument('--window-size=1920,1080') 

        service = Service("../driver/chromedriver.exe") 
        driver = webdriver.Chrome(service=service, options=chrome_options) 
        driver.implicitly_wait(10) 

        yield driver 
        driver.quit()

    def test_page_loads(self, driver): 
        """Test 1: Vérifier que la page se charge correctement""" 
        file_path = os.path.abspath("../src/index.html") 
        driver.get(f"file://{file_path}") 

        # Vérifier le titre 
        assert "Calculatrice Simple" in driver.title 

        # Vérifier la présence des éléments principaux 
        assert driver.find_element(By.ID, "num1").is_displayed() 
        assert driver.find_element(By.ID, "num2").is_displayed() 
        assert driver.find_element(By.ID, "operation").is_displayed() 
        assert driver.find_element(By.ID, "calculate").is_displayed() 

    def test_addition(self, driver): 
        """Test 2: Tester l'addition""" 
        file_path = os.path.abspath("../src/index.html") 
        driver.get(f"file://{file_path}") 

        # Saisir les valeurs 
        driver.find_element(By.ID, "num1").send_keys("10") 
        driver.find_element(By.ID, "num2").send_keys("5") 

        # Sélectionner l'addition 
        select = Select(driver.find_element(By.ID, "operation")) 
        select.select_by_value("add") 

        # Cliquer sur calculer 
        driver.find_element(By.ID, "calculate").click() 

        # Vérifier le résultat 
        result = WebDriverWait(driver, 10).until( 
            EC.presence_of_element_located((By.ID, "result")) 
        ) 
        assert "Résultat: 15" in result.text 
    
    def test_division_by_zero(self, driver): 
        """Test 3: Tester la division par zéro""" 
        file_path = os.path.abspath("../src/index.html") 
        driver.get(f"file://{file_path}") 

        # Saisir les valeurs 
        driver.find_element(By.ID, "num1").clear() 
        driver.find_element(By.ID, "num1").send_keys("10") 
        driver.find_element(By.ID, "num2").clear() 
        driver.find_element(By.ID, "num2").send_keys("0") 

        # Sélectionner la division 
        select = Select(driver.find_element(By.ID, "operation")) 
        select.select_by_value("divide") 

        driver.find_element(By.ID, "calculate").click() 

        # Vérifier le message d'erreur 
        result = WebDriverWait(driver, 10).until( 
            EC.presence_of_element_located((By.ID, "result")) 
        ) 
        assert "Erreur: Division par zéro" in result.text 

    def test_all_operations(self, driver): 
        """Test 4: Tester toutes les opérations""" 
        file_path = os.path.abspath("../src/index.html") 
        driver.get(f"file://{file_path}") 

        operations = [ 
            ("add", "8", "2", "10"), 
            ("subtract", "8", "2", "6"), 
            ("multiply", "8", "2", "16"), 
            ("divide", "8", "2", "4") 
        ] 

        for op, num1, num2, expected in operations: 
            # Nettoyer les champs 
            driver.find_element(By.ID, "num1").clear() 
            driver.find_element(By.ID, "num2").clear() 

            # Saisir les valeurs 
            driver.find_element(By.ID, "num1").send_keys(num1) 
            driver.find_element(By.ID, "num2").send_keys(num2) 

            # Sélectionner l'opération 
            select = Select(driver.find_element(By.ID, "operation")) 
            select.select_by_value(op) 

            # Calculer 
            driver.find_element(By.ID, "calculate").click() 

            # Vérifier le résultat 
            result = WebDriverWait(driver, 10).until( 
                EC.presence_of_element_located((By.ID, "result")) 
            ) 
            assert f"Résultat: {expected}" in result.text 

            time.sleep(1)
    
    def test_page_load_time(self, driver): 
        """Test 5: Mesurer le temps de chargement de la page""" 
        start_time = time.time() 

        file_path = os.path.abspath("../src/index.html") 
        driver.get(f"file://{file_path}") 

        # Attendre que la page soit complètement chargée 
        WebDriverWait(driver, 10).until( 
            EC.presence_of_element_located((By.ID, "calculator")) 
        )

        load_time = time.time() - start_time 
        print(f"Temps de chargement: {load_time:.2f} secondes") 

        # Vérifier que le chargement prend moins de 3 secondes 
        assert load_time < 3.0, f"Page trop lente à charger: {load_time:.2f}s"

    def test_decimal_numbers(self, driver):
        """Test 6: Tester avec des nombres décimaux"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        # Exemple: 10.5 + 2.25 = 12.75
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("10.5")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("2.25")

        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")

        driver.find_element(By.ID, "calculate").click()

        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )

        # Tolérance: certains affichent 12.75, d'autres 12.7500000001
        # On extrait le nombre et on compare en float.
        print(result.text)
        text = result.text.replace("Résultat:", "").strip()
        value = float(text)
        assert abs(value - 12.75) < 1e-6, f"Résultat décimal inattendu: {value}"

    def test_negative_numbers(self, driver):
        """Test 7: Tester avec des nombres négatifs"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        # Exemple: -8 - 2 = -10
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("-8")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("2")

        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("subtract")

        driver.find_element(By.ID, "calculate").click()

        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: -10" in result.text

    def test_ui_interface_styles(self, driver):
        """Test 8: Test basique de l'interface utilisateur (couleurs, tailles, lisibilité)"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        num1 = driver.find_element(By.ID, "num1")
        num2 = driver.find_element(By.ID, "num2")
        operation = driver.find_element(By.ID, "operation")
        button = driver.find_element(By.ID, "calculate")
        calculator = driver.find_element(By.ID, "calculator")

        # --- 1) Tailles "utilisables" (évite une UI minuscule ou cassée) ---
        # Champs input: hauteur/largeur minimales
        assert num1.size["height"] >= 25, f"Input num1 trop petit: {num1.size}"
        assert num1.size["width"] >= 120, f"Input num1 trop étroit: {num1.size}"
        assert num2.size["height"] >= 25, f"Input num2 trop petit: {num2.size}"
        assert num2.size["width"] >= 120, f"Input num2 trop étroit: {num2.size}"

        # Bouton: cliquable + taille raisonnable
        assert button.size["height"] >= 28, f"Bouton trop petit: {button.size}"
        assert button.size["width"] >= 90, f"Bouton trop étroit: {button.size}"

        # Container: doit être visible et non "0px"
        assert calculator.size["width"] > 200, f"Container trop étroit: {calculator.size}"
        assert calculator.size["height"] > 100, f"Container trop petit: {calculator.size}"

        # --- 2) Vérifier que des styles existent (pas tout en noir/blanc par défaut) ---
        # On accepte n'importe quelle valeur non vide, mais on refuse "transparent" / vide.
        btn_bg = button.value_of_css_property("background-color")
        btn_color = button.value_of_css_property("color")
        assert btn_bg and btn_bg != "rgba(0, 0, 0, 0)", f"Background bouton invalide: {btn_bg}"
        assert btn_color and btn_color != "rgba(0, 0, 0, 0)", f"Couleur texte bouton invalide: {btn_color}"

        # --- 3) Font-size lisible ---
        # Selenium renvoie souvent "16px"
        def px_to_float(px: str) -> float:
            return float(px.replace("px", "").strip())

        num_font = num1.value_of_css_property("font-size")
        btn_font = button.value_of_css_property("font-size")
        assert px_to_float(num_font) >= 12, f"Police input trop petite: {num_font}"
        assert px_to_float(btn_font) >= 12, f"Police bouton trop petite: {btn_font}"

        # --- 4) Alignement simple: le bouton ne doit pas être hors écran ---
        # Vérifie que le bouton est dans la fenêtre (viewport)
        x, y = button.location["x"], button.location["y"]
        assert x >= 0 and y >= 0, f"Bouton positionné bizarrement: {(x, y)}"

        # --- 5) Select visible + utilisable ---
        assert operation.is_displayed(), "Select operation non visible"
        assert operation.size["height"] >= 25, f"Select trop petit: {operation.size}"


if __name__ == "__main__": 
    pytest.main(["-v", "--html=report.html", "--self-contained-html"]) 