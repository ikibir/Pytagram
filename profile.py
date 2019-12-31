import requests
import json
from post import post


def to_dict(response):
	page_text = response.content
	json_string = page_text
	obj = json.loads(json_string)
	return obj


p = post()
username = input('Enter the user name: ')
link = f'https://www.instagram.com/{username}/?__a=1'

response = requests.get(link)
obj = to_dict(response)

timeline = obj['graphql']['user']['edge_owner_to_timeline_media']
user_id = obj['graphql']['user']['id']


has_next_page = timeline['page_info']['has_next_page']
end_cursor = timeline['page_info']['end_cursor']
end_cursor=''
i=0
while True:
	link = f'https://instagram.com/graphql/query/?query_id=17888483320059182&id={user_id}&first=12&after={end_cursor}'
	response = requests.get(link)
	obj = to_dict(response)
	edges = obj['data']['user']['edge_owner_to_timeline_media']['edges']
	for edge in edges:
		shortcode = edge['node']['shortcode']
		p.download(shortcode)
		i+=1
		print(f'{i} :: Downloading instagram.com/p/{shortcode}')
	page_info = obj['data']['user']['edge_owner_to_timeline_media']['page_info']
	has_next_page = page_info['has_next_page']
	if has_next_page==False:
		break
	else:
		end_cursor = page_info['end_cursor']