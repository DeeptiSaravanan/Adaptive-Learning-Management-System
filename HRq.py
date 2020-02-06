from bs4 import BeautifulSoup
import pandas as pd

k = "https://www.mcqslearn.com/mba/hrm/performance-appraisal-rater-errors.php"

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

c=23


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
#df.to_csv('Human_unit5.csv', index=False)
df.to_csv('Human_unit5.csv', mode='a', header=False, index=False)


	


		


		







