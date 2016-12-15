from __future__ import division		# Floating point division in Python 2.7.3
import os
import sys
import re

# ARGUMENTS : Path of the training directory
# RETURNS : Dictionary of words with their counts and number of files in directory
def fileParser(param):

	
	wordDict = {}													# Dictionary of words with counts
	
	dirs = os.listdir(param)										

	for fileName in dirs:
		f = open(param + fileName, 'r')


		contents = ' '.join(f.read().split('\n')).split(" ")		# Take all the terms in the file
		
		for word in contents:										# Build the dictionary of words and counts
			if word in wordDict:
				wordDict[word] += 1
			else:
				wordDict[word] = 1


 	
	tot = 0
	blacklist = []													# To remove word occurences lesser than 5
	for word in wordDict:
		if wordDict[word] < 5:
			blacklist.append(word)
		else:
			tot += wordDict[word]

	for word in blacklist:											# Remove blacklisted words
		del wordDict[word]


	return (wordDict, len(dirs))									# Returns word dictionary and no. of files in directory




if __name__ == "__main__":

	directory = sys.argv[1]											# Input training directory
	output = sys.argv[2]											# Output to this file


	posTuple = fileParser(directory + '/pos/')					
	negTuple = fileParser(directory + '/neg/')

	posDict = posTuple[0]											# Dictionary of words and counts in positive class
	negDict = negTuple[0]											# Dictionary of words and counts in negative class
	docCount = posTuple[1] + negTuple[1]

	posProb = posTuple[1] / docCount								# Probability of positive class
	negProb = negTuple[1] / docCount								# Probability of negative class

	outputTuple = (posDict, posProb, negDict, negProb)				# Positive/negative dictionaries and probabilities as tuples

	outputFile = open(output, 'w')
	outputFile.write(str(outputTuple))								# Output tuples to the output file
	
