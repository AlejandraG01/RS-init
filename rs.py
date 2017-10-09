import math

"""Representation in python of users'rating data"""
users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}, \
"Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}, \
"Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},\
"Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},\
"Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},\
"Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},\
"Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0}, \
"Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}}


"""Computes the Manhattan distance or cosine similarity. Both rating1 and rating2 are dictionaries of the form {The Strokes: 3.0, Slightly Stoopid: 2.5}"""

def manhattan (rating1, rating2):
    distance = 0
    commontRatings = False
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key]-rating2[key])
            commontRatings = True
    if commontRatings:
        return distance
    else:
        return -1 # indicates no ratings in commun

"""Computes the euclidean distance"""
def euclidean (rating1, rating2):
    distance = 0
    commontRatings = False
    for key in rating1:
        if key in rating2:
            distance += pow(abs(rating1[key]-rating2[key]),2)
            commontRatings =True
    if commontRatings:
        return pow(distance, 1/2)
    else:
        return -1
    
"""Compute the pearson similarity"""    
def pearson(rating1, rating2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in rating1:
        if key in rating2:
            n +=1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += x**2
            sum_y2 += y**2
    #now compute denominator
    denominator = math.sqrt(sum_x2- (sum_x**2) / n) * math.sqrt(sum_y2 - (sum_y**2) /n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y)/n) / denominator
"""if the data is subject to grade-inflaction( different users maybe using different scales)
use Pearson """
"""if the data is danse (almost all attributes have non-zero value) and the magnitude of
attributes values is important, use distances measures as a euclidean"""
""" If data is sparse considere using cosine similarity"""

"""creates a sorted list of users based on their distance to username"""
def computeNearestNeighbor(username, users, measure):
    distances = []
    for user in users:
        if user != username:
            #distance = manhattan(users[user],users[username])
            distance = measure(users[user],users[username])
            distances.append((distance, user))
    distances.sort()
    
    return distances


""" creates a recommendation"""
"""Give a list of recommendations"""
def recommend (username, users, measure):
    #first find the nearest Neighbor
    nearest = computeNearestNeighbor(username,users, measure)[0][1] #identifine the first neighbor
    
    recommendations = []
    #now find bands Neighbor rated that user didn't
    NeighborRatings = users[nearest] #take the itens with ratings (item, rating) of neighbor
    print "Ratings dos vizinhos: {}" .format(NeighborRatings)
    userRatings = users[username] # take the itens with ratings of user to recommender
    print "Ratings do usuario {}" .format(userRatings)
    for artist in NeighborRatings: 
        if not artist in userRatings:
            recommendations.append((artist,NeighborRatings[artist]))
    recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)
    return recommendations


prefers = {"lisa Rose":{"Lady in the Whater":2.5, "Snakes on a Plane":3.5}, \
           "Gene Seymour":{"Lady in the Whater":3, "Snakes on a Plane":3.5}
                 
        }


def transformPrefs(prefers):
    result = {}
    for person in prefers:
        for item in prefers[person]:
            result.setdefault(item, {})
            result[item][person] = prefers[person][item]
            
    return result



movies = transformPrefs(users)
measures_vector = [pearson, manhattan, euclidean]

def comparison(data, database, measures):
    
    m_pearson = computeNearestNeighbor(data, database, measures[0])
    m_manhattan = computeNearestNeighbor(data, database, measures[1])
    m_euclidean = computeNearestNeighbor(data, database, measures[2])
    
    print "Recommendation to item by pearson {}" .format(m_pearson)
    
    x = {"":[]}
    for name in m_pearson:
        for name2 in m_manhattan:
            for name3 in m_euclidean:
                if (name[1]==name2[1])and (name[1]==name3[1]):
                    x = {name[1]:[name[0],name2[0],name3[0]] }
        print x
        
    #print "Recommendation to item by Cosine Similarity {}" .format(m_manhattan)
    #print "Recommendation to item by euclidean {}" .format(m_euclidean)
    
    #for data in bd:
        


"""PRINTS"""
print "Distancia manhattan {}" .format(manhattan(users["Bill"], users["Veronica"]))
print "Distancia euclideana {}" .format(euclidean(users["Bill"], users["Veronica"]))
print "NearestNeighbor {}" .format(computeNearestNeighbor("Bill", users, manhattan ))
print "O vizinho: {}" .format(computeNearestNeighbor("Bill", users, euclidean)[0][1])
print "recommendation {}" .format(recommend("Bill", users, euclidean))
print "Correlacao Pearson {}" .format(pearson(users["Bill"], users["Angelica"]))
print "Correlacao entre usuarios {}" .format(pearson(users["Veronica"], users["Angelica"]))
print "Correlacao entre usuarios {}" .format(pearson(users["Hailey"], users["Angelica"]))

print "tranformacion {}" .format(movies)

print "comparacion {}" .format(comparison("Blues Traveler", movies, measures_vector))

