#!/usr/bin/python3

import os
import sys

class Dir:
	def __init__(self, path, parent):
		self.path = path
		self.parent = parent
		self.children = {}
		self.size = 0
		self.count = 0
	
	def getOrCreatePath(self, path):
		if self.path == path:
			return self
		elif not path.startswith(self.path):
			return self.parent.getOrCreatePath(path)
		else:
			relative_path = path[len(self.path):]
			
			if not '/' in relative_path:
				return self
			
			child_name = relative_path[0:relative_path.index('/') + 1]
			
			if not child_name in self.children:
				child_path = os.path.join(self.path, child_name)
				self.children[child_name] = Dir(child_path, self)
			
			return self.children[child_name].getOrCreatePath(path)
	
	def updateHierarchyWithFile(self, size):
		if self.parent != None:
			self.parent.updateHierarchyWithFile(size)
			
		self.count = self.count + 1
		self.size = self.size + size
	
	def depth(self):
		if self.parent != None:
			return self.parent.depth() + 1;
		
		return 0

root = Dir('/', None)
	
def analyze(s3_ls_output_file):
	with open(s3_ls_output_file, 'r') as file:
		for line in file.readlines():
			parts = line.split()
			size = parts[2]
			
			if size == '0':
				continue
			
			path = parts[3]
			folder = root.getOrCreatePath('/' + path)
			
			folder.updateHierarchyWithFile(int(size))

def sizeof_fmt(num, suffix='B'):
	for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
		if abs(num) < 1024.0:
			return f'{num:3.1f}{unit}{suffix}'
		num /= 1024.0
	return f'{num:.1f}Y{suffix}'

def print_dir(directory, depth):
	print('{}{} [size: {}] [count: {}]'.format('\t' * depth, directory.path, sizeof_fmt(directory.size), directory.count))
	
	for child in directory.children:
		print_dir(directory.children[child], depth + 1)

def print_level_dirs(directory, depth, desired_level):
	if depth > desired_level:
		return
	
	if desired_level == directory.depth():
		print('{} [size: {}] [count: {}]'.format(directory.path, sizeof_fmt(directory.size), directory.count))
	
	for child in directory.children:
		print_level_dirs(directory.children[child], depth + 1, desired_level)

analyze(sys.argv[1])

for x in range(0, 4):
	print('-----------LEVEL-{} BEGIN-----------'.format(x))
	print_level_dirs(root, 0, x)
	print('-----------LEVEL-{} END-----------'.format(x))
	print('')

print_dir(root, 0)
