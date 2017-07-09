import os
from setuptools import setup, find_packages

version = {}
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'snowman', 'version.py'), 'r') as f:
    exec(f.read(), version)

setup(
    name = 'snowman',
    version = version['__version__'],
    description = 'An interactive system for portfolios on xueqiu.com',
    url = 'https://github.com/ruioaix/snowman',
    author = 'rui oaix',
    author_email = 'rui.oaix@gmail.com',
    license = 'MIT',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages = ['snowman'],
    install_requires = ['requests'],
    entry_points = {
        'console_scripts': [
            'snowman = snowman:main',
        ]
    }
)
