import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions

account = input('Get the followers from account: ')

auth = ""
password = ""

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://www.instagram.com")
print('Webdriver initialized')

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Only allow essential cookies']"))).click()
time.sleep(2)

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='username']"))).send_keys(auth)
driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
time.sleep(1)
driver.find_element(By.XPATH, "//button/div[text()='Log In']").click()

try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search']"))).send_keys(account)
    print('Successfully logged into Instagram')
except:
    print('ERROR: Login details are wrong')
    exit()

try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/%s/']" % account))).click()
    print('%s profile found' % account)
except:
    print('ERROR: %s profile not found' % account)
    exit()

number_of_followers_string = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()=' followers']/span"))).text
number_of_followers = int(number_of_followers_string.replace(",", ""))

try:
    driver.find_element(By.XPATH, "//div[text()=' followers']").click()
except:
    print('ERROR: Could not access %s followers list, the account is probably private' % account)
    exit()

scroll_bar = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='_aano']")))

print('Loading followers, expected time: %s' % str(datetime.timedelta(seconds=int(number_of_followers / 10))))
follower_names = []

for i in range(1, number_of_followers):
    try:
        follower_name = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[%d]/div[2]/div[1]/div/div/span/a/span/div' % i)))
        
        follower_names.append(follower_name.text)
        scroll_bar.send_keys(Keys.END)
    except:
        break

f = open("%s-followers.txt" % account, "w")

for i in follower_names:
    f.write("%s\n" % i)
f.close()

print('{} follower names saved in %s-followers.txt'.format(len(follower_names), account))