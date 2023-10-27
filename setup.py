import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "repominer",
    version = "0.0.1",
    author = "Jose Alvarez",
    author_email = "itasahobby@gmail.com",
    description = ("Tool to extract open source projects from bug bounty scopes"),
    license = "MIT",
    keywords = "",
    url = "https://github.com/jalvarezit/repominer",
    packages=['repominer'],
    entry_points = {
        "console_scripts": [
            "repominer = repominer.__main__:main",
        ]
    },
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
    ],
)
