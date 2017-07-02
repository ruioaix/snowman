from setuptools import setup, find_packages

setup(
    name = 'xqportfolio',
    version = '0.1.0',
    description = 'An interactive system for portfolios on xueqiu.com',
    url = 'https://github.com/RuiOAIX/XueQiuPortfolio',
    author = 'Rui OAIX',
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
    packages = ['xqportfolio'],
    install_requires = ['requests'],
)
