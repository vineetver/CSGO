from setuptools import setup, find_packages

setup(
    name='CSGO',
    version='0.1',
    description='This package contains the code for the CSGO competitive scene analysis',
    author='Vineet Verma',
    author_email='vineetver@hotmail.com',
    packages=find_packages(exclude=['tests']),
    install_requires=[],
    entry_points={
        'console_scripts': [
        ],
    }
)