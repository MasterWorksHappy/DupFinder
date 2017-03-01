import logging
import pprint


pp = pprint.PrettyPrinter(indent=4)
logger = logging.getLogger('dupDestroyer')


def log_msg(**kwargs):
    msg = "\n\t\t"
    for k, v in kwargs.iteritems():
        if isinstance(v, dict) or isinstance(v, list):
            v = "\n" + pp.pformat(v)
        msg += '%s: >%s<, ' % (k, v)
    return msg

class jQTree(object):
    def __init__(self):
        # self.tree_list = []
        pass


class DirTreeUI(jQTree):
    def __init__(self, acfg, dup_dirs):
        """
        :param  scope: the dir where the dup search began
        """
        jQTree.__init__(self)
        # self.scope = "\\" + acfg['SEARCH_SCOPE']
        self.dup_dirs = dup_dirs
        scope = acfg['SEARCH_SCOPE']
        self.root_dir = scope
        self.pic_root = acfg['PICS_ROOT']
        self.scope = scope.replace(acfg['PICS_ROOT'] + '\\', '')
        self.dir_list = list()


    # def list_files(self, startpath):
    #     for parent, dirs, files in os.walk(startpath):
    #         # level = parent.replace(startpath, '').count(os.sep)
    #         if parent == self.root_dir:
    #             parent = '#'
    #         for d in dirs:
    #             self.dir_list.append([d, parent, os.path.basename(parent)])
    #             # self.list_files(d)


    # def process_dup_dirs(self, dup_dirs):
    #     """
    #     Only called from jQueryUtils.DirTreeUI#make_tree
    #     takes list of dirs from dup finder and splits them into parent and base
    #     to make an intermediary data structure
    #     :param: dup_dirs, list of dirs containing dups
    #     :return: dir_tree_list:  dirname, parent, base
    #     """
    #     dir_tree_list = list()
    #     # parent, base = self.scope.rsplit('\\', 1)
    #     # dir_tree_list.append([self.scope, '#', self.scope])
    #     for dirname in dup_dirs:
    #         if len(dir_tree_list) == 0 or \
    #                 any(e[0] != dirname for e in dir_tree_list):
    #             if dirname.count('\\') > 0:
    #                 parent, base = dirname.rsplit('\\', 1)
    #             else:
    #                 parent = dirname
    #                 base = dirname
    #             if parent == self.scope:
    #                 parent = '#'
    #             dir_tree_list.append([dirname, parent, base])
    #     logger.debug(log_msg(
    #         dup_dirs=dup_dirs,
    #         imgdir_tree_list_list=dir_tree_list))
    #     return dir_tree_list

    # def make_tree(self, dup_dirs):
    def make_tree(self, dir_list):
        """
        Only called from dupRunner init code
        writes dup dirs into a jQuery - jsTree list[dict{}] structure,
        used for display to the user
        :param dup_dirs: a hierarchical dictionary of dup dirs;
           from DupDestroyer.get_dirs_with_dups
        :return: a jQuery tree: a list of dictionaries
        'tree_data' : [
               { "id" : "a1", "parent" : "#", "text" : "Simple root node" },
               { "id" : "a2", "parent" : "#", "text" : "Root node 2" },
               { "id" : "a3", "parent" : "a2", "text" : "Child 1" },
               { "id" : "a4", "parent" : "a2", "text" : "Child 2" },
            ]
        'tree_dict' : dict of children keyed by parent
        """
        tree_dict = dict()
        for row in dir_list:
            dirname, parent, base = row
            node_dict = self.make_dict_node(base, dirname, parent)
            if parent not in tree_dict:
                tree_dict[parent] = []
            tree_dict[parent].append(node_dict)
        self.tree_dict = self.ck_for_kids(tree_dict)
        # self.tree_dict = self.keep_only_dup_dirs(tree_dict)
        logger.debug(log_msg(
            tree_dict=self.tree_dict
        ))

    def keep_only_dup_dirs(self, sdict):
        """
        review sdict for dirs that actually contain dups in their hierarchy
        do NOT remove a dir if it has children
        """

        lt = len(sdict)
        # 1st pass removes branches of non-dup dirs
        tmp_dict = {k: v for k, v in sdict.iteritems()
                    for d in v if self.is_dup(d)}
        # lt = len(tmp_dict)
        #
        # # 2nd pass removes branches of non-dup dirs
        # tmp_dict = {k: v for k, v in tmp_dict.iteritems()
        #             for d in v if not self.is_dup(d)}
        # lt = len(tmp_dict)

        # # 3rd pass removes the empty nodes
        # tmp_dict = {k: v for k, v in tmp_dict.iteritems()
        #             if k not in self.dup_dirs}
        # lt = len(tmp_dict)


        # dir_list = {}
        # tbd = list()
        # for k, v in sdict.iteritems():
        #     orig = v
        #     for d in v:
        #         disp_dir = self.is_dup(d)
        #         if disp_dir not in dup_dirs:
        #             if 'children' in d:
        #                 tbd.append(d['id'])
        #             else:
        #                 orig.remove(d)
        # tbd = set(tbd)

        # diffs = self.diff(tmp_dict, self.dup_dirs)

        return tmp_dict




    def is_dup(self, d):
        disp_dir = d['id'].replace(self.pic_root + '\\', '')
        return disp_dir in self.dup_dirs

    def ck_for_kids(self, sdict):
        """
        review sdict for parents with children, set 'children'
        to True, if yes
        sdict: dict of children by parent
        """
        for k, v in sdict.iteritems():
            for d in v:
                if d['id'] in sdict.keys():
                    d['children'] = True
        return sdict

    def make_dict_node(self, base, dirname, parent):
        node_dict = {
            'id': dirname,
            'parent': parent,
            'text': base
        }
        return node_dict

    def get_tree_branch_dict(self, dir_id):
        x = self.tree_dict[dir_id]
        logger.debug(log_msg(
            dir_id=dir_id,
            tree_dict=x))
        return x


