import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
#from checkUpdate import getHash
url = ["https://scholarexpress.com/multiple-choice-questions-mcq-principles-practices-management-ppm/", 
"https://scholarexpress.com/multiple-choice-questions-mcq-principles-practices-management-ppm/2/",
"https://scholarexpress.com/multiple-choice-questions-mcq-principles-practices-management-ppm/3/",
"https://scholarexpress.com/multiple-choice-questions-mcq-principles-practices-management-ppm/4/"]

#"https://global.oup.com/uk/orc/busecon/business/combe/student/mcqs/ch01/"


options = []
ques = []
answers = []
op1 = []
op2 = []
op3 = []
op4 = []
number = list(range(1,41))

def getQuestions(url):
	html = urlopen(url)
	soup = BeautifulSoup(html, 'lxml')
	questions = soup.findAll('p')

	for q in questions:
		temp = q.get_text()
		if temp.startswith('(A)'):
			op1.append(temp[3:])
		elif temp.startswith('(B)'):
			op2.append(temp[3:])
		elif temp.startswith('(C)'):
			op3.append(temp[3:])
		elif temp.startswith('(D)'):
			op4.append(temp[3:])
		elif temp.startswith('1-(') or temp.startswith('11-(') or temp.startswith('21-(') or temp.startswith('31-('):
			ans = temp
		elif temp.startswith('1') or temp.startswith('2') or temp.startswith('3') or temp.startswith('4') or temp.startswith('5') or temp.startswith('6') or temp.startswith('7') or temp.startswith('8') or temp.startswith('9'):
			for i in range(0,len(temp)):
				if temp[i] == "-":
					break
			temp = temp[i+1:]
			ques.append(temp)
			#print(temp)

	for i in ans:
		if i.isalpha():
			answers.append(i)
	#print(answers)
	
for i in range (0,4):
	getQuestions(url[i])

dict = {'Index': number, 'Question' : ques, 'Option1' : op1, 'Option2': op2, 'Option3': op3, 'Option4': op4, 'Answer' : answers}
df = pd.DataFrame(dict)
df.to_csv("Diagnostic.csv", index = False)



#######################################Tried Seleniun code####################################

	
# from selenium import webdriver
# import time

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument("--test-type")
# options.binary_location = "/usr/bin/chromium"
# driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
# driver.get('http://codepad.org')

# # click radio button
# python_button = driver.find_elements_by_xpath("//input[@value='Submit my answers' and @type='submit']")[0]
# python_button.click()

# # type text
# text_area = driver.find_element_by_id('textarea')
# text_area.send_keys("print('Hello World')")

# # click submit button
# submit_button = driver.find_elements_by_xpath('//*[@id="editor"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[3]/input')[0]
# submit_button.click()

# check = soup.findAll('div',attrs={"class":"mcqcross"})

# print(check)
