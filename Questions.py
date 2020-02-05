from bs4 import BeautifulSoup
k = "https://www.objectivequiz.com/objective-questions/business-management/marketing-management"
import requests
html = requests.get(k).content
soup = BeautifulSoup(html)
type(soup)
z = soup.find_all('div', attrs={'class' : 'qblock'})

for z1 in z:
	qtag = z1.find_all('p')	
	for q in qtag:
		print(q.text)

	otag = z1.find_all('li')
	for o in otag:	
		print(o.text)
		

# Selenium to extract answers upon onclick

from selenium import webdriver
import time

options = webdriver.ChromeOptions()
#options.add_argument('--ignore-certificate-errors')
#options.add_argument("--test-type")
options.binary_location = "/usr/bin/chromium"
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.objectivequiz.com/objective-questions/business-management/marketing-management')

# click radio button
python_button = driver.find_elements_by_xpath("//input[@type='radio' and @class='chkans']")[0]
python_button.click()

# type text
driver.find_element_by_class_name("ctsymbol4").text

# click submit button
submit_button = driver.find_elements_by_xpath('//*[@id="editor"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[3]/input')[0]
submit_button.click()





