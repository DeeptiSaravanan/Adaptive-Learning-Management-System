python manage.py shell

from elearnerapp.models import Questionnaire,Question,UserAnswer
import csv
t1=Questionnaire(topic="HR5")
t1.save()
q=Questionnaire.objects.get(topic="HR5")
q.id
with open('C:\\Users\\shwet\\Desktop\\E-learner-Shwetha\\Human_unit5.csv',encoding='utf-8') as csvfile:
         reader = csv.DictReader(csvfile)
         for row in reader:
            p=Question(questionnaire=q,q_text=row['Question'],option_a=row['Option1'],option_b=row['Option2'],option_c=row['Option3'],option_d=row['Option4'],correct=row['Answer'])
            p.save()
Question.objects.filter(questionnaire=q)

qset=Question.objects.filter(questionnaire=q)
qset.filter(correct="Answer A").update(correct="A")
qset.filter(correct="Answer B").update(correct="B")
qset.filter(correct="Answer C").update(correct="C")
qset.filter(correct="Answer D").update(correct="D")
print([p.correct for p in qset])