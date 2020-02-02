from post import post

p = post('https://www.instagram.com/p/B8Ad6cKAuOH/')

print('post_id: ', p.post_id)
print('post_shortcode: ', p.post_shortcode)
print('dimensions: ', p.dimensions)
print('display_url: ', p.display_url)
print('media_text: ', p.media_text)
print('is_video: ', p.is_video)
print('tagged_users: ', p.tagged_users)
print('captions: ', p.captions)
print('time_stamp: ', p.time_stamp)
print('like_count: ', p.like_count)
print('comment_count: ', p.comment_count)
print('location: ', p.location)
print('owner: ', p.owner)

p.download()