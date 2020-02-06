from bs4 import BeautifulSoup
import pandas as pd

#k1 = "https://www.mcqslearn.com/bba/marketing-management/mcq/analyzing-business-markets-multiple-choice-questions-answers.php"
#k2 = "https://www.mcqslearn.com/bba/marketing-management/mcq/analyzing-consumer-markets-multiple-choice-questions-answers.php"
k = "https://www.mcqslearn.com/bba/marketing-management/mcq/competitive-dynamics-multiple-choice-questions-answers.php"
import requests
html = requests.get(k).content
soup = BeautifulSoup(html)
type(soup)
z = soup.find_all('div', attrs={'class' : 'images_content_div'})

c1 = []
c2 = []
c3 = []
c4 = []
c5 = []
c6 = []


for z1 in z:
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

dict = {'Question' : c1, 'Option1' : c2, 'Option2' : c3, 'Option3' : c4, 'Option4' : c5, 'Answer' : c6}
df = pd.DataFrame(dict)
#df.to_csv('Marketing_unit2.csv')
df.to_csv('Marketing_unit2.csv', mode='a', header=False)

#Indexing not continuous
	

#1 
#2,4,10,3
#6,11,12,14
#8,7
#5,9,13
		


		







