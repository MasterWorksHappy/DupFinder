import os
import pprint


class DirWalker(object):
    def __init__(self):
        self._search_root = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + r"\\static\\media\\pics")
        # self._search_root = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + r"\\static\\media")
        self._rowProperty = {}
        self._dir_PathKeys = {}
        self._dir_IdKeys = {}
        self._dirTree = []
        self._dirList = []
        self.load_dirs()
        self.dirIdxs = []

    @property
    def search_root(self):
        return self._search_root

    @search_root.setter
    def search_root(self, value):
        self._search_root = value

    @property
    def dirTree(self):
        return self._dirTree

    @dirTree.setter
    def dirTree(self, value):
        self._dirTree.append(value)

    @property
    def dirList(self):
        return self._dirList

    @dirList.setter
    def dirList(self, value):
        self._dirList.append(value)

    @property
    def dir_IdKeys(self):
        x = self._dir_IdKeys
        return x

    @dir_IdKeys.setter
    def dir_IdKeys(self, value):
        self._dir_IdKeys = value

    @property
    def dir_PathKeys(self):
        return self._dir_PathKeys

    @dir_PathKeys.setter
    def dir_PathKeys(self, value):
        self._dir_PathKeys = value

    def load_dirs(self):
        row_cnt = 0
        self.dir_IdKeys[row_cnt] = '#'
        self.dir_PathKeys['#'] = row_cnt
        self.dir_IdKeys[row_cnt] = self._search_root
        self.dir_PathKeys[self._search_root] = row_cnt
        self.rowProperty = {
            'id': row_cnt,
            'parent': '#',
            'text': self._search_root}
        # self.dirTree.append(self.rowProperty)
        self.dirTree = self.rowProperty
        del self.rowProperty
        for _root, _dirs, files in os.walk(self._search_root):
            for dir in _dirs:
                row_cnt += 1
                self.dir_IdKeys[row_cnt] = _root + "\\" + dir
                self.dir_PathKeys[_root + "\\" + dir] = row_cnt
                self.rowProperty = {
                    'id': row_cnt,
                    'parent': self.dir_PathKeys[_root],
                    'text': dir}
                # self.dirTree.append(self.rowProperty)
                self.dirTree = self.rowProperty
                del self.rowProperty

    def setIndex(self, indexes):
        dirIdx = indexes.pop()
        dirIdx1 = dirIdx.encode('ascii')
        # # dirIdx15 = dirIdx1.strip("\"\'[]")
        # for ch in ['\"', '\]', '\[']:
        #     if ch in dirIdx1:
        #         dirIdx15 = dirIdx1.replace(ch, '')
        # dirIdx15 = dirIdx15.strip('[]')
        # dirIdx2 = dirIdx15.split(',')
        # self.dirIdxs = dirIdx2
        self.dirIdxs = dirIdx1

    def setSearchDirs(self):
        for index in self.dirIdxs:  # Iterate the folders given
            self.dirList = self.getDirPath(index)

    def getDirPath(self, key):
        key = int(key)
        if key in self.dir_IdKeys.keys():
            x = self.dir_IdKeys[key]
            return x

    @property
    def rowProperty(self):
        return self._rowProperty

    @rowProperty.setter
    def rowProperty(self, values):
        self._rowProperty['id'] = values['id']
        self._rowProperty['parent'] = values['parent']
        self._rowProperty['text'] = values['text']

    @rowProperty.deleter
    def rowProperty(self):
        # del self._rowProperty
        self._rowProperty = {}
        return self._rowProperty

    def printResults(self, dirs):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(dirs)
        print len(dirs), " Photo Directories Found"


if __name__ == '__main__':
    dw = DirWalker()
    Indexes = [u'["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21"]']
    dw.setIndex(Indexes)
    print dw.search_root
    dw.printResults(dw.dirTree)
    dirs = dw.setSearchDirs([1, 2, 3])
    dw.printResults(dirs)
