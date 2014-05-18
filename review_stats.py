"""More statistics of the database."""
from datetime import datetime
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

def getdatetime(date):
    date_split = date.split('-')
    dt = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    return dt


# Number of reviews
reviews_str = open('data/yelp_academic_dataset_review.json', 'r').read()
reviews = json.loads(reviews_str)
#print len(reviews)

dates = []

for rev in reviews:
    date = rev['date']
    dates.append(getdatetime(date))


#earliest = min(dates)
#latest = max(dates)
#print earliest.strftime("%d %B %Y")
#print latest.strftime("%d %B %Y")

#import sys
#sys.exit()

# What makes a review useful?

# Number of stars?
stars = []
stars_hist = {1:0, 2:0, 3:0, 4:0, 5:0}
acc_votes_useful = {1:0, 2:0, 3:0, 4:0, 5:0}
acc_votes_cool = {1:0, 2:0, 3:0, 4:0, 5:0}
acc_votes_funny = {1:0, 2:0, 3:0, 4:0, 5:0}
length = []
num_votes = []
too_new_delta = datetime.timedelta(days=365)
for rev in reviews:
    date = rev['date']
    dt = getdatetime(date)
    if dt > threshold_dt:
        continue
    num_stars = rev['stars']
    stars_hist[num_stars] += 1
    stars.append(num_stars)
    useful = rev['votes']['useful']
    cool = rev['votes']['cool']
    funny = rev['votes']['funny']
    acc_votes_useful[num_stars] += useful
    acc_votes_cool[num_stars] += cool
    acc_votes_funny[num_stars] += funny
    length.append(len(rev['text']))
    num_votes.append(useful)
#print acc
#print stars_hist
print 'Average number of useful votes per number of stars of review'
for i in range(1, 6):
    print '%d: %f votes for useful on average.' % (i,
            acc_votes_useful[i]/float(stars_hist[i]))

print 'Average number of cool votes per number of stars of review'
for i in range(1, 6):
    print '%d: %f votes for cool on average.' % (i,
            acc_votes_cool[i]/float(stars_hist[i]))

print 'Average number of funny votes per number of stars of review'
for i in range(1, 6):
    print '%d: %f votes for funny on average.' % (i,
            acc_votes_funny[i]/float(stars_hist[i]))

#print 'Analyzing length'
#scatterplot(length, num_votes)

