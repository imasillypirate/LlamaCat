import io
import random 
import numpy as np
import pickle
import time
from tkinter import *
import tkMessageBox, tkFileDialog

def isInt(num):
#return True if num can be converted into an integer, False otherwise
	try:
		int(num)
		return True
	except ValueError:
		return False
		
def FilTypeChecker(path,ext):
#check if path ends in ext
	splitted = path.split('.')
	if splitted[-1] == ext:
		return True
	else:
		return False
		
def splitLine(textSL):
	#given a string textSL, will return a list of the words and punctuation marks as their own elements in order.
	punct = ['.',',','!','?','"','-',';']
	initSL = textSL.split(' ')
	returnSL = []
	tempreturnSL = []
	probIndex = []
	for iSL in range(len(initSL)):
		for pSL in punct:
			if (pSL in initSL[iSL]) and (initSL[iSL] != pSL): #if the word has a punctuation attached to it
				probIndex.append(iSL)
				tempLS = list(initSL[iSL])
				ltemp = len(tempLS)
				
				pLoc = tempLS.index(pSL)#location of punctuation in list
				
				if (pLoc == 0):#punctuation is 1st character
					tempreturnSL.append([pSL,''.join(tempLS[1:ltemp])])
				elif (pLoc == ltemp-1):#punctuation is last character
					tempreturnSL.append([''.join(tempLS[0:ltemp-1]),pSL])
				else: #punctuation midword somewhere
					tempreturnSL.append([''.join(tempLS[0:pLoc]),pSL,''.join(tempLS[pLoc+1:ltemp])])
			
	if (len(probIndex) == 0):
		returnSL = [kSL for kSL in initSL]
	else:
		cSL = 0
		for jSL in range(len(initSL)):
			if jSL not in probIndex:
				returnSL.append(initSL[jSL])
			else:
				for j2SL in tempreturnSL[cSL]:
					returnSL.append(j2SL)
				cSL+=1
	return returnSL
	
def mkWordList(h,l2s):
#h = file name of txt to read in
#l2s = lines to skip at the beginning of the document
#returns a list of words used in the work as wordList
#  probGrid which is a dictionary with a key for every word corresponding to a
#           list containing a 0 for every word in wordList
#depends on splitLine()
	text = open(h,'r')
	punct = ['.',',','!','?','"','-',';']
	c = 0
	wordList = []
	probGrid = {}
	l2s = int(l2s)
	for line in text:
		if (c<l2s):
			pass #skip first l2s lines
			
		else:
			line = line.strip()
			#line = line.strip('\n')
			spLine = splitLine(line)
			for word in spLine:
				if (word not in wordList) and (word !=''):
					wordList.append(word)
		
		c+=1
		
	text.close()
	for word in wordList:
		probGrid.update({word:[0 for k in wordList]})
		
	return wordList, probGrid

	
def readUp(hT,sT,wordsT,probGridT):
#Fills in probabilities in probGridT from file named hT with words in wordsT. Skips first sT lines of hT.
	text = open(hT,'r')
	punct = ['.',',','!','?','"','-',';']
	c = 0
	lastWord = ''
	currentWord = ''
	sT = int(sT)
	for line in text:
		if (c<sT):
			pass #skip first l2s lines
		else:
			line = line.strip()
			spLine = splitLine(line)
			for word in spLine:
				if (lastWord == ''):#we are on the first word
					lastWord = word
				else:
					if word != '':
						currentWord = word
						wLoc = wordsT.index(currentWord)#location of current word in lists
						probGridT[lastWord][wLoc] +=1
						lastWord = currentWord #prepare to move to next word, even if on next line
		
		c+=1
		
	text.close()
	#normalize probabilities for each word
	for wordRU in wordsT:
		sumP = sum(probGridT[wordRU])
		if (sumP ==0):
			pass
		else:
			probGridT[wordRU] = [1.*k/sumP for k in probGridT[wordRU]]
	
	return probGridT

def writeChain(nW,wordListWC,seed,probGridWC):
#nW = number of words (or punctuation marks) to appear in message.
#wordListWC = list of words for probGridWC
#seed = first word for message. seed MUST be in wordListWC
#probGridWC = probability grid as formatted by mkWordList() and populated by readUp()
	message = seed
	lastWord = seed
	for iWC in range(nW-1):
		#print lastWord, sum(probGridWC[lastWord])
		newWord1 = np.random.choice(wordListWC,1,p = probGridWC[lastWord])
		newWord = newWord1[0]
		message += ' '+newWord
		lastWord = newWord
	return message 
	
def quit1():
	#close window and quit
	top.destroy()
	raise SystemExit(0)
	
def quit2():
	#close window and quit
	#has.destroy()
	raise SystemExit(0)
	
