from pyramid.view import (
    view_config,
    view_defaults
    )

import project.resources
from project.blogdata import BlogData
from pyramid.httpexceptions import HTTPFound
import datetime
import pymongo

@view_config(route_name='home', renderer='project:template/index.jinja2')
def home(request):
    posts = list(request.db['posts'].find())

    return {'posts':posts}

@view_config(route_name='insert', renderer='project:template/insertPost.jinja2')
def insert(request):
    params = request.params
    title = params.get('title')
    author = params.get('author')
    content = params.get('content')
    # p_id = title.strip()

    if request.POST and title and author:
        post = {
            'title': title,
            'author': author,
            'content': content,
        }

        request.db['posts'].insert(post)

        return {'Success':True}
    return {}
