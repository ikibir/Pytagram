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
	def __init__(self, post_input):
		self.post(post_input)

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
		#self.media_text = media['accessibility_caption'] if 'accessibility_caption' in media.keys() else ""
		self.is_video = media['is_video']
		self.tagged_users = self.__get_tagged_users__(media['edge_media_to_tagged_user'])
		self.captions = self.__get_post_captions__(media['edge_media_to_caption'])
		self.time_stamp = media['taken_at_timestamp']
		self.like_count = media['edge_media_preview_like']['count']	
		self.comment_count = media['edge_media_preview_comment']['count']
		self.location = media['location']
		self.owner = self.__get_user_info__(media['owner'])
		self.content, self.media_text = self.__get_post_media__(media)
		# Yorumlardan Devam Et


	@classmethod
	def __get_post_media__(self, content):
		try:
			if 'edge_sidecar_to_children' not in content.keys():
				if self.is_video:
					return [content['video_url']], None
				else:
					return [content['display_url']], content['accessibility_caption']
			else:
				content = content['edge_sidecar_to_children']['edges']
				all_media = []
				all_image_info = []
				for per_media in content:
					is_video = per_media['node']['is_video']
					if is_video:
						all_media += [per_media['node']['video_url']]
						all_image_info += ['']
					else:
						all_media += [per_media['node']['display_url']]
						all_image_info += [per_media['node']['accessibility_caption']]
				return all_media, all_image_info

		except Exception as e:
			with open('errors.log', 'w') as f:
				f.write(str(e))
			error_msg = f'Unexpected Error ! \n For more details check errors.log'
			post.__print_error_and_exit__(error_msg)


	@classmethod
	def __get_user_info__(self, user):
		full_name = user['full_name']
		is_verified = user['is_verified']
		profile_pic_url = user['profile_pic_url']
		username = user['username']
		return user_info(username, full_name, is_verified, profile_pic_url)

	@classmethod
	def __get_tagged_users__(self, media_tagged):
		all_users = []
		for user_node in media_tagged['edges']:
			user = user_node['node']['user']
			all_users += [self.__get_user_info__(user)]
		return all_users
	
	@classmethod
	def __get_post_captions__(self, media_captions):
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
		self.link = post_input
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

	@classmethod
	def __make_dir__(self, dir_name):
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)

	@classmethod
	def download(self):
		self.__make_dir__(self.owner.username)
		for i,url in enumerate(self.content):
			if url.find('.mp4?')>=0:
				self.save_video(url, self.post_shortcode, i)
			else:
				self.save_image(url, self.post_shortcode, i)

	@classmethod
	def save_image(self, link, post_id, i):
		urllib.request.urlretrieve(link, f"{self.owner.username}/{post_id}_{i}.jpg")

	@classmethod
	def save_video(self, link, post_id, i):
		urllib.request.urlretrieve(link, f"{self.owner.username}/{post_id}_{i}.mp4")





