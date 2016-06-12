import hashlib
import ntpath
import os
import os.path
import pprint


def hashfile(path):
    hasher = hashlib.md5()
    f = open(path)
    while True:
        buf = f.read(128)
        if buf == '':
            break
        hasher.update(buf)
    f.close()
    return hasher.hexdigest()


def normalize_pathname(path):
    path = path.replace("C:\\Users\\Michele\\Pictures\\", "")
    path = path.replace("C:\\Users\\Michele\\PycharmProjects\\DupFinder\\static\\media\\pics\\", "")
    return path


class DupFinder(object):
    def __init__(self, dir_to_dup_srch):
        self.pp = pprint.PrettyPrinter(indent=4)
        self.dups = {}
        self._dup_imgs = {}
        self.results = []
        self.num_files_moved = 0
        self.dir_has_dups = {}
        self.find_dup(dir_to_dup_srch)
        self.num_dirs_reviewed = 0
        self.num_img_dups = 0

    # def searchDirs(self, dir_list):
    #     self.dups = {}
    #     for dir in dir_list:  # Iterate the folders given
    #         if os.path.exists(dir):
    #             self.findDup(dir)

    # def num_files(self, dir_name):
    #     num_files = None
    #     if dir_name:
    #         # num_files = len([name for name in os.listdir('.') if os.path.isfile(dir_name)])
    #         num_files = sum(os.path.isfile(os.path.join(dir_name, f)) for f in os.listdir(dir_name))
    #     return num_files

    def move_to_final_resting_place(self, files_to_move, dest_dir, local_root):
        # noinspection PyAugmentAssignment
        self.num_files_moved = len(files_to_move)
        for old_filepath in files_to_move:
            old_filepath = "{}/static/media/pics{}".format(local_root, old_filepath.replace('\\', '/'))
            new_filepath = local_root + dest_dir + "/" + ntpath.basename(old_filepath)
            try:
                os.rename(old_filepath, new_filepath)
            except WindowsError:
                base, ext = os.path.splitext(new_filepath)
                os.rename(new_filepath, base + '_' + ext)
                os.rename(old_filepath, new_filepath)

    def dirs_with_dups(self):
        x = self.dir_has_dups.keys()
        print "Dirs with Dups: ", self.pp.pprint(x)
        return x

    def find_dup(self, parent_folder):
        """
        :param parent_folder: directory to search for dups
        :return: None, loads two data structures:
            self.dups: format {hash:[list of file pathnames]}
            self.dir_has_dups: format {dirname:[list of hashes]}
        """
        img_types = ['.jpg', '.jpe', '.jpeg']
        for dname, subdirs, fileList in os.walk(parent_folder):
            for filename in fileList:
                fname, fext = os.path.splitext(filename)
                if fext in img_types:
                    path = os.path.join(dname, filename)
                    file_hash = hashfile(path)
                    path = normalize_pathname(path)
                    dir_name = normalize_pathname(dname)
                    if file_hash in self.dups:  # file is a dup
                        if path not in self.dups[file_hash]:  # add path to hash list
                            self.dups[file_hash].append(path)
                        if dir_name in self.dir_has_dups:
                            if file_hash not in self.dir_has_dups[dir_name]:
                                self.dir_has_dups[dir_name].append(file_hash)
                        else:
                            self.dir_has_dups[dir_name] = [file_hash]
                    else:  # first appearance of hash
                        self.dups[file_hash] = [path]
        print "Finished finding all dups."

    def load_results_by_dirs(self, dir_list):
        """
        Iterates over the list of dirs selected in the ui to produce
        a list of lists of duplicate images found in those dirs
        :param dir_list: list of dirs user wants to review for dup images
        :return:
        """
        img_urls = list()
        self.num_dirs_reviewed = len(dir_list)
        for dName in dir_list:  # Iterate the folders given
            if dName in self.dir_has_dups.keys():
                for file_hash in self.dir_has_dups[dName]:
                    img_urls.append(self.dups[file_hash])
        print "Results: ", self.pp.pprint(img_urls)
        self.num_img_dups = len(img_urls)
        return img_urls

    # def getResults(self):
    #     """converts a dictionary into a list of urls"""
    #     self.results = list(filter(lambda x: len(x) > 1, self.dups.values()))
    #     return self.results

    def getTreeResults(self):
        """processes the results list of urls into a jquery/jstree tree for display to the user"""
        results = self.res
        treeResults = []
        row_cnt = 0
        parent_id = row_cnt
        """ manages the root level"""
        treeResults.append({
            'id': parent_id,
            'parent': '#',
            'icon': False,
            'state': {
                'opened': True,
                'checkbox_disabled': True,
                'disabled': True
            }
        })
        if len(results) > 0:
            for result in results:
                pic_url = self.reset_web_prefix(result[0])
                # print "pic_url: ", pic_url
                fancyPic = \
                    '<img src="' + pic_url + '" class="img-circle" width="50" height="50">'
                row_cnt += 1
                """ handles the hash group level"""
                treeResults.append({
                    'id': row_cnt,
                    'parent': 0,
                    'icon': False,
                    'text': fancyPic,
                    'state': {
                        'opened': True,
                        'checkbox_disabled': True,
                        'disabled': True
                    }
                })
                parent_id = row_cnt
                for url in result:
                    row_cnt += 1
                    url = self.reset_web_prefix(url)
                    urlRef = '<a href="' + url + '">' + url + '</a>'
                    urlRef = urlRef.replace('/static/media/pics', '')
                    """handles the individual urls for each image"""
                    treeResults.append({
                        'id': row_cnt,
                        'parent': parent_id,
                        'icon': False,
                        'text': urlRef
                    })
                    self._dup_imgs[row_cnt] = url
        if len(treeResults) == 1:  # only contains header, reset to null
            treeResults = []
        return treeResults

    # def fixPath(self, url):
    #     """convert path from windows to web"""
    #     url = url.replace('\\', '/')
    #     pos = url.find("/static")
    #     return url[pos:]

    def move_images(self, indexes, dest_dir, local_root):
        """using the indexes from the ui, grab filepaths and move to destDir"""
        self.num_files_moved = len(indexes)
        imgs_to_move = []
        for index in indexes:
            index = index.encode('ascii')
            imgs_to_move.append(self._get_dir_path(index))
        move_to_final_resting_place(imgs_to_move, dest_dir, local_root)

        # def _get_dir_path(self, key):
        #     """use the provided key to lookup and return the url"""
        #     key = int(key)
        #     x = None
        #     if key in self._dup_imgs.keys():
        #         x = self._dup_imgs[key]
        #     return x

        # def set_img_dirs_to_display(self, indexes):
        #     """create the list of directories selected by the user from the indexes returned from the ui"""
        #     self._search_dirs = indexes

        # def get_img_dirs_to_search(self):
        #     """return the list of directories selected by the user"""
        #     return self._search_dirs

        # def _get_dir_path(self, key):
        #     """use the provided key to lookup and return the dir path"""
        #     key = int(key)
        #     x = None
        #     if key in self.get_dirs_with_dups():
        #         x = self._dir_id_keys[key]
        #     return x

        # def append_path(self, root, paths):
        #     if paths:
        #         before, sep, after = paths.partition("\\")
        #         if 'children' not in root:
        #             child = root.setdefault('children', [])
        #             child.setdefault('text', before)
        #             child.setdefault('state', {
        #                 'opened': True,
        #                 'selected': False
        #             })
        #         else:
        #             root['children'].append(
        #                 {
        #                     'text': before,
        #                     'state': {
        #                         'opened': True,
        #                         'selected': False
        #                     },
        #                     'children': []
        #                 }
        #             )
        #         self.append_path(root, after)
        #
        # def get_path(self, root, paths):
        #     if paths:
        #         before, sep, after = paths.partition("\\")
        #         child = root.setdefault(before, {})
        #         self.get_path(child, after)

        # def get_dir_list_to_display(self):
        #     """
        #     takes in a flat list of dirs and returns a hierarchical dict
        #     :return: hDict: hierarchical dict of dirs
        #     """
        #     self.hDict = {}
        #     for p in self.dirs_with_dups():
        #         self.get_path(self.hDict, p)
        #     return [self.hDict]


