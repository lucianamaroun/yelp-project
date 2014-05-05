"""More statistics of the database."""
from matplotlib import pyplot
from numpy import arange

import json
import numpy

def scatterplot(x, y):
    pyplot.plot(x, y, 'b.')
    pyplot.xlim(min(x)-1, max(x)+1)
    pyplot.ylim(min(y)-1, max(y)+1)
    pyplot.show()

def barplot(labels, data):
    pos = arange(len(data))
    pyplot.xticks(pos+1.4, labels)
    pyplot.bar(pos, data)
    pyplot.show()


# Number of reviews
reviews_str = open('data/yelp_academic_dataset_review.json', 'r').read()
reviews = json.loads(reviews_str)
print len(reviews)

# What makes a review useful?

# Number of stars?
stars = []
stars_hist = {1:0, 2:0, 3:0, 4:0, 5:0}
acc_votes = {1:0, 2:0, 3:0, 4:0, 5:0}
length = []
num_votes = []
for rev in reviews:
    num_stars = rev['stars']
    stars_hist[num_stars] += 1
    stars.append(num_stars)
    useful = rev['votes']['useful']
    acc_votes[num_stars] += useful
    length.append(len(rev['text']))
    num_votes.append(useful)
#print acc
#print stars_hist
print 'Average number of useful votes per number of stars of review'
for i in range(1, 6):
    print '%d: %f votes for useful on average.' % (i,
            acc_votes[i]/float(stars_hist[i]))

print 'Analyzing length'
scatterplot(length, num_votes)

