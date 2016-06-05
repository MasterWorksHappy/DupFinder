import hashlib
import ntpath
import os
import os.path
import pprint


class DupFinder():
    def __init__(self, dir_to_dup_srch):
        self.dups = {}
        self._dup_imgs = {}
        self.results = []
        self.num_files_moved = 0
        self.pp = pprint.PrettyPrinter(indent=4)
        self.dir_has_dups = {}
        self.findDup(dir_to_dup_srch)

    def searchDirs(self, dir_list):
        self.dups = {}
        for dir in dir_list:  # Iterate the folders given
            if os.path.exists(dir):
                self.findDup(dir)

    def num_files(self, dir_name):
        num_files = None
        if dir_name:
            # num_files = len([name for name in os.listdir('.') if os.path.isfile(dir_name)])
            num_files = sum(os.path.isfile(os.path.join(dir_name, f)) for f in os.listdir(dir_name))
        return num_files

    def findDup(self, parentFolder):
        """
        :param parentFolder:
        :return:
        Dups format {hash:[names]}
        dir_has_dups format {dirname:[hashes]}
        """
        img_types = ['.jpg', '.jpe', '.jpeg']
        for dirName, subdirs, fileList in os.walk(parentFolder):
            for filename in fileList:
                fname, fext = os.path.splitext(filename)
                if fext in img_types:
                    path = os.path.join(dirName, filename)
                    file_hash = self.hashfile(path)
                    path = self.normalize_pathname(path)
                    dir = self.normalize_pathname(dirName)
                    if file_hash in self.dups:  # file is a dup
                        if not path in self.dups[file_hash]:  # add path to hash list
                            self.dups[file_hash].append(path)
                        if dir in self.dir_has_dups:
                            if not file_hash in self.dir_has_dups[dir]:
                                self.dir_has_dups[dir].append(file_hash)
                        else:
                            self.dir_has_dups[dir] = [file_hash]
                    else:  # first appearance of hash
                        self.dups[file_hash] = [path]
        print "done"


    def hashfile(self, path):
        hasher = hashlib.md5()
        f = open(path)
        while True:
            buf = f.read(128)
            if buf == '':
                break
            hasher.update(buf)
        f.close()
        return hasher.hexdigest()

    def normalize_pathname(self, path):
        path = path.replace("C:\\Users\\Michele\\Pictures\\", "")
        path = path.replace("C:\\Users\\Michele\\PycharmProjects\\DupFinder\\static\\media\\pics\\", "")
        return path

    def load_results_by_dirs(self, dir_list):
        self.res = []
        for dir in dir_list:  # Iterate the folders given
            subdirs = [x[0] for x in os.walk(dir)]
            for subdir in subdirs:
                subdir = self.normalize_pathname(subdir)
                if subdir in self.dir_has_dups.keys():
                    for hash in self.dir_has_dups[subdir]:
                        self.res.append(self.dups[hash])
        return self.res

    def getResults(self):
        """converts a dictionary into a list of urls"""
        self.results = list(filter(lambda x: len(x) > 1, self.dups.values()))
        return self.results

    def getTreeResults(self):
        """processes the results list of urls into a jquery/jstree tree for display to the user"""
        results = self.res
        # results = self.getResults()
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

    def reset_web_prefix(self, url):
        """add web prefix 'static' to path"""
        # print "\n\nOld url: ", url
        url = "\\static\\media\\pics\\" + url
        url = url.replace('\\', '/')
        # print "New url: ", url
        return url

    def fixPath(self, url):
        """convert path from windows to web"""
        url = url.replace('\\', '/')
        pos = url.find("/static")
        return url[pos:]

    def move_images(self, indexes, dest_dir, local_root):
        """using the indexes from the ui, grab filepaths and move to destDir"""
        self.num_files_moved = len(indexes)
        imgs_to_move = []
        for index in indexes:
            index = index.encode('ascii')
            imgs_to_move.append(self._get_dir_path(index))
        self.move_to_final_resting_place(imgs_to_move, dest_dir, local_root)

    def _get_dir_path(self, key):
        """use the provided key to lookup and return the url"""
        key = int(key)
        x = None
        if key in self._dup_imgs.keys():
            x = self._dup_imgs[key]
        return x

    def move_to_final_resting_place(self, files_to_move, dest_dir, local_root):
        for old_filepath in files_to_move:
            old_filepath = local_root + old_filepath
            new_filepath = local_root + dest_dir + "/" + ntpath.basename(old_filepath)
            try:
                os.rename(old_filepath, new_filepath)
            except WindowsError:
                base, ext = os.path.splitext(new_filepath)
                os.rename(new_filepath, base + '_' + ext)
                os.rename(old_filepath, new_filepath)

if __name__ == '__main__':
    df = DupFinder(r"C:\Users\Michele\Pictures\_from Otto\_before pictures\1990's")

    dups = df.dups
    print "Dups type/len : ", type(dups), "/", len(dups)
    print "Dups: ", df.pp.pprint(dups)

    dhd = df.dir_has_dups
    print "Dir has Dups type/len : ", type(dhd), "/", len(dhd)
    print "Dir has Dups: ", df.pp.pprint(dhd)

    df.load_results_by_dirs([r"C:\Users\Michele\Pictures\_from Otto\_before pictures\1990's\1993"])
    res2 = df.res
    print "Res 2 results type/len : ", type(res2), "/", len(res2)
    print "Res results: ", df.pp.pprint(res2)

    res1 = df.getResults()
    print "Res 1 results type/len : ", type(res1), "/", len(res1)
    print "Res 1 results: ", df.pp.pprint(res1)

    diff = [a for a in res1 + res2 if (a not in res1) or (a not in res2)]
    print "diff type/len : ", type(diff), "/", len(diff)
    print "diff b/t ", df.pp.pprint(diff)
    # print "get tree results: ", df.pp.pprint(df.getTreeResults())
