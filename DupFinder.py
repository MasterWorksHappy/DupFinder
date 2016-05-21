import hashlib
import os
import os.path


class DupFinder():
    def __init__(self):
        self.data = []
        self.dups = {}

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

    def getURLResults(self):
        # new_url = None
        # varURLx = None
        # slash_pos = 0
        results = self.getResults()
        urls = []
        if len(results) > 0:
            for result in results:
                row = []
                main_pic = result[0]
                for url in result:
                    url = url.replace('\\', '/')
                    # if main_pic == url:
                    #     new_url = url
                    #     print("main_pic==url matches")
                    # else:  # trim prefix from url
                    #     urllen = len(url)
                    #     for x in range(0, urllen):
                    #         varURLx = url[x]
                    #         varMainPicx = main_pic[x]
                    #         if varURLx == '/':
                    #             slash_pos = x
                    #         if varMainPicx != varURLx:
                    #             new_url = url[slash_pos + 1:urllen]
                    #             break
                    pos = url.find("/static")
                    url = url[pos:]
                    # print("short url: ", new_url )
                    row.append(url)
                urls.append(row)
        return urls

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
        'C:\\Users\\Michele\\PycharmProjects\\DeDuper\\static\\media\\pics\\_from Otto\\2015\\2015 Passport Pics',
        'C:\\Users\\Michele\\PycharmProjects\\DeDuper\\static\\media\\pics\\_from Otto\\2015\\Butch',
        'C:\\Users\\Michele\\PycharmProjects\\DeDuper\\static\\media\\pics\\_from Otto\\2015\\CCI',
        "C:\\Users\\Michele\\PycharmProjects\\DeDuper\\static\\media\\pics\\_from Otto\\_all pictures\\1980's\\1983",
        "C:\\Users\\Michele\\PycharmProjects\\DeDuper\\static\\media\\pics\\_from Otto\\_before pictures\\1980's\\1983"
    ]
    df.searchDirs(dirList)
    urls = df.getURLResults()
    df.printResults()
