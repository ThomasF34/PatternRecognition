#Returns the prefix of the word given in parameter. The length of the wanted prefix is len, given in parameter.
def prefix(word,len):
	return word[:len]

#Returns the suffix of the word given in parameter. The length of the wanted suffix is len, given in parameter.
def suffix(word,len):
	return word[-len:]

#Returns the length of the longuest prefix of the patern that could be a suffix of the word, each one given in parameter
def long(word, pattern):
	count = 0
	for i in range(1,len(word)+1):
		#We extract the prefix of the pattern
		pref = prefix(pattern,i)
		#We extract the suffix of the given word (this suffix has the same length as the prefix previously extracted)
		suff = suffix(word, len(pref))
		#Checking if suffix and prefix are equal
		if pref == suff :
			#If it's the case, we keep the length of suffix or prefix
			count = len(pref)
	return count

#Returns the transitionTable to recognize the given partern in a text
def transitionTable(pattern,alphabet):
	table = []
	#For each state (from 0 to the length of the pattern)
	for state in range(0,len(pattern)+1) :
		line = []
		#for each letter in the given alphabet
		for letter in alphabet :
			#Adding the returning result of long-function
			line.append(long(prefix(pattern,state)+letter,pattern))
		table.append(line)
	#The table is now describing perfectly the automate
	return table

def detectPattern(text,pattern,alphabet):
	state = 0
	results = []
	transTable= transitionTable(pattern,alphabet)
	for i in range(0,len(text)) :
		#We have to make sure that each letter are lowered, so that comparasions aren't falsed.
		letterOccured = text[i].lower();

		if(letterOccured in alphabet) :
			#We have to select line first then column. So firstly we indicate the state, then the index of the letterOccured in the alphabet
			state = transTable[state][alphabet.index(letterOccured)]
			if(state == len(pattern)):
				results.append(i - len(pattern) + 2)
		else :
			#If the letter does not belong to alphabet, we go back to state 0
			state = 0
	return results

def detectPatternFile(file,pattern,alphabet):
	state = 0
	position = 0
	results = []
	transTable= transitionTable(pattern,alphabet)
	for line in file :
		i = 0
		while(i<len(line)):
			#We have to make sure that each letter are lowered, so that comparasions aren't falsed.
			letterOccured = line[i].lower();
			if(letterOccured in alphabet) :
				#We have to select line first then column. So firstly we indicate the state, then the index of the letterOccured in the alphabet
				state = transTable[state][alphabet.index(letterOccured)]
				if(state == len(pattern)):
					results.append(position - len(pattern) + 1)
			elif letterOccured == '\r' or letterOccured == '\n' :
				#position -= 1
				pass
			else : #If the letter does not belong to alphabet, we go back to state 0
				state = 0
			i += 1;
			position += 1
	return results
	
tags = open("tags.txt","r")
for line in tags :
	toPrint = line[:-2] + " : "
	for res in detectPatternFile(open("chr22.fa.txt",'r'),line[:-2].lower(),'acgt') :
		toPrint += str(res)
		toPrint += ' '
	print toPrint
