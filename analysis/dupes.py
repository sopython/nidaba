from database_scripts import *

client = pym.MongoClient()
db = client.nidaba
post_links = db.post_links
questions = db.questions

dupes_query = post_links.find({'LinkTypeId':3}, {'_id':False, 
                                              'Id':True,  
                                              'RelatedPostId':True})

dupes = pd.DataFrame(list(dupes_query))
dupes = dupes.set_index(dupes.Id)
del dupes['Id']

count = dupes.groupby('RelatedPostId').count()
count.rename(columns={'RelatedPostId':'Count'}, inplace=True)

dupe_list = list(map(int, count.index))
details_query = questions.find({'Id':{'$in':dupe_list}}, {'_id':False,
                                                          'Title':True,
                                                          'Score':True,
                                                          'Id':True})

details = pd.DataFrame(list(details_query))
details = details.set_index(details.Id)
del details['Id']

count = pd.merge(left=count, right=details, left_index=True, 
                 right_index=True).sort('Count', ascending=False)

print(count.head())

client.close()
