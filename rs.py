
"""Representation in python of users'rating data"""
users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}, \
"Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}, \
"Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0},\
"Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},\
"Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0},\
"Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},\
"Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0}, \
"Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5, "The Strokes": 3.0}}


"""Computes the Manhattan distance. Both rating1 and rating2 are dictionaries of the form {The Strokes: 3.0, Slightly Stoopid: 2.5}"""

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

"""creates a sorted list of users based on their distance to username"""
def computeNearestNeighbor(username, users):
    distances = []
    for user in users:
        if user != username:
            distance = manhattan(users[user],users[username])
            distances.append((distance, user))
    distances.sort()
    
    return distances


""" creates a recommendation"""
"""Give a list of recommendations"""
def recommend (username, users):
    #first find the nearest Neighbor
    nearest = computeNearestNeighbor(username,users)[0][1] #identifine the first neighbor
    
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

"""PRINTS"""
print "Distancia manhattan {}" .format(manhattan(users["Bill"], users["Veronica"]))
print "Distancia euclideana {}" .format(euclidean(users["Bill"], users["Veronica"]))
print "NearestNeighbor {}" .format(computeNearestNeighbor("Bill", users))
print "O vizinho: {}" .format(computeNearestNeighbor("Bill", users)[0][1])
print "recommendation {}" .format(recommend("Bill", users))
