#!/usr/bin/env python3

import argparse
import glob
import os
from os import path
import shutil
import sqlite3

import bs4
from bs4 import BeautifulSoup

PLIST = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleIdentifier</key>
	<string>pep</string>
	<key>CFBundleName</key>
	<string>Python Enhancement Proposals</string>
	<key>DashDocSetKeyword</key>
	<string>pep</string>
	<key>DashDocSetPluginKeyword</key>
	<string>pep</string>
	<key>DocSetPlatformFamily</key>
	<string>usercontribPEP</string>
	<key>dashIndexFilePath</key>
	<string>www.python.org/dev/peps/index.html</string>
	<key>isDashDocset</key>
	<true/>
</dict>
</plist>
"""


def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('docset')
	return parser


def make_dir_if_not_exist(p):
	try:
		os.makedirs(p)
	except FileExistsError:
		pass

	
def create_index(config):
	base_dir = path.abspath(config.docset)
	resource_dir = path.join(base_dir, 'Contents/Resources/')
	document_dir = path.join(resource_dir, 'Documents')
	content_dir = path.join(document_dir, 'www.python.org/dev/peps')
	
	db = sqlite3.connect(path.join(resource_dir, 'docSet.dsidx'))
	cur = db.cursor()

	try:
		cur.execute('DROP TABLE searchIndex;')
	except:
		pass
	cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
	cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

	os.chdir(content_dir)
	pep_pages = glob.glob('pep-*')
	for i, folder_name in enumerate(pep_pages):
		if folder_name == 'pep-xxxx':
			continue    # skip pep-xxxx
		index_file = path.join(folder_name, 'index.html')
		title = extract_title_from_page(index_file)
		rel_path = path.relpath(index_file, document_dir)
		cur.execute(
			'INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
			(title, 'guide', rel_path))
		print("{} of {} transformed".format(i + 1, len(pep_pages)))

	db.commit()
	db.close()
	

def extract_title_from_page(filepath):
	with open(filepath) as fin:
		soup = BeautifulSoup(fin)
		title = soup.find_all('h1', class_='page-title')[0]
		return title.string


def main():
	parser = create_parser()
	config = parser.parse_args()
	create_index(config)


if __name__ == '__main__':
	main()
