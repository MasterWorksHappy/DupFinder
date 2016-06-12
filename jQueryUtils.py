import pprint


class jQTree(object):
    def __init__(self):
        self.pp = pprint.PrettyPrinter(indent=4)
        self.tree_list = []

    def __str__(self):
        return "".format(self.pp.pprint(self.tree_list))


class DirTreeUI(jQTree):
    def __init__(self, scope):
        """

        :param  scope: the dir where the dup search began
                dup_dirs: list of dirs with dups
        """
        jQTree.__init__(self)
        self.scope = "\\" + scope

    def process_dup_dirs(self, dup_dirs):
        """
        takes list of dirs from dup finder and splits them into parent and base
        :param
        :return: None, but loads dir_tree_list: row_cnt, parent, base
        tree_list:  id, parent, base
        """
        dir_tree_list = list()
        dir_tree_list.append([self.scope, '#', self.scope])
        for dirname in dup_dirs:
            parent, base = dirname.rsplit('\\', 1)
            dir_tree_list.append([dirname, parent, base])
        return dir_tree_list

    def make_tree(self, dup_dirs):
        """
        writes dup dirs into a jQuery - jsTree list[dict{}] structure, used for display to the user
        :param dup_dirs: a hierarchical dictionary of dup dirs
        :return: a jQuery tree: a list of dictionaries
        """
        dir_list = list()
        for row in self.process_dup_dirs(dup_dirs):
            dirname, parent, base = row
            dir_list.append({
                'id': dirname,
                'parent': parent,
                'text': base,
                'state': {
                    'opened': True,
                    'selected': False
                }
            })
        return dir_list

    def get_dir_tree(self, dup_dirs):
        self.tree_list = self.make_tree(dup_dirs)
        return self.tree_list


def reset_web_prefix(url):
    """add web prefix 'static' to path for image display by server"""
    url = "\\static\\media\\pics" + url
    url = url.replace('\\', '/')
    return url


def get_pic_url(url):
    return '<img src="' + reset_web_prefix(url) + '" class="img-circle" width="75" height="75">'


class ImgTreeUI(jQTree):
    def __init__(self):
        jQTree.__init__(self)
        self._dup_imgs = {}

    def process_img_urls(self, img_urls):
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
        parent_id = 'root'
        img_list.append([parent_id, '#', parent_id, True])  # empty root level rec
        for result in sorted(img_urls):
            hash_id = "hash level " + result[0]
            img_list.append([
                hash_id,
                parent_id,
                get_pic_url(result[0]),
                True
            ])  # hash level rec with pic
            for url in result:
                img_list.append([
                    url,
                    hash_id,
                    url.replace('\\', '/'),
                    False
                ])  # dup img level rec, text only
        return img_list

    def make(self, img_urls):
        """
        writes dup imgs into a jQuery - jsTree list[dict{}] structure, used for display to the user
        :param img_urls: a list of lists of dup imgs, grouped by hashes
        :return: a jQuery tree: a list of dictionaries
        """
        img_list = list()
        for row in self.process_img_urls(img_urls):
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

        # def make(self, img_urls):
        #     """processes the results list of urls into a jquery/jstree tree for display to the user"""
        #     img_list = list()
        #     row_cnt = 0
        #     parent_id = row_cnt
        #     """ manages the root level"""
        #     img_list.append({
        #         'id': parent_id,
        #         'parent': '#',
        #         'icon': False,
        #         'state': {
        #             'opened': True,
        #             'checkbox_disabled': True,
        #             'disabled': True
        #         }
        #     })
        #     if len(img_urls) > 0:
        #         for result in sorted(img_urls):  # img_urls.sort():
        #             pic_url = reset_web_prefix(result[0])
        #             fancy_pic = '<img src="' + pic_url + '" class="img-circle" width="75" height="75">'
        #             row_cnt += 1
        #             """ handles the hash group level"""
        #             img_list.append({
        #                 'id': row_cnt,
        #                 'parent': 0,
        #                 'icon': False,
        #                 'text': fancy_pic,
        #                 'state': {
        #                     'opened': True,
        #                     'checkbox_disabled': True,
        #                     'disabled': True
        #                 }
        #             })
        #             parent_id = row_cnt
        #             for url in result:
        #                 row_cnt += 1
        #                 url = reset_web_prefix(url)
        #                 url_ref = '<a href="' + url + '">' + url + '</a>'
        #                 url_ref = url_ref.replace('/static/media/pics', '')
        #                 """handles the individual urls for each image"""
        #                 img_list.append({
        #                     'id': row_cnt,
        #                     'parent': parent_id,
        #                     'icon': False,
        #                     'text': url_ref
        #                 })
        #                 self._dup_imgs[row_cnt] = url
        #     if len(img_list) == 1:  # only contains header, reset to null
        #         img_list = list()
        #     self.tree_list = img_list


if __name__ == '__main__':
    # pp = pprint.PrettyPrinter(indent=4)
    dirs = list([
        "_from Otto\\_before pictures\\1990's\\1993",
        "_from Otto\\_before pictures\\1990's\\1992",
        "_from Otto\\_before pictures\\1990's\\1995",
        "_from Otto\\_before pictures\\1990's\\1994",
        "_from Otto\\_before pictures\\1990's\\1997",
        "_from Otto\\_before pictures\\1990's\\1996",
        "_from Otto\\_before pictures\\1990's\\1998"
    ])
    # print "dir_list: ", pp.pprint(dir_list)
    # print "dir_list sorted: ", pp.pprint(dir_list.sort())

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
