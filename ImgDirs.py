import os
import pprint


class ImgDirs(object):
    def __init__(self):
        self.pp = pprint.PrettyPrinter(indent=4)
        self._search_root = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) +
                                             r"\\static\\media\\pics")
        self._dir_id_keys = {}
        self._search_dirs = []
        self._all_img_dirs = self._load_all_img_dirs()

    def get_all_img_dirs(self):
        """return the list of all image directories"""
        return self._all_img_dirs

    def get_img_dirs_to_search(self):
        """return the list of directories selected by the user"""
        return self._search_dirs

    def set_img_dirs_to_search(self, indexes):
        self._search_dirs = []
        """create the list of directories selected by the user from the indexes returned from the ui"""
        for index in indexes:
            index = index.encode('ascii')
            self._search_dirs.append(self._get_dir_path(index))

    def _get_dir_path(self, key):
        """use the provided key to lookup and return the dir path"""
        key = int(key)
        x = None
        if key in self._dir_id_keys.keys():
            x = self._dir_id_keys[key]
        return x

    def _load_all_img_dirs(self):
        """writes all image dirs into a jQuery - jsTree list[dict{}] structure, used for display to the user"""
        dir_path_keys = {}
        dir_list = []
        row_cnt = 0
        self._dir_id_keys[row_cnt] = '#'
        dir_path_keys['#'] = row_cnt
        self._dir_id_keys[row_cnt] = self._search_root
        dir_path_keys[self._search_root] = row_cnt
        row_dict = {
            'id': row_cnt,
            'parent': '#',
            'text': self._search_root,
            'state': {
                'opened': True,
                'selected': False
            }
            }
        dir_list.append(row_dict)
        for _root, _dirs, files in os.walk(self._search_root):
            for dir in _dirs:
                row_cnt += 1
                self._dir_id_keys[row_cnt] = _root + "\\" + dir
                dir_path_keys[_root + "\\" + dir] = row_cnt
                row_dict = {
                    'id': row_cnt,
                    'parent': dir_path_keys[_root],
                    'text': dir
                }
                dir_list.append(row_dict)
        return dir_list

    def _print_results(self, dirs):
        self.pp.pprint(dirs)
        print len(dirs), " Photo Directories Found"

if __name__ == '__main__':
    dw = ImgDirs()
    idirs = dw.get_all_img_dirs()
    dw.pp.pprint(idirs)
    # import json
    #
    # dw.pp.pprint(json.dumps(idirs))



    # print "\nDirWalker type: ", type(dw.dirTree)
    # dw.pp.pprint(dw.dirTree)

    # Indexes = [u'["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21"]']
    # # dw.setIndex(Indexes)
    # # print dw.search_root
    # # dw.printResults(dw.dirTree)
    # dirs = dw.setSearchDirs(Indexes)
    # dw.printResults(dirs)