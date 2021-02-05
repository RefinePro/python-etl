from setuptools import setup, find_packages

setup(
    name='refinepro-python-etl',
    # url='https://bitbucket.org/refinepro_team/refinepropy/src/master/',
    version='0.1.0',
    author="RefinePro",
    author_email='curious@refinepro.com',

    description="RefinePro ETL utilities in Python",
    long_description="RefinePro common python library",
    long_description_content_type="text/markdown",
    classifiers=[],
    keywords='',
    license='BSD',
    zip_safe=False,
    extras_require={
        'test': ['pytest'],
    },
    packages=find_packages(),
    install_requires=[
        "cement", "peewee", "peewee-db-evolve", "python-json-logger", "rich", "colorlog", "python-dotenv"
    ],
    entry_points={},
)