def help1():
	#Display help message for first page about loading libraries
	HelpMess = "-This program reads in a text, and uses it to create a Markov Chain before it can create gibberish of the style found in said text.\n"
	HelpMess += "-The library generated during this reading can be saved as a .pkl file and reused. If you would like to load an existing, click 'Load' and select the .pkl file.'\n"
	HelpMess += "-If you would like to update an existing library, load it first, then updating will be a later option.\n"
	HelpMess += "-If you would like to create a new library, click 'Read,' then select a .txt containing the text to read.\n"
	HelpMess += "-There is a field just before the Read button labeled 'Lines to skip.' If you enter a number there, the reader will skip the first this many lines before reading. "
	HelpMess += "This may be benificial if you have introductory information at the beginning that is not part of the text (as is common for Project Gutenberg texts).\n\n"
	HelpMess += "-This should work with any .txt with more than a few words. Longer texts will offer more interesting results, but will take longer to load.\n"
	HelpMess += "A great source of texts is Project Gutenberg: https://www.gutenberg.org/"
	
	tkMessageBox.showinfo('Libraries Help', HelpMess)

def info():
	#Display info about the program
	InfoMess = "Llama Cat's Gibberish Generator\n Version 1.0 \n by Richard D Mellinger Jr \n imasillypirate.wordpress.com"
	tkMessageBox.showinfo('Information', InfoMess)

def getName(pathnm):
#extract the name of the file from the path
	if "'\'" in pathnm:
		name = pathnm.split("'\'")[-1]
		name1 = name.split('.')[-2]
	elif '/' in pathnm:
		name = pathnm.split('/')[-1]
		name1 = name.split('.')[-2]
	else:
		name1 = pathnm
	return  name1
	
def readIn():
#Select a txt file to read in, then read it in.
	global words, probs, libNam
	SkLines = SkipLineEntry.get()
	if not isInt(SkLines): #make sure they entered an integer
		tkMessageBox.showinfo('Error', "The 'Lines to skip' entry MUST be an integer.")
	else: 
		FilFind = Tk() #Let them select the path to the destination file
		FilFind.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
		if not FilTypeChecker(FilFind.filename,'txt'): #make sure they picked a .txt file
			tkMessageBox.showinfo('Error', "The file MUST be a .txt file.")
		else:
			libNam = getName(FilFind.filename)
			filPath = FilFind.filename
			FilFind.destroy()
			top.destroy()
			reading = Tk()
			readingStatus = StringVar()
			Label(reading,textvariable=readingStatus, width=100,justify='center').grid(row=0, column=0, columnspan = 2, rowspan = 2)
			readingStatus.set("Reading words list from "+libNam+'...\n This may take a while.')
			reading.update()
			words,probs = mkWordList(filPath,SkLines)
			readingStatus.set("Generating probabilities from "+libNam+'...\n This may take some time.')
			reading.update()
			probs = readUp(filPath,SkLines,words,probs)
			reading.destroy()

			hasLibrary()
		
def loadIn():
#load in a pickle file created previously by this program, which wil contain a dictionary with key 'w' storing a words list, and 'p' storing a table of probabilities
#Sets words and probs
	global words, probs, libNam
	FilFind = Tk()
	FilFind.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Pickle files","*.pkl"),("all files","*.*")))
	if not FilTypeChecker(FilFind.filename,'pkl'): #make sure they picked a .pkl file
		tkMessageBox.showinfo('Error', "The file MUST be a .pkl file.")
	else:
		libNam = getName(FilFind.filename)
		filPath = FilFind.filename
		FilFind.destroy()
		top.destroy()
		loading = Tk()
		loadingMess = StringVar()
		Label(loading, textvariable = loadingMess ,width=100,justify='center').grid(row = 0, column = 0,columnspan = 2, rowspan = 2)
		loadingMess.set('Loading '+libNam+'...\n This may take a while.')
		loading.update()
		with open(filPath, 'rb') as f:
			loaded = pickle.load(f)
		words = loaded['w']
		probs = loaded['p']
		loading.destroy()
		hasLibrary()

def help2():
	#Display help message for first page about loading libraries
	HelpMess = "-Enter a message length in the 'Message length' field (this should be an integer value that gives the number of words for the message)\n"
	HelpMess += "The actual message length may vary from the entered length because the code treats gramatical marks as their own words.\n"
	HelpMess += "-Insert a single word that appears in the library in the 'Seed Word' field, or check the box next to it labeled 'Random'.\n"
	HelpMess += "A Markov Chain requires a first word to start from. The entered word will be the first word or, if the 'Random' box is checked, a random word will be chosen from the library.\n"
	HelpMess += "The words in the library ARE case sensitive.\n"
	HelpMess += "-A library can be saved so that it can be loaded later instead of reading it in anew. To do this enter a file name in the 'Library name' field, and click 'Save'.\n"
	HelpMess += "When the save is complete a little message should appear in the upper right-hand corner of the window telling the file name."
	HelpMess += "The saving process can take quite a bit of time for large libraries."
	tkMessageBox.showinfo('Generate Gibberish Help', HelpMess)
	
