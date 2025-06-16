from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Configurando o serviço e o driver do Chrome
service = Service('driver/chromedriver')
service.start()
driver = webdriver.Chrome(service=service)

try:
    # Abrindo o site da AcordedLab
    driver.get("http://localhost:8000")

    time.sleep(3)

    # Preenchendo e-mail e senha
    email_field = driver.find_element(By.ID, "email")
    email_field.send_keys("email@acordelab.com.br")
    password_field = driver.find_element(By.ID, "senha")
    password_field.send_keys("123senha")

    # Clicando no botão "Entrar"
    enter_button = driver.find_element(By.CLASS_NAME, "botao-login")
    enter_button.click()

    # Aguardando a validação das credenciais
    time.sleep(3)

    # Verificando se foi redirecionado para a tela principal logada
    assert "home.html" in driver.current_url

finally:
    # Fechando o navegador após 3 segundos
    time.sleep(3)
    driver.quit()
    service.stop()
