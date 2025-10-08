import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
import requests
import time
import atexit

# Patch Chrome class to prevent cleanup
def _patched_quit(self, *args, **kwargs):
    pass

uc.Chrome.quit = _patched_quit
uc.Chrome.__del__ = lambda self: None

lowFloats = {
    #Fracture
    ("Galil AR | Connexion (Field-Tested)"): lambda x: 0.15 < x < 0.20,
    ("MP5-SD | Kitbash (Field-Tested)"): lambda x: 0.15 < x < 0.20,
    ("Tec-9 | Brother (Field-Tested)"): lambda x: 0.15 < x < 0.20,
    ("MAG-7 | Monster Call (Field-Tested)"): lambda x: 0.15 < x < 0.20,
    ("MAC-10 | Allure (Field-Tested)"): lambda x: 0.15 < x < 0.20,

    #Kilowatt
    ("Sawed-Off | Analog Input (Minimal Wear)"): lambda x: 0.07 < x < 0.10,
    ("M4A4 | Etch Lord (Minimal Wear)"): lambda x: 0.07 < x < 0.10,
    ("MP7 | Just Smile (Minimal Wear)"): lambda x: 0.07 < x < 0.10,
    ("Five-SeveN | Hybrid (Minimal Wear)"): lambda x: 0.07 < x < 0.10,

    #Revolution
    ("P2000 | Wicked Sick (Field-Tested)"): lambda x: 0.15 < x < 0.1875,
    ("UMP-45 | Wild Child (Field-Tested)"): lambda x: 0.15 < x < 0.1875,

    #Prisma
    ("XM1014 | Incinegator (Field-Tested)"): lambda x: 0.15 < x < 0.1875,

    #Glove
    ("G3SG1 | Stinger (Minimal Wear)"): lambda x: 0.07 < x < 0.0933,
    ("Nova | Gila (Minimal Wear)"): lambda x: 0.07 < x < 0.0933,
}


def start():
    options = uc.ChromeOptions()
    
    # Configure options first
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--window-size=1280,800")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    options.add_argument('--disable-automation')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--remote-debugging-port=9222')
    
    # Create driver with version_main parameter to match your Chrome version
    driver = uc.Chrome(options=options, version_main=140)
    
    # Prevent driver from closing
    driver._executable_path = None
    
    # Configure stealth settings
    stealth(driver,
        vendor="Google Inc. ",
        platform="Win32",
        webgl_vendor="intel Inc. ",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    
    # Configure additional driver settings
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
    
    # Navigate to website
    driver.get("https://gamerpay.gg/?sortBy=newest&ascending=false&page=1&floatMax=0.20&floatMin=0.07")
    print("Page loaded successfully")
    
    # Wait longer and check if element exists
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # Increase wait time to 20 seconds
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ItemCardBody_float__Qk2F1"))
            )
            print("Successfully found item element")
            break
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries} - Element not found yet, refreshing page...")
            if attempt < max_retries - 1:
                driver.refresh()
                time.sleep(5)
            else:
                # Don't raise error, just warn
                print("Warning: Element not found after all attempts, but continuing anyway...")
                print("You may need to verify the class name 'ItemCardBody_float__Qk2F1' is correct")
    
    return driver

def normalize_name(raw_name, float_value):
    # Remove duplicate "StatTrak™" and trim spaces
    name = raw_name.replace("StatTrak™", "").strip()

    # Add "StatTrak™" prefix if it's a StatTrak item
    if "StatTrak™" in raw_name:
        name = f"StatTrak™ {name}"

    # Determine condition based on float value
    if float_value <= 0.07:
        condition = "(Factory New)"
    elif float_value <= 0.15:
        condition = "(Minimal Wear)"
    elif float_value <= 0.38:
        condition = "(Field-Tested)"
    elif float_value <= 0.45:
        condition = "(Well-Worn)"
    else:
        condition = "(Battle-Scarred)"

    # Append condition
    name = f"{name} {condition}"

    return name

def checkPrice(driver):
    try:
        # Click the item to view details
        item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ItemCardBody_float__Qk2F1"))
        )
        item.click()

        # Attempt to extract details
        retries = 3
        name = None
        float_value = None
        
        while retries > 0:
            try:
                # Extract elements
                name_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ItemTitle_header__7a9e7"))
                )
                
                # Get name text immediately
                name = name_element.text
                
                # Try to find float element - if it doesn't exist, skip this item
                try:
                    float_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "(//div[@class='ItemDetails_row__gcoCh'])[1]"))
                    )
                    # Get float text immediately to avoid stale element
                    float_text = float_element.text
                    float_value = float(float_text.replace("Float", "").strip())
                except:
                    print("Item has no float value, skipping...")
                    return False, item
                
                break
            except Exception as e:
                retries -= 1
                if retries == 0:
                    raise
                print(f"Retrying element location due to: {e}")
                time.sleep(1)

        # Normalize name
        name = normalize_name(name, float_value)
        
        print(f"Checking: {name} with float {float_value}")

        # Check if the name exists in lowFloats and meets condition
        if name in lowFloats:
            if lowFloats[name](float_value):
                print(f"✓ BUY: '{name}' matches low float condition!")
                return True, item
            else:
                print(f"✗ Item '{name}' found but float {float_value} doesn't match condition")
        else:
            print(f"✗ Item '{name}' not in dictionary")

        return False, item

    except Exception as e:
        print(f"Error in checkPrice: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def main():
    try:
        driver = start()
        driver._healthy = False

        time.sleep(30)

        # Initial element retrieval
        auxitem = None
        while auxitem is None:
            try:
                item = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ItemCardBody_float__Qk2F1"))
                )
                auxitem = item.text
                print("Found initial item with float value")
            except:
                print("No items with float found, refreshing...")
                driver.refresh()
                time.sleep(10)

        while True:
            try:
                # Locate the current item with float
                try:
                    item2 = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "ItemCardBody_float__Qk2F1"))
                    )
                    auxitem2 = item2.text
                except:
                    print("No items with float currently visible, refreshing...")
                    driver.refresh()
                    time.sleep(10)
                    continue

                # Check if the item text has changed
                if auxitem2 == auxitem:
                    driver.refresh()
                    time.sleep(10)
                    continue

                # If the item is different, proceed
                print("\n--- New item detected ---")
                auxitem = auxitem2

                time.sleep(2)
                should_buy, item = checkPrice(driver)
                
                if should_buy:
                    print("🎯 BUY DECISION: YES")
                    # Add your buy logic here
                else:
                    print("❌ BUY DECISION: NO")
                
                time.sleep(2)
                driver.back()
                time.sleep(10)

            except Exception as e:
                print(f"Error in main loop: {e}")
                driver.refresh()
                time.sleep(5)
                
    except KeyboardInterrupt:
        print("\nScript stopped but browser will remain open")
        driver._healthy = False
        return
    except Exception as e:
        print(f"Error during startup: {e}")

main()