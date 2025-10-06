import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
import requests
import time

lowFloats = {
    #Fracture

    #Kilowatt

    #Revolution

    #Prisma

    #Glove
}


def main():
    driver = start()

    time.sleep(30)

    # Initial element retrieval
    item = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ItemCardNewBody_float__mpCp4"))
    )
    auxitem = item.text  # Get initial item text

    while True:
        try:
            # Locate the current item again in the loop
            item2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ItemCardNewBody_float__mpCp4"))
            )
            auxitem2 = item2.text  # Get current item text

            # Check if the item text has changed
            if auxitem2 == auxitem:
                driver.refresh()
                time.sleep(10)
                continue

            # If the item is different, proceed
            print("Item has changed. Proceeding...")
            auxitem = auxitem2  # Update auxitem to the new value

            time.sleep(2)
            print("Buy decision:", buy)
            time.sleep(2)

            driver.back()
            time.sleep(10)

        except Exception as e:
            print(f"Error in main loop: {e}")
            driver.refresh()
            time.sleep(5)

def start():

    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)

    # Use undetected-chromedriver
    
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("window-size=1280,800")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-popup-blocking')

    stealth(driver,
        vendor="Google Inc. ",
        platform="Win32",
        webgl_vendor="intel Inc. ",
        renderer= "Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

    options.add_argument('--remote-debugging-port=9222')

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
    """
    })
    driver.execute_script("window.chrome=true")
    driver.execute_script("return navigator.userAgent")

    driver.implicitly_wait(2)

    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")


    # Initialize the undetected Chrome driver
    # Navigate to the website
    driver.get("https://gamerpay.gg/?sortBy=newest&ascending=false")

    time.sleep(5)

    return driver

    try:
        item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ItemCardNewBody_float__mpCp4"))
        )
        item.click()

        name = name_element.text
        float_value = float(float_element.text.replace("Float", "").strip())


        else:

        data = response.json()

        if data.get("data"):
            value = (data["data"][0]["price"]) / 1000
            ecb_response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
            ecb_data = ecb_response.json()
            value_in_eur = value * ecb_data["rates"]["EUR"]
            print("Price in EUR:", value_in_eur)

            if (price / value_in_eur) <= 0.70:
                return 1, item  # Decision to buy
        else:

    except Exception as e:
        print(f"Error in checkPrice: {e}")

main()