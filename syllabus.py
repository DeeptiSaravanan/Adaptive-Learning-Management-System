#!/usr/bin/env python
class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None


class Topics(object):
	def __init__(self,name,topics):
		self.name = name
		self.topics = topics
	def display_topics(self):
			print(self.name)
			print(self.topics)
	
class Node(object):
	def __init__(self,name,units):
		self.name = name  #This is the main three topics
		self.units = units  #This will be a dictionary with units and topics
	def display_units(self):
		print(self.name)
		for i in self.units:
			print(i)
			for j in self.units[i]:
				j.display_topics()
				print("\n")
			print("\n")
        
def Readfile(filename):
	lineList = [line.rstrip('\n') for line in open(filename)]
	return lineList

root = Tree()

Introduction = Topics("Introduction", Readfile("Basics_unit1.txt"))
Planning = Topics("Planning", Readfile("Basics_unit2.txt"))
Organising = Topics("Organising", Readfile("Basics_unit3.txt"))
Directing = Topics("Directing", Readfile("Basics_unit4.txt"))
Controlling = Topics("Controlling", Readfile("Basics_unit5.txt"))

Dict1 = {'Easy': [Introduction, Planning], 'Medium': [Organising, Directing], 'Hard': [Controlling]}
root.data = Node("Basics of Management",Dict1)
 


root.left = Tree()

Perspectives = Topics("Perspectives", Readfile("HR_unit1.txt"))
BestFit = Topics("BestFit", Readfile("HR_unit2.txt"))
Training = Topics("Training", Readfile("HR_unit3.txt"))
EmpInterest = Topics("EmpInterest", Readfile("HR_unit4.txt"))
Evaluation = Topics("Evaluation", Readfile("HR_unit5.txt"))

Dict2 = {'Easy' : [Perspectives, BestFit], 'Medium': [Training, EmpInterest], 'Hard': [Evaluation]}
root.left.data = Node("Human Resource Management",Dict2)


root.right = Tree()

Intro_marketing = Topics("Intro_marketing", Readfile("MM_unit1.txt"))
Strategy = Topics("Strategy", Readfile("MM_unit2.txt"))
MixDecisions = Topics("MixDecisions", Readfile("MM_unit3.txt"))
Behaviour = Topics("Behaviour", Readfile("MM_unit4.txt"))
Trends = Topics("Trends", Readfile("MM_unit5.txt"))

Dict3 = {'Easy' : [Intro_marketing], 'Medium' : [Strategy, MixDecisions], 'Hard' : [Behaviour, Trends]}
root.right.data = Node("Marketing Management",Dict3)
 

root.data.display_units()
print("\n")
root.left.data.display_units()
print("\n")
root.right.data.display_units()

