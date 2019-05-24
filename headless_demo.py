from selenium import webdriver
import time

mobileEmulation = {'deviceName': 'iPhone 6'}
option = webdriver.ChromeOptions()
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('--headless')
option.add_experimental_option('mobileEmulation', mobileEmulation)
#option.add_argument('blink-settings=imagesEnabled=false')
option.add_argument('--disable-gpu')
option.add_argument('--hide-scrollbars')
driver = webdriver.Chrome(chrome_options=option)
url = "https://www.tuoke123.cn/exploit_client/index20190429233632.html?debug_token=haha123#/house?id=29387&owner=2388&type=house&mode=2"
#driver.set_window_size(375, 812)
driver.get(url)
time.sleep(5)
print(driver.page_source)
driver.get_screenshot_as_file("test.png")
driver.quit()
