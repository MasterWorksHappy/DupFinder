import pprint

pp = pprint.PrettyPrinter(indent=4)


class jQTree(object):
    def __init__(self):
        self.pp = pprint.PrettyPrinter(indent=4)
        self.tree_list = []
        self.tree_dict = {}


class DirTreeUI(jQTree):
    def __init__(self, scope):
        """
        :param  scope: the dir where the dup search began
        """
        jQTree.__init__(self)
        self.scope = "\\" + scope

    def process_dup_dirs(self, dup_dirs):
        """
        takes list of dirs from dup finder and splits them into parent and base
        to make an intermediary data structure
        :param
        :return: None, but loads dir_tree_list
        dir_tree_list:  dirname, parent, base
        """
        dir_tree_list = list()
        parent, base = self.scope.rsplit('\\', 1)
        dir_tree_list.append([self.scope, '#', base])
        for dirname in dup_dirs:
            if any(e[0] != dirname for e in dir_tree_list):
                parent, base = dirname.rsplit('\\', 1)
                dir_tree_list.append([dirname, parent, base])
        return dir_tree_list

    def make_tree(self, dup_dirs):
        """
        writes dup dirs into a jQuery - jsTree list[dict{}] structure, used for display to the user
        :param dup_dirs: a hierarchical dictionary of dup dirs
        :return: a jQuery tree: a list of dictionaries
        """
        tree_list = list()
        streamer_dict = dict()
        for row in self.process_dup_dirs(dup_dirs):
            dirname, parent, base = row
            node_dict = {
                'id': dirname,
                'parent': parent,
                'text': base,
                'state': {
                    'opened': True,
                    'selected': False
                }
            }
            tree_list.append(node_dict)
            if parent not in streamer_dict:
                streamer_dict[parent] = []
            streamer_dict[parent].append(node_dict)
        self.tree_list = tree_list
        self.tree_dict = streamer_dict

    def get_tree_list(self):
        return self.tree_list

    def get_tree_dict(self):
        return self.tree_dict

    def get_tree_branch_dict(self, dir_id):
        x = self.tree_dict[dir_id]
        print "get_tree_branch_dict[", dir_id, "]:\n", pp.pprint(x)
        return x

    def get_tree_branches(self, dir_ids):
        bouquet = {}
        for dir_id in dir_ids:
            bouquet.update(self.tree_dict[dir_id])
        return bouquet


def reset_web_prefix(url):
    """
    add web prefix 'static' to path for image display by server
    C:\Users\Michele\PycharmProjects\DupFinder\static\media\pics
    """
    url = "\\static\\media\\pics" + url
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
    # print "img_urls:\n", pp.pprint(img_urls)
    img_list = list()
    parent_id = 0
    img_list.append([parent_id, '#', parent_id, True])  # empty root level rec
    for hash_id, result_list in img_urls.iteritems():
        img_list.append([hash_id, parent_id, get_pic_url(result_list[0]), True])  # hash level rec with pic
        entry_id = 0
        for url in result_list:
            clickable = '<a href="%s">"%s"</a>' % (reset_web_prefix(url), url)
            img_list.append([url, hash_id, clickable, False])  # dup img level rec, text only
            entry_id += 1
    return img_list  # id, parent_id, display_item, state


class ImgTreeUI(jQTree):
    def __init__(self):
        jQTree.__init__(self)

    def make(self, img_urls):
        """
        writes dup imgs into a jQuery - jsTree list[dict{}] structure, used for display to the user
        :param img_urls: a list of lists of dup imgs, grouped by hashes
        :return: a jQuery tree: a list of dictionaries
        """
        img_list = list()
        for row in process_img_urls(img_urls=img_urls):
            # osLeafPath, osLeafPath of parent, text/display item, state dict entry
            url, parent_url, display_item, state = row
            row = {
                'id': url,
                'parent': parent_url,
                'text': display_item,
                'icon': False
            }
            if state:
                row['state'] = {
                    'opened': True,
                    'selected': False
                }
            img_list.append(row)
        if len(img_list) == 1:  # only contains header, reset to null
            img_list = list()
        self.tree_list = img_list
        # print "img_list:\n", pp.pprint(img_list)


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
