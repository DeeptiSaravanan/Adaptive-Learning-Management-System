from bs4 import BeautifulSoup
import pandas as pd

#k1 = "https://www.mcqslearn.com/bba/marketing-management/mcq/analyzing-business-markets-multiple-choice-questions-answers.php"
#k2 = "https://www.mcqslearn.com/bba/marketing-management/mcq/analyzing-consumer-markets-multiple-choice-questions-answers.php"
#k2 = "https://www.mcqslearn.com/bba/marketing-management/mcq/competitive-dynamics-multiple-choice-questions-answers.php"
#k2 = "https://www.mcqslearn.com/bba/marketing-management/mcq/developing-marketing-strategies-plans-multiple-choice-questions-answers.php"
#k2 = "https://www.mcqslearn.com/bba/marketing-management/mcq/collecting-information-forecasting-demand-multiple-choice-questions-answers.php"
#k3 = "https://www.mcqslearn.com/bba/marketing-management/mcq/crafting-brand-positioning-multiple-choice-questions-answers.php"
#k3 = "https://www.mcqslearn.com/bba/marketing-management/mcq/developing-pricing-strategies-multiple-choice-questions-answers.php"
#k3 = "https://www.mcqslearn.com/bba/marketing-management/mcq/identifying-market-segments-targets-multiple-choice-questions-answers.php"
#k3 = "https://www.mcqslearn.com/bba/marketing-management/mcq/product-strategy-setting-multiple-choice-questions-answers.php"
#k4 = "https://www.mcqslearn.com/bba/marketing-management/mcq/creating-longterm-loyalty-relationships-multiple-choice-questions-answers.php"
#k4 = "https://www.mcqslearn.com/bba/marketing-management/mcq/creating-brand-equity-multiple-choice-questions-answers.php"
#k5 = "https://www.mcqslearn.com/bba/marketing-management/mcq/conducting-marketing-research-multiple-choice-questions-answers.php"
#k5 = "https://www.mcqslearn.com/bba/marketing-management/mcq/designing-and-managing-services-multiple-choice-questions-answers.php"
#k5 = "https://www.mcqslearn.com/bba/marketing-management/mcq/integrated-marketing-channels-multiple-choice-questions-answers.php"

import requests
html = requests.get(k).content
soup = BeautifulSoup(html)
type(soup)
z = soup.find_all('div', attrs={'class' : 'images_content_div'})

c0 = []
c1 = []
c2 = []
c3 = []
c4 = []
c5 = []
c6 = []

c=0


for z1 in z:
	c = c+1
	c0.append(c)
	qtag = z1.find_all('p')	
	q = qtag[0].text
	c1.append(q.strip('MCQ:'))
	#a = qtag[1].text	
	c6.append(qtag[1].text)

	otag = z1.find_all('li')
	c2.append(otag[0].text)
	c3.append(otag[1].text)
	c4.append(otag[2].text)
	c5.append(otag[3].text)

dict = {'Index': c0, 'Question' : c1, 'Option1' : c2, 'Option2' : c3, 'Option3' : c4, 'Option4' : c5, 'Answer' : c6}
df = pd.DataFrame(dict)
#df.to_csv('Marketing_unit5.csv', index=False)
df.to_csv('Marketing_unit5.csv', mode='a', header=False, index=False)

#Indexing not continuous
	

#1 
#2,4,10,3
#6,11,12,14
#8,7
#5,9,13
		


		







