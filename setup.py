import os
from setuptools import setup, find_packages


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT_DIR, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='keymapper',
    version='1.0.5',
    license='MIT',
    description='Dictionary key mapping tool that enables the user to declare a single keyword regardless of depth.',
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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='dict dot delimiter key map dynamic dictionary object notation',
    packages=find_packages(exclude=['tests']),
    project_urls={
        'Bug Reports': 'https://gitlab.com/rburns629/KeyMapper/issues',
        'Source': 'https://gitlab.com/rburns629/KeyMapper',
    },
)