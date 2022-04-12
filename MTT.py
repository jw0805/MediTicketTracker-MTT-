#Medis TicketTracker

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

#creates eine Liste mit allen codes die in der .txt gespeichert sind als Strings
#einzelne Codes sind durch Komma separiert
#codes müssen in der .txt in einer neuen Zeile beginnen
code_list = []

#für jeden Link wird ein neuer Eintrag in der Liste angelegt
with open(input("Speicherort der codes.txt"), 'r') as file:
    for line in file:
        code_list.extend(line.split())
file.close()

# Startet Browser
browser = webdriver.Chrome(ChromeDriverManager().install())
action = webdriver.common.action_chains.ActionChains(browser)

# Öffnet Website
browser.get('https://ticket.medimeisterschaften.com/')

# Findet Voucher Feld & Button
voucher = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="voucher"]'))
    )
button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/aside[1]/form/div/div[2]/button'))
    )
exp_url = "https://ticket.medimeisterschaften.com/?voucher_invalid"

# Code-Check-Prozess
i = 0
try:
    for i in range(len(code_list)):
        voucher = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="voucher"]'))
            )
        voucher.clear()
        voucher.send_keys(code_list[i])
        button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/aside[1]/form/div/div[2]/button'))
            )
        button.click()
        cur_url = browser.current_url
        if exp_url == cur_url:
            print(code_list[i] + " eingelöst")
            browser.back()
        else:
            browser.back()
            print(code_list[i] + " nicht eingelöst")
        i += 1
finally:
    browser.close()
