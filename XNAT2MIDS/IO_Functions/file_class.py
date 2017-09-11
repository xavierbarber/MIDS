# -*- coding: utf-8 -*-

###############################################################################
# Imports
###############################################################################
import os
import magic
import fnmatch

###############################################################################
# Classes section
###############################################################################

## Class that define a folder o archve with a path
class FileInfo(object):

    def __init__(self, filepath):


        self.is_file = os.path.isfile(filepath)
        self.is_dir = os.path.isdir(filepath)
        self.is_link = os.path.islink(filepath)
        if self.is_dir:
            self.depth = filepath.strip('/').count('/') + 1
        else:
            self.depth = filepath.strip('/').count('/')
        self.size = os.path.getsize(filepath)
        m = magic.open(magic.MAGIC_NONE)
        m.load()
        self.meta = m.file(filepath).lower()
        m = magic.open(magic.MAGIC_MIME)
        m.load()
        self.mime = m.file(filepath)
        self.filepath = filepath
        self.path = "/".join(filepath.split('/')[0:len(filepath.split(
            '/')) - 1]) + '/'
        self.filename = filepath.split('/')[len(filepath.split(
            '/')) - 1].split('.')[0]

        self.extension = "." + ".".join(filepath.split('.')[1:])

    def match(self, exp):
        return fnmatch.fnmatch(self.filepath, exp)

    def readfile(self):
        if self.is_file:
            with open(self.filepath, 'r') as _file:
                return _file.read()

    def read_lines_file(self,match):
        with open(self.filepath, 'r') as _file:
            for line in _file:
                if fnmatch.fnmatch(line, match):
                    return line

    def __str__(self):
        return str(self.__dict__)


###############################################################################
# Functions
###############################################################################

## this function allow the user to visit directories and files depthly
## with one given path
def get_dirs_and_files(root):
    for root, dirs, files in os.walk(root):
        for directory in dirs:
            yield FileInfo(os.path.join(root, directory))
            for filename in directory:
                filename = os.path.join(root, filename)
                if os.path.isfile(filename) or os.path.isdir(filename):
                    yield FileInfo(filename)

        for filename in files:
            filename = os.path.join(root, filename)
            if os.path.isfile(filename) or os.path.isdir(filename):
                yield FileInfo(filename)

## this function allow the user to visit only directories depthly
## with one given path
def get_dirs(root):
    for root, dirs, files in os.walk(root):
        for directory in dirs:
            yield FileInfo(os.path.join(root, directory))

## this function allow the user to visit only files depthly
## with one given path
def get_files(root):
    for root, dirs, files in os.walk(root):
        for directory in dirs:
            for filename in directory:
                filename = os.path.join(root, filename)
                if os.path.isfile(filename) or os.path.isdir(filename):
                    yield FileInfo(filename)

        for filename in files:
            filename = os.path.join(root, filename)
            if os.path.isfile(filename) or os.path.isdir(filename):
                yield FileInfo(filename)