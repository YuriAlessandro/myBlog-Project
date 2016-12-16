class BlogData(object):
	def __init__(self, request):
		self.settings = request.registry.settings
		self.collection = request.db['blogExample']

	def get_recent_posts(self, num_of_entries, page, titles_only=False):
		row = num_of_entries * (page - 1)
		entries = self.collection.find({'active': True}).sort('_id', -1)[row: row + num_of_entries]
		if titles_only:
			titles = []
			for entry in entries:
				this_entry = {'title': entry['title'], 'url': entry['url']} 
				titles.append(this_entry)
			return titles
		else:
			return entries

	def get_post_by_url(self, url):
		post = self.collection.find_one({'url': url})
		return post

	def get_recent_posts_by_category(self, category, num_of_entries, page):
		row = num_of_entries * (page - 1)
		entries = self.collection.find({'category': category, 'active': True}).sort('_id', -1)[row: row + num_of_entries]
		return entries