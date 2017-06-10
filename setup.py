#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='Annual',
    version='0.0.1',
    description='An annual report processing tool',
    url='https://github.com/gaojunhuicavon/Annual',
    author='Yongcong Ruan, Zihuai Lin, Han Liu, Junhui Gao',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ],
    keywords='annual information retrieval python',
    packages=['annual', 'annual/parse'],
    install_requires=['python-Levenshtein==0.12.0', 'jieba==0.38']
)
