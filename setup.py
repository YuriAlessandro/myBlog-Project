from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pymongo',
]

setup(name='project',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = project:main
      """,
)
