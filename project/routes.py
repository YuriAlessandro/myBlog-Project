def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('insert', '/insert')
    config.add_route('img_test', '/img')
    config.add_route('img_rotate_confirm', '/saveImg')
    config.scan('.views')