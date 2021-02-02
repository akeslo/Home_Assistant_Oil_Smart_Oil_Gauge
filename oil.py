from selenium import webdriver
import paho.mqtt.publish as publish
from pyvirtualdisplay import Display
from webdriver_manager.chrome import ChromeDriverManager

user_name = "YOUR_SMART_OIL_USERNAME"
password = "YOUR_SMART_OIL_PASSWORD"
mqtt_server = "YOUR_MQTT_SERVER"
mqtt_user = "YOUR_MQTT_USER"
mqtt_password = "YOUR_MQTT_PASSWORD"

display = Display(visible=0, size=(800, 600))
display.start()

options = webdriver.ChromeOptions()
options.add_argument('--headless')

browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
browser.set_window_size(1440, 900)

browser.get("https://app.smartoilgauge.com/app.php")
browser.find_element_by_id("inputUsername").send_keys(user_name)
browser.find_element_by_id("inputPassword").send_keys(password)
browser.find_element_by_css_selector("button.btn").click()
browser.implicitly_wait(3)

nav = browser.find_element_by_xpath('//p[contains(text(), "/")]').text
nav_value = nav.split(r"/")
browser.quit()
print(nav_value[0])
publish.single("oilgauge/tanklevel", nav_value[0], hostname=mqtt_server, port=1883, auth={'username':mqtt_user, 'password':mqtt_password})

display.stop()
