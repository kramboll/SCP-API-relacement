"""
Made by kramboll - 4th November 2021
Version 1.0
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def get_images(url):
	html_page = urlopen(url)
	soup = BeautifulSoup(html_page, features="html5lib")
	images = []
	for img in soup.findAll('img'):
		images.append(img.get('src'))

	return images


def get_texts(url):
	global output
	html = urlopen(url).read()
	soup = BeautifulSoup(html, features="html.parser")
	for script in soup(["script", "style"]):
		script.extract()

	text = soup.get_text()



	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

	output = [chunk for chunk in chunks if chunk]


def get_data(url_arg):
	get_texts(url_arg)

	sideimgs = get_images('https://scp-wiki.wikidot.com/scp-096')

	imgs = get_images(url_arg)
	images = []
	for img in imgs:
		if not img in sideimgs and not 'thumbnails.wdfiles.com/thumbnail/site/' in img and not 'd2qhngyckgiutd.cloudfront.net/' in img:
			images.append(img)

	for i in output:
		try:
			detector = i.index('Object Class:')
			object_class_full = i
			object_class = i.strip('Object Class: ')
		except ValueError:
			pass
		try:
			detector = i.index('Item #:')
			name_full = i.strip('Item #: ')
			designation = url_arg.strip('https://scp-wiki.wikidot.com/')
			
		except ValueError:
			pass
		try:
			detector = i.index('Special Containment Procedures:')
			special_containment_procedures_full = i
			special_containment_procedures = i.strip('Special Containment Procedures: ')
		except ValueError:
			pass
		try:
			detector = i.index('Description:')
			description_full = i
			description = i.strip('Description: ')
		except ValueError:
			pass

	data = {
		"designation":designation,
		"name":name_full,
		"object_class":object_class,
		"special_containment_procedures":"SCP"+special_containment_procedures,
		"description":description,
		"description_full":description_full,
		"images":images
	}

	return data
