"""
Pass drawable.xml as argument to this script for it to be arranged

Ensure all new drawables are listed in the new category and the last new item is followed by a blank line
"""

import sys, os, re

with open(sys.argv[1]) as file:
	lines = file.readlines()
	drawables = []
	google = []
	folder = []

	# Get all in New
	newDrawables = []
	newest = re.compile(r'<category title="New" />')
	drawable = re.compile(r'drawable="([\w_]+)"')
	num = 0

	while lines:
		new = re.search(newest, lines[num])
		if new:
			break
		num += 1

	new = True
	num += 1
	while new:
		new = re.search(drawable, lines[num])
		if new:
			newDrawables.append(new.groups(0)[0])
			num += 1

	newDrawables.sort()

	# collect existing drawables
	for line in lines[num:]:
		new = re.search(drawable, lines[num])
		if new:
			if new.groups(0)[0].startswith('google'):
				google.append(new.groups(0)[0])
			elif new.groups(0)[0].startswith('folder'):
				folder.append(new.groups(0)[0])
			else:
				drawables.append(new.groups(0)[0])
		num += 1

	print(newDrawables)

	drawables += newDrawables

	# remove duplicates and sort
	drawables = list(set(drawables))
	drawables.sort()
	google = list(set(google))
	google.sort()
	folder = list(set(folder))
	folder.sort()

	# build
	output = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n<version>1</version>\n\n\t<category title="New" />\n\t'
	for newDrawable in newDrawables:
		output += '<item drawable="%s" />\n\t' % newDrawable

	output += '\n\t<category title="Google" />\n\t'
	for entry in google:
		output += '<item drawable="%s" />\n\t' % entry

	output += '\n\t<category title="Folders" />\n\t'
	for entry in folder:
		output += '<item drawable="%s" />\n\t' % entry

	output += '\n\t<category title="A" />\n\t'
	letter = "a"

	# iterate alphabet
	for entry in drawables:
		if not entry.startswith(letter):
			letter = chr(ord(letter) + 1)
			output += '\n\t<category title="%s" />\n\t' % letter.upper()
		output += '<item drawable="%s" />\n\t' % entry

	output += "\n</resources>"

	# write to new_'filename'.xml in working directory
	outFile = open("new_" + sys.argv[1].split("/")[-1], "w")
	outFile.write(output)