# -*- coding: utf-8 -*-
# $File: group.py
# $Date: Mon Oct 08 14:05:39 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""Implementing :class:`Group<ftp9.group.Group>` class and define authorization strategy."""

import os
import os.path
import shutil

from ftp9.config import config
from ftp9.utils import relpath, fs_enc

class Group(object):
    """group information and authorization strategy"""
    authed_users = None
    """set(<str>), authorized users"""

    class Node(object):
        name = None

        children = None
        """list<Node>, children of this node"""

        parent = None
        """Node, the parent"""

        users = None
        """set<unicode>, names of users directly belonging to this group"""

        admins = None
        """set<unicode>, admins of this group"""

        public_read = None
        """set<unicode>, users with public read permission"""
        public_write = None
        """set<unicode>, users with public write permission"""
        public_modify = None
        """set<unicode>, users with public modify permission"""
        private_read = None
        """set<unicode>, users with private read permission"""
        private_write = None
        """set<unicode>, users with private write permission"""
        private_modify = None
        """set<unicode>, users with private modify permission"""

        def __init__(self):
            for i in 'public', 'private':
                for j in 'read', 'write', 'modify':
                    setattr(self, i + '_' + j, set())

    _timestamp = None
    _root = None
    _path2grp = None

    def update(self, api):
        """update group information and corresponding filesystem structure
        using an :class:`Acnt9API <ftp9.api.Acnt9API>` instance."""
        t = api.get_group_timestamp()
        if t != self._timestamp:
            self._timestamp = t
            self._update_structure(api)
            self._update_fs()
            self._update_perm()

    def get_node_by_path(self, path):
        """return the corresponding Node for filesystem path ``path``, or None
        on error"""
        path = fs_enc(path)
        while path[-1] == u'/':
            path = path[:-1]
        return self._path2grp.get(path)

    def _update_structure(self, api):
        name2grp = dict()
        for i in api.get_group_info():
            g = Group.Node()
            for j in 'children', 'users', 'admins':
                setattr(g, j, i[j])
            g.name = i['title']
            name2grp[i['name']] = g

        for i in name2grp.itervalues():
            for j in range(len(i.children)):
                ch = name2grp[i.children[j]]
                i.children[j] = ch
                ch.parent = i

        self._root = name2grp[config.ROOTGRP_NAME]


    def _update_fs(self):
        pjoin = os.path.join
        path2grp = dict()

        def get_grpname(fname):
            t = fname.split('-', 1)
            if len(t) == 1:
                return None
            return t[1]

        def walk(node, rootdir):
            path2grp[rootdir] = node

            create_list = set([i.name for i in node.children])
            if node is self._root:
                create_list.add(config.ROOT_PUB_NAME)
            else:
                create_list.add(config.PUBLIC_NAME)
                create_list.add(config.PRIVATE_NAME)

            remove_list = set()
            if os.path.isdir(rootdir):
                for i in os.listdir(rootdir):
                    if os.path.isdir(pjoin(rootdir, i)):
                        remove_list.add(fs_enc(i))

            intersect = create_list & remove_list
            create_list -= intersect
            remove_list -= intersect

            for i in create_list:
                os.makedirs(pjoin(rootdir, i))

            for i in remove_list:
                p0 = pjoin(rootdir, i)
                if config.FTP_DISCARDEDGRP_SAVEDIR:
                    tgt_dir = pjoin(
                            config.FTP_DISCARDEDGRP_SAVEDIR,
                            self._timestamp,
                            relpath(rootdir))
                    if not os.path.isdir(tgt_dir):
                        os.makedirs(tgt_dir)
                    shutil.move(p0, tgt_dir)
                else:
                    shutil.rmtree(p0)

            for i in node.children:
                walk(i, pjoin(rootdir, i.name))
        
        walk(self._root, config.FTP_ROOT)

        self._path2grp = {fs_enc(k): v for k, v in path2grp.iteritems()}


    def _update_perm(self):

        def add_to_root(node, fields, user):
            while node:
                for i in fields:
                    getattr(node, i).update(user)
                node = node.parent

        def add_to_subtree(node, fields, user):
            for i in fields:
                getattr(node, i).update(user)
            for i in node.children:
                add_to_subtree(i, fields, user)

        alluser = set()
        for g in self._path2grp.itervalues():
            alluser.update(g.users, g.admins)
        self.authed_users = alluser
        add_to_subtree(self._root, ['public_read'], alluser)

        for g in self._path2grp.itervalues():
            curuser = g.users + g.admins
            add_to_subtree(g, ['private_read'], curuser)
            add_to_root(g, ['private_read'], curuser)

            add_to_root(g, ['public_write', 'private_write'], curuser)
            add_to_subtree(g, ['public_write', 'private_write'], g.admins)

            add_to_subtree(g, ['public_modify', 'private_modify'], g.admins)
