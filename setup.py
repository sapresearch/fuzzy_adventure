try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Fuzzy Adventure - SAP questions-answers system',
    'author': '',
    'url': 'https://github.com/sapresearch/fuzzy_adventure.',
    'download_url': 'Where to download it.',
    'author_email': '',
    'version': '0.1',
    'install_requires': ['nose', 'scikit-learn', 'pandas', 'numpy', 'scipy', 'nltk'],
    'packages': ['fuzzy_adventure'],
    'scripts': [],
    'name': 'Fuzzy Adventure'
}

setup(**config)