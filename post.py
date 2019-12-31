import json
import requests
import os
import urllib.request


class post:
	def to_dict(self, response):
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


"""
p = post()
post_id = 'B6pvZPXAbso'
p.download(post_id)
"""