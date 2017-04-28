import random
import csv
import numpy as np
from config import SOURCE, TRANING, TEST

# init random
random.seed(1)

# creates a random dataset
def generateRandomSet(rows, dim, datatype):
    """Generate 10 random dataset"""

    # set size
    size = dim[0] * dim[1]

    # init empty space for input
    data = np.zeros(size, datatype)

    # output holder
    out = []

    # loop the set of rows
    for row in range(rows):

        # loop the set of cols
        for col in range(size):

            # save the random data as either 0 or 1
            data[col] = random.randrange(2)

        # save ref to output
        out.append({
            'recordNum': row,
            'bucketIdx': row,
            'actValue': row,
            'raw': data
        })

    # return the resulting random set
    return out


def getRealData(optimise, datatype):

    # output holder
    training = []
    test = []

    with open(SOURCE, 'rb') as csvfile:

        # get sourcereader
        sourcereader = csv.reader(csvfile, delimiter=',')

        # skips the first since it is header information
        sourcereader.next()

        # get length of source
        data = list(sourcereader)
        length = len(data)
        counter = 1

        # read up to here
        trainto = int(TRANING * length)
        rest = int((length - trainto) * TEST)

        # check if optimisation data set should be set
        if optimise is True:
            spanrest = [trainto + rest + 1, length]
        else:
            spanrest = [trainto + 1, trainto + rest]

        # loop all he rows
        for row in data:

            # empty raw array
            raw = np.zeros(len(row[3]), datatype)

            # copy content to array
            for i in range(len(row[3])):
                raw[i] = row[3][i]

            # load traning data
            if counter <= trainto:
                training.append({
                    'recordNum': row[0],
                    'bucketIdx': row[1],
                    'actValue': row[2],
                    'raw': raw
                })

            # load test data if current row is within span
            if counter >= spanrest[0] and counter <= spanrest[1]:
                test.append({
                    'recordNum': row[0],
                    'bucketIdx': row[1],
                    'actValue': row[2],
                    'raw': raw
                })

            # increase the counter
            counter = counter + 1

    return [test, training]
    