from pyramid.view import (
    view_config,
    view_defaults
    )

import project.resources
from project.blogdata import BlogData
from pyramid.httpexceptions import HTTPFound
import datetime
import pymongo
import urllib, cStringIO
import os
import math

from PIL import Image

@view_config(route_name='home', renderer='project:template/index.jinja2')
def home(request):
    posts = list(request.db['posts'].find())

    return {'name': "Index", 'posts':posts}

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

        return {'name': "Novo Post", 'Success':True}
    return {'name': "Novo Post"}

@view_config(route_name='img_test', renderer='project:template/img_test.jinja2')
def imgtest(request):
    return {'name': "IMGTest"}

@view_config(route_name='img_rotate_confirm', renderer='json')
def save_image(request):
    params = request.params
    img_path = params.get('img_path')
    degrees = -1 * float(params.get('degree'))

    directory = os.path.dirname(os.path.realpath(__file__)) + "/static"

    img = Image.open(directory + "/slide-surf-ilha-grande.jpg")
    img_rotated = img.rotate(degrees)
    # TODO: Dar o croop antes do save
    # img_croped = make_crop(img_rotated, degrees)
    # img_croped.save(directory + "/croped.jpg")
    wr, hr = rotatedRectWithMaxArea(img_rotated, degrees)
    img_crop = crop_around_center(img_rotated, wr, hr)
    img_crop.save(directory + "/teste.jpg")
    img.close()
    url = "/static/teste.jpg"
    return {'url': url}

# def make_crop(img, angle):
#     w, h = img.size

#     return img

def rotatedRectWithMaxArea(img, degrees):
    """
    Given a rectangle of size wxh that has been rotated by 'angle' (in
    radians), computes the width and height of the largest possible
    axis-aligned rectangle (maximal area) within the rotated rectangle.
    """
    angle = math.radians(degrees)
    w, h = img.size
    if w <= 0 or h <= 0:
        return 0,0

    width_is_longer = w >= h
    side_long, side_short = (w,h) if width_is_longer else (h,w)

    # since the solutions for angle, -angle and 180-angle are all the same,
    # if suffices to look at the first quadrant and the absolute values of sin,cos:
    sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
    if side_short <= 2.*sin_a*cos_a*side_long:
        # half constrained case: two crop corners touch the longer side,
        #   the other two corners are on the mid-line parallel to the longer line
        x = 0.5*side_short
        wr,hr = (x/sin_a,x/cos_a) if width_is_longer else (x/cos_a,x/sin_a)
    else:
        # fully constrained case: crop touches all 4 sides
        cos_2a = cos_a*cos_a - sin_a*sin_a
        wr,hr = (w*cos_a - h*sin_a)/cos_2a, (h*cos_a - w*sin_a)/cos_2a

    return wr,hr

def crop_around_center(image_rot, width, height):
    """
    Given a NumPy / OpenCV 2 image, crops it to the given width and height,
    around it's centre point
    """

    w, h = image_rot.size
    image_size = (w, h)
    image_center = (int(image_size[0] * 0.5), int(image_size[1] * 0.5))

    if(width > image_size[0]):
        width = image_size[0]

    if(height > image_size[1]):
        height = image_size[1]

    x1 = int(image_center[0] - width * 0.5)
    # x2 = int(image_center[0] + width * 0.5)
    y1 = int(image_center[1] - height * 0.5)
    # y2 = int(image_center[1] + height * 0.5)

    img_croped = image_rot.crop(
    (
        x1 + 1,
        y1 + 1,
        width,
        height
    ))

    return img_croped