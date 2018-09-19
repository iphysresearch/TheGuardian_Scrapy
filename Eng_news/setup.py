# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='scrapy-mymodule',
	entry_points={
		'scrapy.commands': [
			'crawlall=Eng_news.commands:crawlall',
			],
		},
	)