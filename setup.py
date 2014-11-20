from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='nidaba',
    packages=find_packages(),
    url='http://sopython.com/pages/nidaba',
    license='BSD',
    author='Keiron Pizzey',
    author_email='ffisegydd@sopython.com',
    description='Machine learning library for studying Stack Overflow data.',
    install_requires=requirements
    )
    
    
