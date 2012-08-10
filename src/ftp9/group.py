# -*- coding: utf-8 -*-
# $File: group.py
# $Date: Thu Aug 02 17:43:18 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

import os
import os.path
import shutil

from ftp9.config import config

class Group(object):
    """group information and authorization strategy"""
    class Node(object):
        name = None
        children = None
        """list<Node>, children of this node"""

        parent = None
        """Node, the parent"""

        dirname = None
        """unicode, name of the corresponding directory"""

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
        t = api.get_group_timestamp()
        if t != self._timestamp:
            self._timestamp = t
            self._update_structure(api)
            self._update_fs()
            self._update_perm()

    def get_node_by_path(self, path):
        """return the corresponding Node for filesystem path ``path``, or None
        on error"""
        while path[-1] == '/':
            path = path[:-1]
        return self._path2grp.get(path)

    def _update_structure(self, api):
        name2grp = dict()
        for i in api.get_group_info():
            g = Group.Node()
            for j in 'children', 'users', 'admins':
                g.__setattr__(j, i[j])
            g.children.sort()
            g.name = i['title']
            name2grp[i['name']] = g

        for i in name2grp.itervalues():
            fmt = u'{{0:0>{}}}-{{1}}'.format(len(str(len(i.children))))
            i.children.sort()
            for j in range(len(i.children)):
                ch = name2grp[i.children[j]]
                i.children[j] = ch
                ch.dirname = fmt.format(j, ch.name)
                ch.parent = i

        self._root = name2grp['authorized']


    def _update_fs(self):
        pjoin = os.path.join
        self._path2grp = dict()

        def get_grpname(fname):
            t = fname.split('-', 1)
            if len(t) == 1:
                return None
            return t[1]

        def walk(node, rootdir):
            self._path2grp[rootdir] = node

            if not os.path.isdir(pjoin(rootdir, 'public')):
                os.makedirs(pjoin(rootdir, u'public'))
                os.makedirs(pjoin(rootdir, u'private'))

            target_list = set([i.dirname for i in node.children])
            flist = set([i.decode(config.FILESYSTEM_ENCODING) if isinstance(i, str)
                    else i for i in os.listdir(rootdir)])
            flist.remove(u'public')
            flist.remove(u'private')

            if target_list != flist:
                grpname2fname = dict()
                for i in flist:
                    grpname2fname[get_grpname(i)] = i

                # create new dirs
                for i in target_list:
                    if i in flist:
                        flist.remove(i)
                        continue
                    orig = grpname2fname.get(get_grpname(i))
                    tgt = pjoin(rootdir, i)
                    if orig:
                        shutil.move(pjoin(rootdir, orig), tgt)
                        flist.remove(orig)
                    else:
                        os.makedirs(tgt)

                # remove unused dirs
                for i in flist:
                    p0 = pjoin(rootdir, i)
                    if config.FTP_DISCARDED_GROUP:
                        tgt_dir = pjoin(
                                config.FTP_DISCARDED_GROUP,
                                self._timestamp,
                                os.path.relpath(rootdir, config.FTP_ROOT))
                        if not os.path.isdir(tgt_dir):
                            os.makedirs(tgt_dir)
                        shutil.move(p0, tgt_dir)
                    else:
                        shutil.rmtree(p0)

            for i in node.children:
                walk(i, pjoin(rootdir, i.dirname))
        
        walk(self._root, config.FTP_ROOT)


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
        add_to_subtree(self._root, ['public_read'], alluser)

        for g in self._path2grp.itervalues():
            curuser = g.users + g.admins
            add_to_subtree(g, ['private_read'], curuser)
            add_to_root(g, ['private_read'], curuser)

            add_to_root(g, ['public_write', 'private_write'], curuser)
            add_to_subtree(g, ['public_write', 'private_write'], g.admins)

            add_to_subtree(g, ['public_modify', 'private_modify'], g.admins)
