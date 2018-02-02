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


"""Computes the Manhattan distance . Both rating1 and rating2 are dictionaries of the form {The Strokes: 3.0, Slightly Stoopid: 2.5}"""

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
    denominator = math.sqrt(sum_x2- (sum_x**2)/n) * math.sqrt(sum_y2 - (sum_y**2)/n)
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
            distance = measure(users[user],users[username]) ## so aplica para manhattan
            distances.append((distance, user))
    #distances.sort(reverse=True)
    distances.sort()
    return distances #return a tuple (distance, user)


""" creates a recommendation"""
"""Give a list of recommendations"""
def recommendation(username, users, measure):
    #first find the nearest Neighbor
    nearest = computeNearestNeighbor(username,users, measure)[0][1] #identify the first neighbor
    
    recommendations = []
    #now find bands Neighbor rated that user didn't
    NeighborRatings = users[nearest] #take the itens with ratings (item, rating) of neighbor
    print "Ratings do vizinho Mais cercano {}: {} \n" .format(nearest,NeighborRatings)
    userRatings = users[username] # take the itens with ratings of user to recommender
    print "Ratings do usuario {} \n" .format(userRatings)
    #search the itens ratings which nearest neighbor have but the target user dont have
    # to create the recommendation list
    for artist in NeighborRatings: 
        if not artist in userRatings: 
            recommendations.append((artist,NeighborRatings[artist]))
    recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True)
    return recommendations


measures_vector = [pearson, manhattan, euclidean]
def comparison(data, database, measures):
    
    m_pearson = computeNearestNeighbor(data, database, measures[0])
    m_manhattan = computeNearestNeighbor(data, database, measures[1])
    m_euclidean = computeNearestNeighbor(data, database, measures[2])
    
     
    x = {"":{}}
    for name in m_pearson:
        for name2 in m_manhattan:
            for name3 in m_euclidean:
                if (name[1]==name2[1])and (name[1]==name3[1]):
                    x = {name[1]:{"Pearson":name[0], "Manhattan":name2[0], "Euclidean":name3[0]} }
        print x
        
        
    #print "Recommendation to item by Cosine Similarity {}" .format(m_manhattan)
    #print "Recommendation to item by euclidean {}" .format(m_euclidean)
    
    #for data in bd:
        

"""PRINTS"""
print "comparacion {} \n" .format(comparison("Bill", users, measures_vector))
print "NearestNeighbor {} \n" .format(computeNearestNeighbor("Bill", users, manhattan ))
print "RECOMENDACION baseado en usuario{} \n" .format(recommendation("Bill", users, manhattan))


#print "tranformacion {} \n" .format(movies)

######ITEM BASED RECOMENDATION

prefers = {"lisa Rose":{"Lady in the Whater":1, "Snakes on a Plane":3.5}, \
           "Gene Seymour":{"Lady in the Whater":5, "Snakes on a Plane":3.5}
                 
        }


def transformPrefs(prefers):
    result = {}
    for person in prefers:
        for item in prefers[person]:
            result.setdefault(item, {})
            result[item][person] = prefers[person][item]
            
    return result




def calculateSimilarityItem(prefs, sim_distance=manhattan):
    #create a dictionary the items showing which other items they are more similar to.
    results={}
    
    #
    itemPrefs=transformPrefs(prefs)
    print "{} \n" .format(itemPrefs)
    c=0
    for item in itemPrefs:
        c+=1
        if c%100==0: 
            print "{} \n" .format(c, len(itemPrefs))
        scores = computeNearestNeighbor(item, itemPrefs, measure=sim_distance)
        results[item]=scores
            
    return results

itemsim = calculateSimilarityItem(users)

print "calculo de similaridade item {}".format(itemsim)
           
            
            
def recommend(username, users, similarities, n=3):
    scores = {}
    total_sim = {}
    #now get the rating for the user
    userRatings = users[username]
    for item, rating in userRatings.items():   
        for sim, other_item in similarities[item]:
        #ignore if this user has already rated this item
            if other_item in userRatings:
                continue 
            #weighted sum of rating times similarity
            scores.setdefault(other_item, 0.0)
            scores[other_item] += sim * rating
            #sum of all similarities
            total_sim.setdefault(other_item, 0.0)
            total_sim[other_item] += sim
    #divide each total score by total weighting to get an average
    recommendations = [(score/total_sim[item],item) for item,score in scores.items()] 
    # finally sort and return 
    recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse = True) 
    # Return the first n items return      
    return recommendations[:n]



print "Recomendacao baseado em item {} \n".format(recommend("Bill",users, itemsim))
        
        
    
    

    

    
    
    
    
    