from setuptools import setup, find_packages

name = "pycon"
version = "0.1"

setup(
    name=name,
    version=version,
    description="PyconPL 2013 Riddles",
    long_description='',
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords="",
    author="",
    author_email='',
    url='',
    license='',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # framework
        'Flask',
        # forms
        #'flask-wtf',
        # PostreSQL driver
        'psycopg2',
        # framework ORM integration
        'Flask-SQLAlchemy',
        'gevent'
    ],
    entry_points="""
    [console_scripts]
    run = pycon.riddles:run
    init_db = pycon.riddles:init_db
    gen_tokens = pycon.riddles:gen_tokens
    free_tokens = pycon.riddles:free_tokens
    prod_run = pycon.runner:main
    """,
)
