from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

SIMILAR_ACCOUNT = "other" # change this to an account of your choice
USERNAME = "starrtiprf" #change this to your username
PASSWORD = "12385279324586" #change this to your password


class InstaFollower:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        self.driver.find_element(By.NAME, "username").send_keys(USERNAME)
        self.driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)

        # Wait until the homepage loads
        WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/explore/')]"))
        )
        print("✅ Logged in successfully!")

        # Handle pop-ups
        popup_buttons = [
            "//button[contains(text(),'Not now')]",
            "//div[text()='Not now']"
        ]
        for xpath in popup_buttons:
            try:
                btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                print("Dismissed popup.")
                time.sleep(2)
            except:
                pass

    def find_followers(self):
        print("🔍 Navigating to target account...")
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")

        followers_link = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'followers')]"))
        )
        followers_link.click()
        print("📜 Followers dialog opened...")

        # Wait for the scroll box to appear (more flexible selector)
        scroll_box = None
        possible_xpaths = [
            "//div[@role='dialog']//div[contains(@class, '_aano')]",  # Common 2025 class
            "//div[@role='dialog']//div[contains(@class, '_aa_')]",   # Older class
            "//div[@role='dialog']//div[contains(@style,'overflow')]"
        ]

        for xpath in possible_xpaths:
            try:
                scroll_box = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                print(f"✅ Found scroll container using {xpath}")
                break
            except TimeoutException:
                print(f"⚠️ Could not find scroll box with {xpath}")

        if not scroll_box:
            raise Exception("❌ Could not locate followers scroll box!")

        # Scroll followers list
        for i in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_box)
            print(f"🔽 Scrolled {i+1} times")
            time.sleep(random.uniform(2, 3))

    def follow(self):
        time.sleep(3)
        follow_buttons = self.driver.find_elements(By.XPATH, "//button[normalize-space()='Follow']")
        print(f"👥 Follow buttons found: {len(follow_buttons)}")

        for index, btn in enumerate(follow_buttons):
            try:
                btn.click()
                print(f"✅ Followed user #{index + 1}")
                time.sleep(random.uniform(2, 4))
            except ElementClickInterceptedException:
                try:
                    cancel_btn = self.driver.find_element(By.XPATH, "//button[contains(text(),'Cancel')]")
                    cancel_btn.click()
                    print("⚠️ Click intercepted — canceled dialog.")
                except NoSuchElementException:
                    pass
            except Exception as e:
                print(f"⚠️ Error following user #{index + 1}: {e}")


# Run the bot
if __name__ == "__main__":
    bot = InstaFollower()
    bot.login()
    bot.find_followers()
    bot.follow()
