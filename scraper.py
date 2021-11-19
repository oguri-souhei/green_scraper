from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Seleniumをあらゆる環境で起動させるChromeオプション
options = Options()
options.add_argument('--disable-gpu');
options.add_argument('--disable-extensions');
options.add_argument('--proxy-server="direct://"');
options.add_argument('--proxy-bypass-list=*');
options.add_argument('--start-maximized');
# options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す

DRIVER_PATH = '/Users/souhei/Downloads/chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
driver.implicitly_wait(10)

# ログインする
def login(email, password):
  email_field = driver.find_element_by_id('user_mail')
  password_field = driver.find_element_by_id('user_password')
  login_button = driver.find_element_by_name('commit')
  # フォームを入力、送信
  email_field.send_keys(email)
  password_field.send_keys(password)
  login_button.click()

# キーワードを指定して求人を検索
def search_jobs(keyword):
  search_field = driver.find_element_by_id('user_search_keyword')
  search_button = driver.find_element_by_css_selector('button.btn-orange.js-header-search-submit')
  search_field.send_keys(keyword)
  search_button.click()

# スクレイピングする
def scrape(url):
  driver.get(url)

  # 後で環境変数化！
  my_email = os.environ.get('USER_EMAIL')
  my_password = os.environ.get('USER_PASSWORD')
  login(my_email, my_password)

  # 求人を検索
  keyword = 'rails'
  search_jobs(keyword)

  jobs = driver.find_elements_by_css_selector('a.job-card__job-link')
  jobs[0].click()

  fail_count = 0

  # 応募資格がよく書かれている要素を取得
  try:
    oubosikaku = driver.find_element_by_xpath('//*[@id="js-2col-main"]/table[2]/tbody/tr[1]/th')
    print('='*30)
    print(oubosikaku.text())
  except Exception as e:
    if fail_count >= 10:
      print('='*5 + 'Error' + '='*5)
      return exit(1)
    fail_count += 1

url = 'https://www.green-japan.com/mypage01?case=login'
scrape(url)
