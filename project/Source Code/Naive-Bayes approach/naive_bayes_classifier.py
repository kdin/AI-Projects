from __future__ import division		# For floating point division in Python 2.7.3
import sys
import ast
import math
import os

# ARGUMENTS : Name of the file that contains the review
# RETURNS : A tuple of positive and negative review possibilities
def classify(fileName):
	
	f = open(fileName, 'r')
	positive = 0
	negative = 0
	words = []
	for line in f :
		line = line.split('\n')[0]
		words = words + line.split(' ')				# All the contents of the file as a list of terms

	positive = probForClass(words, 'positive')		# To compute the probability that the review is positive
	negative = probForClass(words, 'negative')		# To compute the probability that the review is negative

	f.close()

	return (positive, negative)						# Return positive and negative probability



# ARGUMENTS : Contents of a file as a list of terms, positive or negative parameter
# RETURNS : The probability that the file is positive or negative based on parameter
def probForClass(words, target):
	if target == 'positive':												# Calculate for positive

		probDoc = posProb													# Probability of positive classes in training set
		for word in words:			
			if word in posDict:
				countWord = posDict[word]									# Count of words in positive class
			else:
				countWord = 0

			probDoc += math.log((countWord + 1)/(countPos + vocab))			# Probability that the review is positive with add-1 smoothing

	else:																	# Calculate for negative
		probDoc = negProb													# Probability of negative classes in training set
		for word in words:			
			if word in negDict:
				countWord = negDict[word]									# count of words in negative class 
			else:
				countWord = 0

			probDoc += math.log((countWord + 1)/(countNeg + vocab))			# Probability that the review is negative with add-1 smoothing


	return probDoc															# Return probability of review based on parameter


if __name__ == "__main__":


	modelFile = sys.argv[1]													# Model file input
	testDirectory = sys.argv[2]												# Files for prediction
	predictionsFile = sys.argv[3]											# Output predictions file

	f = open(modelFile, 'r')
	s = f.read().replace("\n", "")
	modelTuple = ast.literal_eval(s)	
	f.close()

	posDict = modelTuple[0]													# Dictionary of words and count in positive class
	posProb = math.log(modelTuple[1])										# Probability of positive class

	negDict = modelTuple[2]													# Dictionary of words and count in negative class
	negProb = math.log(modelTuple[3])										# Probability of negative class

	vocab = len(list(set(posDict.keys() + negDict.keys())))					# Vocabulary of the training set
	# print vocab

	countPos = sum(posDict.values())										# Total word count in positive class
	countNeg = sum(negDict.values())										# Total word count in negative class

	testFiles = os.listdir(testDirectory)
	outputFile = open(predictionsFile, 'w')									# Write output to this file
	outputFile.write ("FILE NAME\tPOSITIVE\t\tNEGATIVE\n")

	for fileName in testFiles:
		probTuple = classify(testDirectory + '/' + fileName)				# Obtain probability of positive and negative
		outputFile.write(fileName+"\t"+str(probTuple[0])+"\t"+str(probTuple[1])+'\n') # Write them to the predictions file

