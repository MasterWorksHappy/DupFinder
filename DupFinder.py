import hashlib
import os
import os.path
import pprint

class DupFinder():
    def __init__(self):
        self.data = []
        self.dups = {}
        self.pp = pprint.PrettyPrinter(indent=4)

    def searchDirs(self, dir_list):
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
        # Dups in format {hash:[names]}
        img_types = ['.jpg', '.jpe', '.jpeg']
        for dirName, subdirs, fileList in os.walk(parentFolder):
            for filename in fileList:
                fname, fext = os.path.splitext(filename)
                if fext in img_types:
                    path = os.path.join(dirName, filename)
                    file_hash = self.hashfile(path)
                    if file_hash in self.dups:
                        if not path in self.dups[file_hash]:
                            self.dups[file_hash].append(path)
                    else:
                        self.dups[file_hash] = [path]

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

    def getResults(self):
        results = list(filter(lambda x: len(x) > 1, self.dups.values()))
        return results

    def getTreeResults(self):
        results = self.getResults()
        treeResults = []
        row_cnt = 0
        parent_id = row_cnt
        treeResults.append({
            'id': parent_id,
            'parent': '#'})
        if len(results) > 0:
            for result in results:
                if row_cnt is not 0:
                    row_cnt += 1
                    treeResults.append({
                        'id': row_cnt,
                        'parent': parent_id})
                    parent_id = row_cnt
                for url in result:
                    row_cnt += 1
                    url = self.fixPath(url)
                    treeResults.append({
                        'id': row_cnt,
                        'parent': parent_id,
                        'text': url  # ,
                        # 'icon': url
                    })
        return treeResults

    def getURLResults(self):
        results = self.getResults()
        urls = []
        if len(results) > 0:
            for result in results:
                row = []
                for url in result:
                    row.append(self.fixPath(url))
                urls.append(row)
        return urls

    def fixPath(self, url):
        url = url.replace('\\', '/')
        pos = url.find("/static")
        return url[pos:]

    def printResults(self):
        results = self.getResults()
        if len(results) > 0:
            print('Duplicates Found:')
            print('The following files are identical. The name could differ, but the content is identical')
            print('___________________')
            for result in results:
                for subresult in result:
                    print('\t\t%s' % subresult)
                    print('___________________')
        else:
            print('No duplicate files found.')


if __name__ == '__main__':
    df = DupFinder()
    dirList = [
        'C:\Users\Michele\PycharmProjects\DupFinder\static\media\pics\Saved Pictures',
        'C:\Users\Michele\PycharmProjects\DupFinder\static\media\pics\_from Otto\2015'
        # 'C:\Users\Michele\PycharmProjects\DupFinder\static\media\pics\_from Otto\_before pictures'
    ]
    df.searchDirs(dirList)

    urls = df.getURLResults()
    print "\nURL Results Type: ", type(urls)
    df.pp.pprint(urls)

    results = df.getTreeResults()
    print "\nTree Results Type: ", type(results)
    df.pp.pprint(results)

    # df.printResults()
