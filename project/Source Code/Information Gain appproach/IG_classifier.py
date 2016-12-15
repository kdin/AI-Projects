from __future__ import division 		# FLoating point division in Python 2.7.3
import os
import sys
import math


# ARGUMENTS : Document and parameter if positive or negative
# RETURNS :   Probability of review being positive or negative absed on parameter
def classify(doc, param):
	
	probDoc = 0
	for word in vocab:

		if word in doc:																	# Probability if word in voacb is in doc also

			if param == 'positive':
				probDoc += math.log((positive.count(word) + 1)/(posCount + 1))
					
			else:
				probDoc += math.log((negative.count(word)+1)/(negCount+1))
					
		else:																			# Probability if word in voacb is not in doc (conjugate)

			if param == 'positive':
				probDoc += 1 - (math.log((positive.count(word)+1)/(posCount+1)))
			else:
				probDoc += 1 - (math.log((negative.count(word)+1)/(negCount+1)))

	return probDoc




if __name__ == "__main__":

	testDirectory = "../dataset/train"		# Training directory

	posFiles = os.listdir(testDirectory + '/pos/')
	negFiles = os.listdir(testDirectory + '/neg/')
	posCount = len(posFiles)
	negCount = len(negFiles)

	positive = []																				# Unique words in each positive document
	for fileName in posFiles:																	# All positive files
		f = open(testDirectory+'/pos/'+fileName, 'r')

		contents = ' '.join(f.read().split('\n')).split(" ")									# All contents in file
		positive += list(set(contents))															# Unique contents in file
		f.close()

	negative = []																				# Unique words in each negative doc
	for fileName in negFiles:																	# All negative files
		f = open(testDirectory+'/neg/'+fileName, 'r')

		contents = ' '.join(f.read().split('\n')).split(" ")									# All contents in file
		negative += list(set(contents))															# Unique contents in file
		f.close()


	vocab = []
	IGFile = "./gainsorted.txt"	# File containing INFO GAIN IN REVERSE ORDER

	f = open(IGFile, 'r')

	for line in f:
		if line[-1] == '\n':
			line = line[0:-1]

		entry = line.split(":")
		entry[0] = entry[0][0:-1]
		entry[1] = entry[1][1:]

		vocab.append(entry[0])

	f.close()
	vocabSize = len(vocab)																		# Form vocabulary in order of decreasing INFO GAIN


	# vocab = vocab[0:(int(round(vocabSize/2)))]
	vocab = vocab[0:10000]																		# Select 'k' most important features needed


	predict = "../dataset/test"      			# Prediction directory


	posPredict = os.listdir(predict)

	print "FILENAME\t POSITIVE\t\t NEGATIVE\n"
	for fileName in posPredict:
		f = open(predict+'/'+fileName, 'r')
		contents = ' '.join(f.read().split('\n')).split(" ")									# All terms in test file

		probPos = math.log(0.5) + classify(contents, 'positive')								# Probability that the doc is positive
		probNeg = math.log(0.5) + classify(contents, 'negative')								# Probability that the doc is negative

		print fileName,'\t',probPos,'\t',probNeg,'\n'											# Print result to file
		f.close()