def reset_web_prefix(url):
    """
    add web prefix 'static' to path for image display by server
    C:\Users\Michele\PycharmProjects\DupFinder\static\media\pics
    """
    url = "\\static\\media\\pics\\" + url  # TODO make setable config var
    url = url.replace('\\', '/')
    return url


def get_pic_url(url):
    return '<img src="' + reset_web_prefix(url) + '" class="img-circle" width="75" height="75">'


def process_img_urls(img_urls=None):
    """
    :param img_urls:
        list([
            ["\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 03 - Copy.jpg",
             "\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 03.jpg"],
            ["\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 04 - Copy.jpg",
             "\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 04.jpg"]
            ])
    :return:
        # osLeafPath, osLeafPath of parent, text/display item, state dict entry
    """
    img_list = list()
    parent_id = '#'
    for hash_id, result_list in img_urls.iteritems():
        img_list.append([hash_id, parent_id, get_pic_url(result_list[0]), True])  # hash level rec with pic
        entry_id = 0
        for url in result_list:
            clickable = '<a href="%s">"%s"</a>' % (reset_web_prefix(url), url)
            img_list.append([url, hash_id, clickable, False])  # dup img level rec, text only
            entry_id += 1
    logger.debug(log_msg(
        img_urls=img_urls,
        img_list=img_list))
    return img_list  # id, parent_id, display_item, state


class ImgTreeUI(jQTree):
    def __init__(self):
        jQTree.__init__(self)
        # self.tree_list = list()

    def make(self, img_urls):
        """
        writes dup imgs into a jQuery - jsTree list[dict{}] structure,
        used for display to the user
        img_urls: a list of lists of dup imgs, grouped by hashes
        a jQuery tree: a list of dictionaries
        'tree_dict' : dict of children keyed by parent
        """
        self.tree_dict = dict()
        for row in process_img_urls(img_urls=img_urls):
            url, parent_url, display_item, state = row
            parent_url = str(parent_url)
            row_dict = {
                'id': url,
                'parent': parent_url,
                'text': display_item,
                'icon': False
            }
            if state:
                row_dict['children'] = True
                row_dict['state'] = {
                    'opened': True,
                    'selected': False
                }
            # self.tree_list.append(row_dict)
            if parent_url not in self.tree_dict:
                self.tree_dict[parent_url] = []
            self.tree_dict[parent_url].append(row_dict)
        # if len(self.tree_list) == 1:  # only contains header, reset to null
        #     self.tree_list = list()
        logger.debug(log_msg(
            img_urls=img_urls,
            tree_dict=self.tree_dict))

    def get_tree_branch_dict(self, pic_id):
        x = self.tree_dict[pic_id]
        logger.debug(log_msg(
            pic_id=pic_id,
            tree_dict=x))
        return x


if __name__ == '__main__':
    dirs = list([
        "_from Otto\\_before pictures\\1990's\\1993",
        "_from Otto\\_before pictures\\1990's\\1992",
        "_from Otto\\_before pictures\\1990's\\1995",
        "_from Otto\\_before pictures\\1990's\\1994",
        "_from Otto\\_before pictures\\1990's\\1997",
        "_from Otto\\_before pictures\\1990's\\1996",
        "_from Otto\\_before pictures\\1990's\\1998"
    ])

    dT = DirTreeUI(r"_from Otto\\_before pictures\\1990's")
    dir_tree = dT.get_dir_tree(dirs)
    print dT

    imgs = list([
        ["\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 03 - Copy.jpg",
         "\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 03.jpg"],
        ["\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 04 - Copy.jpg",
         "\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 04.jpg"],
        ["\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 05 - Copy.jpg",
         "\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 05.jpg"],
        ["\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 06 - Copy.jpg",
         "\\_from Otto\\_before pictures\\1990's\\1993\\19930115 - 06.jpg"]
    ])
    iT = ImgTreeUI()
    iT.make(imgs)
    print iT
