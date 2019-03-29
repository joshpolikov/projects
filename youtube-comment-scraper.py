import requests
import pandas as pd


key = 'your-key'
video_id = 'wSY-KRMpzhM'
user_list = []

first_response = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?key=' + key + 
'&textFormat=plainText&part=snippet&videoId=' + video_id + '&maxResults=100')

data1 = first_response.json()

d1 = data1.get('items')

#print d1

for snippet in d1:
	url = snippet.get('snippet').get('topLevelComment').get('snippet').get('authorChannelUrl')
	user_list.append(url)

nextPageToken = data1.get('nextPageToken')

while nextPageToken:

	next_response = requests.get('https://www.googleapis.com/youtube/v3/commentThreads?key=' + key + 
	'&textFormat=plainText&part=snippet&videoId=' + video_id + '&maxResults=100&pageToken=' + nextPageToken)

	data2 = next_response.json()
	
	#print data2
	
	d2 = data2.get('items')

	nextPageToken = data2.get('nextPageToken')
	
	for snippet in d2:
		url = snippet.get('snippet').get('topLevelComment').get('snippet').get('authorChannelUrl')
		user_list.append(url)
		
import pprint
pprint.pprint(user_list)
print len(user_list),' users commented.'

user_list_subs = []

for channel in user_list:
	id = channel[-24:]
	
	#get channel statistics
	user_response_stats = requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&key=' 
	+ key + '&id=' + id)
	
	user_data = user_response_stats.json()
	
	sub_count = user_data.get('items')[0].get('statistics').get('subscriberCount')
	sub_count = int(sub_count)
	
	view_count = user_data.get('items')[0].get('statistics').get('viewCount')
	view_count = int(view_count)
	
	video_count = user_data.get('items')[0].get('statistics').get('videoCount')
	video_count = int(video_count)
	
	#get channel metadata
	user_response_snippet = requests.get('https://www.googleapis.com/youtube/v3/channels?part=snippet&key=' 
	+ key + '&id=' + id)
	
	user_data = user_response_snippet.json()
	
	title = user_data.get('items')[0].get('snippet').get('title')
	custom_url = user_data.get('items')[0].get('snippet').get('customUrl')

	
	
	#add all data to list
	user_list_subs.append([channel,title,sub_count,view_count,video_count,custom_url])
	
	

pprint.pprint(user_list_subs)

#Convert user_list_subs to dataframe
import pandas as pd
labels = ['channel','title','subscriber_count','view_count','video_count','custom_url']
df = pd.DataFrame.from_records(user_list_subs, columns = labels)
df = df.sort_values(by=['subscriber_count'],ascending=False)

print df

df.to_csv('parachute-young-march28.csv',index=False, encoding='utf-8')
