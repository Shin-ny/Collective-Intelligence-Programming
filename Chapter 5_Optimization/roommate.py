import random
import math


# People, along with their first and second choices
prefs=[('Toby', ('Fred', 'Andrea')),
	   ('Steve', ('Neil', 'Toby')),
	   ('Andrea', ('Suzie', 'Fred')),
	   ('Sarah', ('Toby', 'Neil')),
	   ('Dave', ('Steve', 'Sarah')),
	   ('Jeff', ('Fred', 'Laura')),
	   ('Fred', ('Jeff', 'Steve')),
	   ('Suzie', ('Andrea', 'Toby')),
	   ('Laura', ('Dave', 'Fred')),
	   ('Neil', ('Laura', 'Jeff'))]

# [(0,9), (0,8), (0,7), ... , (0,0)]
domain = [(0, len(prefs) - i - 1) for i in range(0, len(prefs))]

def printsolution(vec):
	slots=[]
	# Create two slots for each dorm
	for i in range(len(prefs)): slots += [i] # slots = [0,1,2,3,4,5,6,7,8,9]

	# Loop over each students assignment
	for i in range(len(vec) / 2):
		x = int(vec[i * 2])
		pair1 = slots[x]
		del slots[x]
		y = int(vec[i * 2 + 1])
		pair2 = slots[y]
		del slots[y]

		# Show the paired students
		print prefs[pair1][0],prefs[pair2][0]
		
		

def roommatecost(vec):
	cost = 0
	# Create a list of slots
	slots=[]
	for i in range(len(prefs)): slots += [i]

	# Loop over each student
	for i in range(len(vec) / 2):
		x = int(vec[i * 2])
		pair1 = slots[x]
		del slots[x]
		y = int(vec[i * 2 + 1])
		pair2 = slots[y]
		del slots[y]

		roommate1 = prefs[pair1][0]
		roommate2 = prefs[pair2][0]
		pref1 = prefs[pair1][1]
		pref2 = prefs[pair2][1]

		# First choice costs 0, second choice costs 1, not on the list costs 3
		if pref1[0] == roommate2: cost += 0
		elif pref1[1] == roommate2: cost += 1
		else: cost += 3

		if pref2[0] == roommate1: cost += 0
		elif pref2[1] == roommate1: cost += 1
		else: cost += 3

	return cost

























