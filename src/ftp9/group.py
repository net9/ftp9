# -*- coding: utf-8 -*-
# $File: group.py
# $Date: Fri Jul 13 14:56:08 2012 +0800
# $Author: jiakai <jia.kai66@gmail.com>

import os
import os.path
import shutil

from ftp9.config import config

class Group(object):
    """group information"""
    class Node(object):
        name = None
        children = None
        parent = None

        dirname = None

        users = None
        admins = None

    _timestamp = None
    _root = None

    def update(self, api):
        t = api.get_group_timestamp()
        if t != self._timestamp:
            self._timestamp = t
            self._update_structure(api)
            self._update_fs()


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
                ch.parent = i
                ch.dirname = fmt.format(j, ch.name)

        self._root = name2grp['authorized']


    def _update_fs(self):
        pjoin = os.path.join

        def get_grpname(fname):
            t = fname.split('-', 1)
            if len(t) == 1:
                return None
            return t[1]

        def walk(node, rootdir):
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