def save():
	saving = Tk()
	savingMess = StringVar()
	toSave = {}
	toSave.update({'w':words})
	toSave.update({'p':probs})
	svNam = svNamEntry.get()
	Label(saving, textvariable =savingMess,width=100,justify='center').grid(row = 0, column = 0,columnspan = 2, rowspan = 2)
	savingMess.set( 'saving as '+svNam+'...\n This may take a while.')
	saving.update()
	with open(svNam + '.pkl', 'wb') as f:
		pickle.dump(toSave, f, pickle.HIGHEST_PROTOCOL)
	saving.destroy()
	saveStat.set('Saved as '+svNam+'.pkl')
	
def generateMessage():
	numW = int(messLenEntry.get())
	if not isInt(numW): #make sure they entered an integer
		tkMessageBox.showinfo('Error', "The 'Message length' entry MUST be an integer.")
	else:
		if RandVal.get() == 0:
			seedTry = seedWordEntry.get()
			if seedTry in words: #seed has to be in words
				seed = seedTry
			else:
				tkMessageBox.showinfo('Error', "The seed word must be a single word that appeared in the text used to create the library.\n Note: words are case sensitive and words containing dashes or apostrophes will have been broken into multiple words.")
		else:
			seed = random.choice(words)
		
	resultMess.set(writeChain(numW,words,seed,probs))
		
def hasLibrary():
	has = Tk()
	global RandVal,messLenEntry, seedWordEntry,resultMess,svNamEntry,saveStat
	RandVal = IntVar()
	resultMess = StringVar()
	saveStat = StringVar()
	Label(has, text = libNam+' is loaded \n and contains '+str(len(words))+' words.', justify = 'center').grid(row = 0,column=0, columnspan = 3)
	Label(has, textvariable = saveStat).grid(row = 0, column = 4)
	Label(has, text = 'Message length:').grid(row = 1,column=0)
	messLenEntry = Entry(has, width = 4)
	messLenEntry.insert(10,'10')
	messLenEntry.grid(row = 1, column = 1)
	Label(has, text = 'Seed word:').grid(row = 1,column=2)
	Checkbutton(has, text = 'Random', variable = RandVal).grid(row=1, column=3,  sticky=W)
	seedWordEntry = Entry(has, width = 7)
	seedWordEntry.grid(row = 1, column = 4)
	genButton =Button(has, text = " Generate ",activeforeground='white',activebackground='gray', command = generateMessage).grid(row = 1, column = 5)
	#quitButton =Button(has, text = " Update ",activeforeground='white',activebackground='gray', command = quit2).grid(row = 2, column = 5)#Add later
	Label(has, text = 'Library name (to save):').grid(row = 2,column=3)
	svNamEntry = Entry(has, width = 7)
	svNamEntry.grid(row = 2, column = 4)
	saveButton =Button(has, text = " Save ",activeforeground='white',activebackground='gray', command = save).grid(row = 2, column = 5)
	helpButton =Button(has, text = " Help ",activeforeground='white',activebackground='gray', command = help2).grid(row = 3, column = 4)#--------------Update
	quitButton =Button(has, text = " Quit ",activeforeground='white',activebackground='gray', command = quit2).grid(row = 3, column = 5)
	Label(has,textvariable=resultMess,justify='center',wraplength=400).grid(row=4, column=1, columnspan = 4, rowspan = 5)
		
#global words, probs, libNam, top, has#, RandVal#, messLenEntry, seedWordEntry
top = Tk()

welcome = StringVar()


Logo = PhotoImage(file = 'LlamaCat.gif')

logoIm = Label(image = Logo)
logoIm.grid(row=0,column=0,columnspan = 2, rowspan = 4)

welcome.set("Welcome to Llama Cat's\n Gibberish Generator!\n by imasillypirate \n\n Pick a library.")
label = Message(top,textvariable=welcome, width=300,justify='center')
label.grid(row=1, column=2, columnspan=3, rowspan = 2)

infoButton = Button(top, text = " Info ",activeforeground='white',activebackground='gray', command = info).grid(row = 3, column = 3)

LoadButton = Button(top, text = " Load ",activeforeground='white',activebackground='gray', command = loadIn).grid(row = 5, column = 0)

Label(top, text = 'Lines to skip:').grid(row = 5,column=1)
SkipLineEntry = Entry(top, width = 6)
SkipLineEntry.insert(10,'0')
SkipLineEntry.grid(row = 5,column=2)

ReadButton =Button(top, text = " Read ",activeforeground='white',activebackground='gray', command = readIn).grid(row = 5, column = 3)

helpButton =Button(top, text = " Help ",activeforeground='white',activebackground='gray', command = help1).grid(row = 6, column = 3)
quitButton =Button(top, text = " Quit ",activeforeground='white',activebackground='gray', command = quit1).grid(row = 6, column = 4)


top.mainloop()