if __name__ == '__main__':
    search_scope = r"\_from Otto\_before pictures\1990's"
    df = DupFinder(r"C:\Users\Michele\Pictures" + search_scope)
    #
    # dups = df.dups
    # print "Dups type/len : ", type(dups), "/", len(dups)
    # print "Dups: ", df.pp.pprint(dups)
    #
    # dhd = df.dir_has_dups
    # print "Dir has Dups type/len : ", type(dhd), "/", len(dhd)
    # print "Dir has Dups: ", df.pp.pprint(dhd)
    #
    # df.load_results_by_dirs([r"C:\Users\Michele\Pictures\_from Otto\_before pictures\1990's\1993"])
    # res2 = df.res
    # print "Res 2 results type/len : ", type(res2), "/", len(res2)
    # print "Res results: ", df.pp.pprint(res2)
    #
    # res1 = df.getResults()
    # print "Res 1 results type/len : ", type(res1), "/", len(res1)
    # print "Res 1 results: ", df.pp.pprint(res1)
    #
    # diff = [a for a in res1 + res2 if (a not in res1) or (a not in res2)]
    # print "diff type/len : ", type(diff), "/", len(diff)
    # print "diff b/t ", df.pp.pprint(diff)
    # # print "get tree results: ", df.pp.pprint(df.getTreeResults())

    dwd = df.dirs_with_dups()
    print "Dirs with Dups type/len : ", type(dwd), "/", len(dwd)
    print "Dirs with Dups: ", df.pp.pprint(dwd)

    # hdir = df.get_dir_list_to_display()
    # print "Hierarchy Dirs with Dups type/len : ", type(hdir), "/", len(hdir)
    # print "HierarchyDirs with Dups: ", df.pp.pprint(hdir)
