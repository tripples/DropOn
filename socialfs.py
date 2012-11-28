#!/usr/bin/env python
# -*_ coding: utf-8 -*-
"""
Usage:
SocialFs.py
"""
import fuse
import time
import stat
import errno
import os
import slog

fuse.fuse_python_api = (0, 2)

class  ShareStat(fuse.Stat):
    """
    ShareStat : Class for Managing stat for each file
    @fuse.Stat : Inherites fuse.Stat object
    """

    def __init__(self):
        """
        @st_mode : Object types and permissions, Protection
        @st_ino : Inode number
        @st_dev : Id of device containing file
        @st_nlink : No of links for given files
        @st_uid : User ID of the  owner
        @st_gid : Group ID of the  owner
        @st_size : Total size in bytes
        @st_atime : Time when the object was last accessed
        @st_mtime : Time when the object was last modified
        @st_citme : Time when the object's metadata was last modified
        For more help give command 'man stat64'
        """
        #slog.info("ShareStat=>init")
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = os.getuid()
        self.st_gid = os.getgid()
        self.st_size = 4096
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0
        self.set_time()

    def set_time(self):
        """
        set atime,mtime,ctime
        in stat everytime
        returns nothing
        """
        #slog.info("ShareStat=>set_time")
        self.st_atime = int(time.time())
        self.st_mtime = int(time.time())
        self.st_ctime = int(time.time())

    def set_dir_attr(self):
        """
        Set attributes for directory
        S_IFDIR : Current path directory
        """
        #slog.info("ShareStat=>set_dir_attr")
        self.st_mode = stat.S_IFDIR | 0775
        self.st_nlink = 2
        self.set_time()

    def set_file_attr(self, size=0):
        """
        Purpose: Set attributes of a file
        size:int the file's size in bytes
        """
        #slog.info("ShareStat=>set_file_attr")
        self.st_mode = stat.S_IFREG | 0776
        self.st_nlink = 1
        self.st_size = size
        self.set_time()

class ShareFS(fuse.Fuse):
    """
    ShareFS : Extends fuse.Fuse
    Defines different methods for filesystem
    """

    def __init__(self, *args, **kwargs):
        """
        Call fuse.Fuse constructor with given
        arguments
        """
        slog.info("ShareFS=>init")
        fuse.Fuse.__init__(self, *args, **kwargs)
        self.directories = {}
        self.files = {}
        self.codec = 'utf-8'

    def getattr(self, path,**kwargs):
        """
        Getattr for filesystem
        return stat for given path
        """
        st = ShareStat()
        if os.path.exists(path):
            slog.info("ShareFS=>getattr" + str(path)+str(kwargs))
        else:
	    if path in self.files.keys():
		st.set_dir_attr()
		return st
            slog.info(str(path) + 'getattr=>return -errno.ENOENT')
            return -errno.ENOENT

        if os.path.isdir(path):
            st.set_dir_attr()
            return st

        elif os.path.isfile(path):
            st.set_file_attr()
            return st

        else:
            return -errno.ENOENT

    def readdir(self, path, offset,**kwargs):
        """
        Read directory
        """
        slog.info("ShareFS=>readdir" + str(path)+str(offset)+str(kwargs))
        for e in '.', '..',self.directories.keys(),'/':
	            yield fuse.Direntry(e)

    def fsinit(self,**kwargs):
        """
        fsinit
        """
        slog.info("ShareFS=>fsinit"+str(kwargs))
        execfile("main.py")
        return 0

    def open(self, path, flags, **kwargs):
        """
        Read all files in working directory.
        """
        slog.info("ShareFS=>open"+str(path)+str(flags)+str(kwargs))
        # Only support for 'READ ONLY' flag

        return 0


    def create(self, path, flags=None, mode=None, **kwargs):
    	#Create call when we have to create new file
        slog.info("ShareFS=>create"+str(path)+str(flags)+str(mode)+str(kwargs))
	self.files[path] = 0
	return open (name, O_WRONLY | O_CREAT | O_TRUNC, mode);

    def write(self, path, length, offset, **kwargs):
        """
        Write call to write some content in file
        """
        slog.info("ShareFS=>write"+str(path)+str(length)+str(offset)+str(kwargs))
        #self.files[path][:offset]
	return 0
        return -errno.ENOENT

    def read(self, path, length, offset, **kwargs):
        """
        Read all files in working directory.
        """
        slog.info("ShareFS => read"+str(path)+str(length)+str(offset)+str(kwargs))
        self.files[path] = open(path,'r').read()
        #determine begining of our reading
        start = offset
        #determine end of our reading
        end = start + length
        return data[start:end]
        return 'This is just interface'

    def mknod(self, path, mode, dev,**kwargs):
        """
        Mknod
        """
        slog.info("ShareFS => mknod " + str(path)+str(mode)+str(kwargs))
        fd = open(path, O_WRONLY | O_CREAT | O_TRUNC,0644)
        return fd
        return -errno.ENOENT

    def unlink(self, path, **kwargs):
        """
        unlink
        """
        slog.info("ShareFS=> unlink" + str(path) + str(kwargs))
        return -errno.ENOENT

    def rename(self, old, new):
        """
        rename
        """
        slog.info("ShareFS=>rename" + str(old) +str(new))
        return -errno.ENOENT

    def trucate(self, path, len, fh, **kwargs):
        """
        trucate
        """
        slog.info("ShareFs=>trucate" + str(path)+str(kwargs))
        return -errno.ENOENT

    def release(self, path, fh, **kwargs):
        """
        release
        """
        slog.info("ShareFS=>release" + str(path) + str(kwargs))
        return -errno.ENOENT

    def mkdir(self, path, **kwargs):
        """
        mkdir
        """
        slog.info("ShareFs=>mkdir" + str("mkdir") + str(kwargs))
        os.mkdir(path)
        return 0

    def rmdir(self, path, **kwargs):
        """
        rmdir
        """
        slog.info("ShareFS=>rmdir" + str(path) + str(kwargs))
        os.rmdir(path)
        return 0
        return -errno.ENOENT

    def chmod(self, path, mode, **kwargs):
        """
        chmod
        """
        slog.info("ShareFs=>chmod"+ str(path) + str(kwargs))
        os.chmod(path,mode)
        return 0
        return -errno.ENOENT

    def chown(self, path, uid, gid, **kwargs):
        """
        chown
        """
        slog.info("ShareFS=>chown"+str(path) + str(kwargs))
        return -errno.ENOENT


def loop():
    """
    This is where actual file system
    start working
    """
    usage = 'SocialFs a virtual Filesytem to manage a social accounts' + \
        fuse.Fuse.fusage
    sfs = ShareFS(version = '%prog' + fuse.__version__,
                  usage = usage,
                  dash_s_do = 'setsingle')
    sfs.parse(errex = 1)
    sfs.main()

if __name__ == '__main__':
    loop()
