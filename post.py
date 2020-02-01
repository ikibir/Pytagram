import json
import requests
import os, re, sys
import urllib.request

class user_info:
	def __init__(self, username=None, full_name=None, is_verified=None, profile_pic_url=None):
		self.username = username
		self.full_name = full_name
		self.is_verified = is_verified
		self.profile_pic_url = profile_pic_url


class post:
	@staticmethod
	def eprint(*args, **kwargs):
		print(*args, file=sys.stderr, **kwargs)

	@staticmethod
	def __print_error_and_exit__(error_msg):
		post.eprint(error_msg)
		exit(-1)

	@classmethod
	def __make_link__(self, post_input):
		post_link = f'https://www.instagram.com/p/{post_input}/'
		return post_link

	@classmethod	
	def __is_link__(self, post_input):
		try:
			if re.match('[https://]*[www.]*instagram.com/p/[a-zA-Z0-9]*', post_input):
				return True
			else:
				return False
		except Exception as e:
			post.__print_error_and_exit__('Link Error: '+ e)

	@classmethod
	def __create_post_object__(self, post_dict):
		media = post_dict['graphql']['shortcode_media']
		self.post_id = media['id']
		self.post_shortcode = media['shortcode']
		self.dimensions = (width, height) = media['dimensions']['width'], media['dimensions']['height']
		self.display_url = media['display_url']
		self.media_text = media['accessibility_caption'] if 'accessibility_caption' in media.keys() else ""
		self.is_video = media['is_video']
		self.tagged_users = self.__get_tagged_users__(media['edge_media_to_tagged_user'])
		self.captions = self._get_post_captions_(media['edge_media_to_caption'])
		self.time_stamp = media['taken_at_timestamp']
		self.like_count = media['edge_media_preview_like']['count']	
		self.comment_count = media['edge_media_preview_comment']['count']
		self.location = media['location']
		# Yorumlardan Devam Et

	@classmethod
	def __get_tagged_users__(self, media_tagged):
		all_users = []
		for user_node in media_tagged['edges']:
			user = user_node['node']['user']
			full_name = user['full_name']
			is_verified = user['is_verified']
			profile_pic_url = user['profile_pic_url']
			username = user['username']
			all_users += [user_info(username, full_name, is_verified, profile_pic_url)]
		return all_users
	
	@classmethod
	def _get_post_captions_(self, media_captions):
		all_captions = []
		for user_node in media_captions['edges']:
			text = user_node['node']['text']
			all_captions += [text]
		return all_captions


	@classmethod
	def post(self, post_input):
		# Cheking link is if proper format if not uses 'post_input' 
		# as post id and generate link from post id
		if not self.__is_link__(post_input):
			post_input = self.__make_link__(post_input)
		
		# convert 'post page' to 'json post page'
		post_link = post_input + '?__a=1'
		
		try:
			response = requests.get(post_link)
		except:
			error_msg = f'Invalid Link : {post_link} \nFor Usage Help Go https://www.github.com/ikibir'
			post.__print_error_and_exit__(error_msg)

		if response.status_code == 404:
			error_msg = f'Page not found : {post_link}'
			post.__print_error_and_exit__(error_msg)
		try:
			post_dict = self.__to_dict__(response)
		except:
			error_msg = f'Invalid Link : {post_link} \nFor Usage Help Go https://www.github.com/ikibir'
			post.__print_error_and_exit__(error_msg)


		self.__create_post_object__(post_dict)
	
		return True

	@classmethod
	def __to_dict__(self, response):
		page_text = response.content
		json_string = page_text

		obj = json.loads(json_string)
		return obj

	def make_dir(self, dir_name):
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)

	def download(self, post_id):
		link = f'https://www.instagram.com/p/{post_id}/?__a=1'
		response = requests.get(link)
		obj = self.to_dict(response)
		self.username = obj['graphql']['shortcode_media']['owner']['username']
		self.make_dir(self.username)
		try:
			edges = obj['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
		except:
			media = obj['graphql']['shortcode_media']
			is_video = media['is_video']
			if is_video:
				video_url = media['video_url']
				self.save_video(video_url, post_id, 0)
			else:
				image_url = media['display_url']
				self.save_image(image_url, post_id, 0)
		else:
			i=0
			for edge in edges:
				is_video = edge['node']['is_video']
				if is_video:
					video_url = edge['node']['video_url']
					self.save_video(video_url, post_id, i)
					#print(video_url)
				else:
					image_url = edge['node']['display_url']
					self.save_image(image_url, post_id, i)
					#print(image_url)

				i+=1

	def save_image(self, link, post_id, i):
		urllib.request.urlretrieve(link, f"{self.username}/{post_id}_{i}.jpg")

	def save_video(self, link, post_id, i):
		urllib.request.urlretrieve(link, f"{self.username}/{post_id}_{i}.mp4")




p = post()
post_id = 'B6pvZPXAbso'
p.post('https://www.instagram.com/p/B79RIw-pMS9/')
print('post_id', p.post_id)
print('post_shortcode', p.post_shortcode)
print('dimensions', p.dimensions)
print('display_url', p.display_url)
print('media_text', p.media_text)
print('is_video', p.is_video)
print('tagged_users', p.tagged_users)
print('captions', p.captions)
print('time_stamp', p.time_stamp)
print('like_count', p.like_count)
print('comment_count', p.comment_count)
print('location', p.location)
#p.download(post_id)
