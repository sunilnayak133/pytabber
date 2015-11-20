#Author: Sunil.S.Nayak
#Current Issues: 
# - Doesn't account for stuff like Hammer Ons, Pull Offs, Bending of Strings, etc. yet.
# - Doesn't account for what notes it'll be playing next, maybe use a different search algorithm?
# - Doesn't account for the open-string-dilemma (playing an open string 
#   after a note on a high fret doesn't necessarily mean playing stuff 
#   on frets like 1 or 2 after that are easy) - work on a better heuristic ?
#Conventions:
# - Strings are numbered from bottom to top, 0 to 5 (or how many ever). 
# - It's not only for a 6 string guitar, you can put in how many ever notes in the tuning to change the number of strings
# - Octaves are just written here without looking at a tuner, change later to make it accurate
# - No flat(b) notes are taken, just sharp(#) notes are used.
# - Fret numbers start at 0 (including open strings)
# - A max of 20 frets are assumed. Look at variable "nofrets" to change this

#the musical notes
notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
#the tuning of the guitar
tuning = ['E','A','D','G','B','E']
#the octaves of the notes corresponding to the tuning
octaves = [1,1,2,2,2,3]
#tuning and octaves set to be reversed - tabs viewed bottom to top
tuning = tuning[::-1]
octaves = octaves[::-1]
#array which will contain the notes on the fretboard	
strs = []
#number of frets
nofrets = 20

#sets up values for the fretboards
def fretmaker(tune,octa,strs):
	snew = []
	count = 0
	for i in tune:
		
		oc = octa[count]
		snew.append(i+str(oc))
		for j in range(1,nofrets):
			fret = (notes.index(i)+j)%12
			if(notes[fret])=="C":
				oc+=1
			snew.append(notes[fret]+str(oc))
		strs.append(snew)
		snew = []
		count+=1

#to see the fretboard
def showfretboard(strs):
	for i in strs:
		for j in i:
			print j," ",
		print " "

#to see the positions of a note in a string
def findnote(note,strs):
	notepos = []
	for i in strs:
		if(note in i):
			notepos.append(i.index(note))
		else:
			notepos.append(-1)
	return notepos

#joker and the thief
#solo = ["D2","G2","A2","G2","C3","D3","D2","G2","A2","G2","C3","D3"]

#stairway to heaven
solo = ["A2","C3","E3","A3","B3","E3","C3","B3","C4","E3","C3","C4","F#3","D3","A2"]

#to start the tab, with the tuning written at the side
tab = [[i] for i in tuning]

#to make the tab
def tabitoff(solo,strs):
	#first note of the solo
	starter = solo[0]

	#current position
	curpos = []
	#decide how to start the solo better, 
	#right now it just chooses open string if possible
	#or else it chooses the highest fret with the value needed
	#where = findnote(starter,strs)
	#if 0 in where:
	#	curpos = [where.index(0),0]
	#else:
	#	m = max(where)
	#	curpos = [where.index(m),m]

	#give a seed value to first position instead?
	curpos = [3,7]

	#Write the start position to the tab array	
	tabwriter(*curpos)

	#Now do the above for the rest keeping in mind the costs
	for i in solo[1:]:
		curpos = findbest(i,*curpos)
		tabwriter(*curpos)

	#Now display the tab	
	tabdisplay(tab)


#greedy findbest, doesn't work well enough.
#to find the best position for the next note 
def findbest(note,ws,wf):
	#ws - which string you're currenty on
	#wf - which fret you're currently on

	#first, find the note's positions on the fretboard
	pos_arr = findnote(note,strs)

	#costs array - to assign costs to each of these notes
	costs = []

	#current string - for the loop
	cs = 0

	#looping through all the positions of the note 
	#and assigning costs to all of them
	for i in pos_arr:
		if(i==-1):
			costs.append(1000)
		else:
			#if the new note is on the open string
			if(i==0):
				costs.append(diff(cs,ws)-0.5)
			#if the new note is on the same string	
			elif(cs==ws):
				costs.append(diff(i,wf))
			#if the new note is on the same fret of the different string
			elif(i==wf):
				costs.append(diff(cs,ws)-0.5)
			#if the new note is on a different string and different fret
			else:
				costs.append(diff(cs,ws)+diff(i,wf))
		cs+=1

	#find the minimum among the costs	
	mincost = min(costs)

	#if the minimum is 1000, then the note isn't on the fretboard
	if(mincost==1000):
		print "NOTE DOES NOT EXIST ON FRETBOARD"
		return [-1,-1]
	#else, return the new position found with the minimum cost
	else:
		ind = costs.index(mincost)
		newpos = [ind,pos_arr[ind]]
		return newpos


#difference function
def diff(a,b):
	if(a-b <0):
		return b-a
	return a-b

#to actually add the tabbing to the tab for display
def tabwriter(which_string,which_fret):
	tab[which_string].append(str(which_fret))
	for i in range(len(tab)):
		if(i!=which_string):
			tab[i].append("-")

#to display the tabs
def tabdisplay(tab):
	showfretboard(tab)


#running the program
fretmaker(tuning,octaves,strs)
showfretboard(strs)
print ""
print "Stairway To Heaven: Tab of the Intro"
print ""
tabitoff(solo,strs)
