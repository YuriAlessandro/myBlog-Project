from .meta import Base
from pymongo import MongoClient
import urllib

class User(Base):
	def set_password(self, pw):
		
