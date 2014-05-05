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
users_str = open('data/yelp_academic_dataset_user.json', 'r').read()
users_list = json.loads(users_str)
print len(users_list)

users = {}

for user in users_list:
    users[user['user_id']] = user

avg_stars_acc = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
avg_stars_count = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}


for user in users_list:
    if user['review_count'] > 0:
        avg = int(user['average_stars'])
        avg_stars_acc[avg] += user['votes']['useful']
        avg_stars_count[avg] += 1

print 'Average number of useful votes per average number of stars of user'
for i in range(6):
    print '%d: %f votes for useful on average.' % (i,
            avg_stars_acc[i]/float(avg_stars_count[i]))






