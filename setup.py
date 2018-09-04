# -*- coding: utf-8 -*-

'''setup.py - Waqas Bhatti (wbhatti@astro.princeton.edu) - Nov 2016


'''
from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

# let's be lazy and put requirements in one place
# what could possibly go wrong?
with open('requirements.txt') as infd:
    INSTALL_REQUIRES = [x.strip('\n') for x in infd.readlines()]

###############
## RUN SETUP ##
###############

setup(
    name='fits_to_stamps',
    version='0.0.4',
    description=('A simple script to convert FITS images to 3 x 3 stamps.'),
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords='astronomy',
    url='https://github.com/waqasbhatti/fits-to-stamps',
    author='Waqas Bhatti',
    author_email='waqas.afzal.bhatti@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts':[
            'fits-to-stamps=fits_to_stamps.fits_to_stamps:main',
        ],
    },
    zip_safe=False,
)
