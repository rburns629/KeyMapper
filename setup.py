import os
from setuptools import setup, find_packages


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT_DIR, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='keymapper',
    version='1.0.0', 
    description='A dynamic dictionary iteration tool that allows you to get and set keys and values with a single key declaration',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/rburns629/KeyMapper',
    author='Robert Burns',
    author_email='rburns629@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='dict dot delimeter key map dynamic',
    packages=find_packages(exclude=['tests']),
    project_urls={
        'Bug Reports': 'https://gitlab.com/rburns629/KeyMapper/issues',
        'Source': 'https://gitlab.com/rburns629/KeyMapper',
    },
)