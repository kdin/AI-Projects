def classify(data, weights):
    
    guesses = []
    for datum in data:
        vectors = {}
        for l in ['positive', 'negative']:
            vectors[l] = 0
            for feature in datum:
                vectors[l] += weights[feature]
        guesses.append(1 if vectors['positive'] >= vectors['negative'] else 0)
    return guesses


if __name__ == "__main__":


    modelFile = sys.argv[1]                                                 # Model file input
    testDirectory = sys.argv[2]                                             # Files for prediction
    predictionsFile = sys.argv[3]                                           # Output predictions file

    f = open(modelFile, 'r')
    s = f.read().replace("\n", "")
    modelTuple = ast.literal_eval(s)    
    f.close()


    posDict = modelTuple[0]                                                 # Dictionary of words and count in positive class
    posProb = math.log(modelTuple[1])                                       # Probability of positive class

    negDict = modelTuple[2]                                                 # Dictionary of words and count in negative class
    negProb = math.log(modelTuple[3])                                       # Probability of negative class

    weights = posDict + negDict

    vocab = len(list(set(posDict.keys() + negDict.keys())))                 # Vocabulary of the training set
    # print vocab

    countPos = sum(posDict.values())                                        # Total word count in positive class
    countNeg = sum(negDict.values())                                        # Total word count in negative class

    testFiles = os.listdir(testDirectory)
    outputFile = open(predictionsFile, 'w')                                 # Write output to this file
    outputFile.write ("FILE NAME\tPOSITIVE\t\tNEGATIVE\n")

    for fileName in testFiles:
        probTuple = classify(testDirectory + '/' + fileName, classify)                # Obtain probability of positive and negative
        outputFile.write(fileName+"\t"+str(probTuple[0])+"\t"+str(probTuple[1])+'\n') # Write them to the predictions file