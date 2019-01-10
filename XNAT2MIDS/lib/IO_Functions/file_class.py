# -*- coding: utf-8 -*-

###############################################################################
# Imports
###############################################################################
import os
import fnmatch
## you can discomment module magic if you want execute python version to
## 3.5 or greater
#import magic

###############################################################################
# Classes section
###############################################################################

"""
Class that define a folder o archve with a path
"""


class FileInfo(object):
    ## The fuction __init__ inicialize the object FileInfo
    def __init__(self, filepath):

        # "is_file" is a bolean variable that describes if the path
        # is a file or not
        self.is_file = os.path.isfile(filepath)

        # "is_dir" is a bolean variable that describes if the path
        # is a directory or not
        self.is_dir = os.path.isdir(filepath)

        # "is_link" is a bolean variable that describes if the path
        # is a link or not
        self.is_link = os.path.islink(filepath)
        # "depth" is a integer variable that describes the depth of a path
        if self.is_dir:
            # if is a directory, the same directory is counted
            self.depth = filepath.strip('/').count('/') + 1
        else:
            self.depth = filepath.strip('/').count('/')
        # "size" is a integer variable that describes the size of a arichive
        # or directory in bytes
        self.size = os.path.getsize(filepath)

        ## you can discomment functions magic if you want execute
        ## python version to 3.5 or greater
 #       m = magic.open(magic.MAGIC_NONE)
 #       m.load()
 #       self.meta = m.file(filepath).lower()
 #       m = magic.open(magic.MAGIC_MIME)
 #       m.load()
 #       self.mime = m.file(filepath)
        # "filepath" is a string variable that describes the complet path
        self.filepath = filepath
        # "path" is a string variable that describes the path to this
        # file or directory
        self.path = "/".join(filepath.split('/')[0:len(filepath.split(
            '/')) - 1]) + '/'
        # "filename" is a string variable that describes the directory
        # or file without extension
        self.filename = filepath.split('/')[len(filepath.split(
            '/')) - 1].split('.')[0]
        # "extension" is a string variable that describes the extension
        # of the file. if it is a directory, the value is a point only
        self.extension = "." + ".".join(filepath.split('.')[1:])

    ## The function match search patterns in the path.
    ##
    ## Return True o False
    def match(self, exp):
        return fnmatch.fnmatch(self.filepath, exp)

    ## the function readfile read the file
    ##
    ## return the archive content
    def readfile(self):
        if self.is_file:
            with open(self.filepath, 'r') as _file:
                return _file.read()

    ## The function read_lines_file open file and search a pattern in file
    ##
    ## return the lines where matches are included
    def read_lines_file(self,match):
        lines=list()
        with open(self.filepath, 'r') as _file:
            for line in _file:
                if fnmatch.fnmatch(line, match):
                    lines.append(line)
        return lines

    ## The fuction __str__
    ##
    ## Return the characteristics of the object at string format
    def __str__(self):
        return str(self.__dict__)


###############################################################################
# Functions
###############################################################################

"""
This function allows the user to visit directories and files depthly
with one given path

Return a iterator with a FileInfo object
"""


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

"""
This function allows the user to visit only directories depthly
with one given path

Return a iterator with a FileInfo object
"""


def get_dirs(root):
    for root, dirs, files in os.walk(root):
        for directory in dirs:
            yield FileInfo(os.path.join(root, directory))

"""
This function allows the user to visit only files depthly
with one given path

Return a iterator with a FileInfo object
"""


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
