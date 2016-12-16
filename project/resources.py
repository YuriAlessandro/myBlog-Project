class Root(object):
    __name__ = ''
    __parent__ = None

    def __init__(self, request):
        pass

    def __getitem__(self, key):
        if key == 'post':
            return Post()
        elif key == 'category':
            return Category()
        raise KeyError


class Post(object):
    __name__ = ''
    __parent__ = Root

    def __init__(self):
        pass

    def __getitem__(self, key):
        if key:
            return PostName(key)
        raise KeyError

class PostName(object):
    def __init__(self, name):
        self.__name__ = name


class Category(object):
    __name__ = ''
    __parent__ = Root

    def __init__(self):
        pass

    def __getitem__(self, key):
        if key:
            return CategoryName(key)
        raise KeyError

class CategoryName(object):
    def __init__(self, name):
        self.__name__ = name