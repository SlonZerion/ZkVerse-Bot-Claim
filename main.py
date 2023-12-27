import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ChromeOptions
from config import *
from loguru import logger
from utils import *

logger.add('log.log', format="<yellow>{time:YYYY-MM-DD at HH:mm:ss}</yellow> | <level>{level}</level>: <level>{message}</level>")


def main(private_key: str):
    for t in range(MAX_TRIES):
        logger.info(f"{private_key[:10]}... Try {t+1}/{MAX_TRIES}") 
        try:
            global ref_code
            with get_chromedriver() as driver:
                driver.get('https://airdrop.zkverse.gg/')
                switch_to_window_title(driver, 'Phantom Wallet')
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid = 'create-wallet-button']"))).click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input')))
                inputs = driver.find_elements(By.XPATH, "//input")
                inputs[0].send_keys("password123456")
                inputs[1].send_keys("password123456")
                inputs[2].click()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid = 'onboarding-form-submit-button']"))).click()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@data-testid = 'onboarding-form-saved-secret-recovery-phrase-checkbox']"))).click()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid = 'onboarding-form-submit-button']"))).click()
                driver.get('chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/popup.html')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid = 'settings-menu-open-button']"))).click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid = 'sidebar_menu-button-add_account']"))).click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[6]/div/div/div/div[4]"))).click()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name = 'name']"))).send_keys("wallet")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//textarea[@name = 'privateKey']"))).send_keys(private_key.strip())
                sleep(random.uniform(1, 3))
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@type = 'submit']"))).click()
                sleep(random.uniform(2, 5))
                driver.close()
                sleep(random.uniform(1, 3))
                switch_to_window_title(driver, 'Fragments Airdrop')
                sleep(random.uniform(1, 3))
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//video"))).click()
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class = 'wallet-adapter-button ']"))).click()
                switch_to_window_title(driver, 'Phantom Wallet')
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@type = 'submit']"))).click()
                switch_to_window_title(driver, 'Fragments Airdrop')
                sleep(random.uniform(4, 5))
                try:
                    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//p[text() = 'Open Referral Panel']"))).click()
                    logger.info(f"{private_key[:10]}... has already been registered")
                    try:
                        ref_code = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[@class = 'text-center ref__code text-white']"))).text
                        logger.success(f"{private_key[:10]}... Get referal-code: {ref_code}") 
                    except:
                        raise ValueError("Fail get referal-code")
                    return
                except:
                    pass
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type = 'text']"))).send_keys(ref_code)
                logger.info(f"{private_key[:10]}... used referal-code {ref_code}") 
                sleep(random.uniform(2, 4))
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[text() = 'Submit Code']"))).click()
                sleep(random.uniform(15, 30))
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'button']"))).click()
                switch_to_window_title(driver, 'Phantom Wallet')
                sleep(random.uniform(1, 2))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type = 'submit']"))).click()
                sleep(random.uniform(30, 40))
                switch_to_window_title(driver, 'Fragments Airdrop')
                try:
                    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "//p[text() = 'Open Referral Panel']"))).click()
                    logger.info(f"{private_key[:10]}... has already been registered")
                    try:
                        ref_code = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[@class = 'text-center ref__code text-white']"))).text
                        logger.success(f"{private_key[:10]}... Get referal-code: {ref_code}") 
                    except:
                        raise ValueError("Fail get referal-code")
                    return
                except:
                    raise ValueError("Fail claim")
            break
        except:
            ex = get_error_message()
            logger.error(f"{private_key[:10]}... Try {t+1}/{MAX_TRIES} Error: {ex}")
        
    
if __name__ == '__main__':
    ref_code = REF_CODE
    console = Console()
    print_welcome()
    logger.info("START")

    with open("private_keys.txt", "r") as f:
        private_keys = f.read().splitlines()
        while "" in private_keys:
            private_keys.remove("")

    for private_key in private_keys:
        main(private_key)
            
        address_wait_time = random.randrange(NEXT_ADDRESS_MIN_WAIT_TIME*60, NEXT_ADDRESS_MAX_WAIT_TIME*60)
        with console.status(f"[bold green]Wait {address_wait_time}s", spinner="simpleDotsScrolling") as status:
            sleep(address_wait_time)

    logger.info("FINAL")

    
