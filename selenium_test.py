from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import scrapy

driver = Chrome()

def main():
    

    driver.get("https://www.baidu.com/")
    WebDriverWait(driver, 10).until(lambda d : "百度" in d.title)
    print(driver.find_element(By.XPATH, '//*[@id="s-top-left"]').text)

if __name__ == "__main__":
    main()
