from math import sqrt
import collections
import os
import csv
import json



# data set of the critics !!
critics = collections.OrderedDict()
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}



def sim_distance(critic1, critic2, critics):
	si = {}
	for i in critics[critic1]:
		if i in critics[critic2]:
			si[i]=1


	if len(si)==0:
		return 0

	sumed = sqrt(sum(pow(critics[critic1][i] - critics[critic2][i] , 2) for i in critics[critic1] if i in critics[critic2]))

	return 1/(1+sumed);


# for i,v in critics.items():
# 	for j,v in critics.items():
# 		if j is not i:

# 			print(i,j)
# 		#print ('%s and %s similarity is' % (critics[i],critics[j])

# 			print (sim_distance(i, j , critics))

print ("pearson corellation -----------------------------------------")

def sim_pearson(critic1, critic2, critics):
	si2 = {}
	for i in critics[critic1]:
		if i in critics[critic2]:
			si2[i]=1


	if len(si2)==0:
		return 0

	n = len(si2)
	

	sum1 = sum([critics[critic1][i] for i in si2])
	print(sum1)

	sum2 = sum([critics[critic2][i] for i in si2])

	sum1sq = sum([pow(critics[critic1][i],2) for i in si2])
	sum2sq = sum([pow(critics[critic2][i],2) for i in si2])

	psum = sum([critics[critic1][i]*critics[critic2][i] for i in si2])

	num = psum - (sum1*sum2/n)
	den = sqrt((sum1sq - pow(sum1,2)/n)* (sum2sq - pow(sum2,2)/n))

	if den==0:
		return 0

	r = num/den

	return r

def topMatches(prefs,person,n=5,similarity=sim_pearson):
	scores=[(similarity(person,other,prefs),other)
	for other in prefs if other!=person]
# Sort the list so the highest scores appear at the top
	scores.sort( )
	scores.reverse( )
	return (scores[0:n])


print (topMatches(critics, 'Lisa Rose'))

def getRecommendations(critic, person):
	total ={}
	simsum = {}
	for other in critic:
		if other == person:
			continue

		sim = sim_pearson(person, other, critic)
		print(sim,other)

		if sim<=0:
			continue

		for i in critic[other]:
			if i not in critic[person] or critic[person][i] == 0:
				total.setdefault(i, 0)
				total[i] +=  critic[other][i] * sim

				simsum.setdefault(i,0)
				simsum[i] += sim

	
	ranking = [(v/simsum[item] , item) for item, v in total.items()]

	ranking.sort()
	ranking.reverse()
	print(ranking)


def transform_data(critics):
	result = {}
	for i in critics:
		for j in critics[i]:
			result.setdefault(j,{})

			result[j][i] = critics[i][j]
	return result
y = transform_data(critics)
getRecommendations(y, 'Superman Returns')


def get_Similarity(ctitics, n=10):
	result = {}
	movie = transform_data(critics)
	
	for m in movie:
		
		scores = topMatches(movie,m)
		result[m] = scores

	return result


print(get_Similarity(critics))

def get_RecommendationList(critics, sim , user):
	user_rating = critics[user]
	total = {}
	sums = {}

	for (movie, rate) in user_rating.items():
		for (similarity, item2) in sim[movie]:
			if item2 in user_rating:
				continue

			total.setdefault(item2,0)
			total[item2] += similarity*rate
			sums.setdefault(item2,0)
			sums[item2] += similarity

			rankings=[(score/sums[item],item) for item,score in total.items( )]

	rankings.sort( )
	rankings.reverse( )
	return rankings

print (get_RecommendationList(critics, get_Similarity(critics), 'Toby'))

def loadMovie(path = os.path.dirname(os.path.realpath(__file__))):
	movies ={}
	y = path+'/ml-latest-small'
	f = y+'/movies.csv'
	with open(f, 'r') as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		for row in r:
			(movieId, title, genre) = row
			movies[int(movieId)]= title
	
	prefs = {}
	z = y+'/ratings.csv'
	with open(z, 'r' ) as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		for row in r:

			(userId,movieId,rating,timestamp) = row
			prefs.setdefault(userId,{})
			prefs[userId][movies[int(movieId)]] = float(rating)
		json.dump(prefs, open("text.txt",'w'))	

	print(prefs['1'])
	return prefs

loadMovie()



