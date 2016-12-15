from __future__ import division  # Floating point division in Python 2.7.3

import math
import os


# ARGUMENTS : Positive or negative directory inside training directory
# RETURNS : List of unique words in each file and number of documents

def fileParser(param):

	directory = "../dataset/"			# Base directory
	train = 'train/'
	negative = 'neg/'		
	positive = 'pos/'

	
	dirs = os.listdir(directory + train + param)
	docsCount = len(dirs)
	words = []																			# Stores list of unique words in each file
	for fileName in dirs:
		f = open(directory + train + param + fileName, 'r')



		contents = ' '.join(f.read().split('\n')).split(" ")							# All terms in the file
		# contents = re.split(' +', contents)
		words = words + list(set(contents))												# Update list of unique words in each file


	return (words, docsCount)															# Tuple of unique words in each file and size of dir


if __name__ == "__main__":

	posTuple = fileParser('pos/')
	negTuple = fileParser('neg/')

	positive = posTuple[0]																# Words of positive class
	negative = negTuple[0]																# Words of negative class

	posCount = posTuple[1]																
	negCount = negTuple[1]
	totalCount = posCount + negCount

	posProbability = posCount/totalCount												# Probability of positive class
	negProbability = negCount/totalCount												# Probability of negative class


	# Computing INFORMATION GAIN

	# GAIN CONTRIBUTION PROBABILITY OF CLASSES
	classProbability = -1 * ((posProbability*(math.log(posProbability))) + (negProbability * (math.log(negProbability))))


	vocab = list(set(positive+negative))												# Vocabulary of training set

	gainDict = {}																		# Dictionary of information gain and words
	itr = 1

	for word in vocab:																	# Calculate INFORMATION GAIN of each word
		informationGain = classProbability

		totalOcc = positive.count(word) + negative.count(word)
		
		wordProb = totalOcc/totalCount
		probBar = 1 - wordProb

		probPos = positive.count(word)/totalOcc											# Probability of positive when occurs
		probNeg = negative.count(word)/totalOcc											# Probability of negative when occurs

		if probPos == 0:																# Make probability very low if 0
			probPos = 000000000000000000000000000000000000000.1
		if probNeg == 0:
			probNeg = 000000000000000000000000000000000000000.1

		nonOccurences = totalCount - totalOcc
		posNonOcc = posCount - positive.count(word)						
		negNonOcc = negCount - negative.count(word)

		if  nonOccurences != 0:
			probNonPos = posNonOcc / nonOccurences										# Probability of positive when doesnt occur
			probNonNeg = negNonOcc / nonOccurences										# Probability of negative when doesnt occur
		else:
			probNonNeg = 00000000000000000000000000000000000000.1						# Make prob very low
			probNonPos = 00000000000000000000000000000000000000.1

		if probNonPos == 0:																# Make probability very low if 0
			probNonPos = 0000000000000000000000000000000000000000.1
		if probNonNeg == 0:
			probNonNeg = 0000000000000000000000000000000000000000.1


		informationGain += wordProb * ((probPos*(math.log(probPos))) + (probNeg*(math.log(probNeg))))			# Information gain

	informationGain += probBar * ((probNonPos*(math.log(probNonPos))) + (probNonNeg*(math.log(probNonNeg))))	# Add info gain of conjugate



	gainDict[word] = informationGain													# Build dictionary of words and gains



sortedList = sorted(gainDict, key=gainDict.__getitem__)									# Sort gains in reverse order

sortedList.reverse()


for word in sortedList:
	print word, ":", gainDict[word]