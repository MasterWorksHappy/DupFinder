import hashlib
import ntpath
import os
import os.path
import pprint
from collections import OrderedDict

pp = pprint.PrettyPrinter(indent=4)


class DataMinder(object):
    """
    Provides:
        create_entry(file_hash=file_hash, dir_name=dir_name, file_path=path)
        flash_entries()
        get_dirs_with_dups()
        get_files_bydir(dir_list=dir_list)
        del_by_list_of_files(files_to_move)
    """

    def __init__(self):
        self.by_hash_dir_file = {}

    def gen_spt_data(self):
        """
        Only called once by DupFinder.DataMinder#flash_entries
        to compile statistics and persistent data structures
        """
        self.by_dir_file = {}
        self.by_file_hash = {}
        self.by_hash_files = {}
        for file_hash, v in self.by_hash_dir_file.iteritems():
            for dir_name, file_path_list in v.iteritems():
                for file_path in file_path_list:
                    self.new_dir_file(dir_name=dir_name, file_path=file_path)
                    self.new_hash_file(file_hash=file_hash, file_path=file_path)
                    self.new_file_hash(file_hash=file_hash, file_path=file_path)
        self.num_uniq_files = len(self.by_hash_dir_file)
        self.num_dirs_reviewed = len(self.by_dir_file)

    def new_dir_file(self, dir_name=None, file_path=None):
        """
        Only called once by DupFinder.DataMinder#gen_spt_data
        Creates self.by_dir_file - a dict of all filepaths in a directory
        """
        if dir_name not in self.by_dir_file.keys():
            self.by_dir_file[dir_name] = []
        try:
            self.by_dir_file[dir_name].append(file_path)
        except KeyError:
            print "****DupFinder.DataMinder#new_dir_file"
            pass

    def new_hash_file(self, file_hash=None, file_path=None):
        """
        Only called once by DupFinder.DataMinder#gen_spt_data
        Creates self.by_hash_files - a dict of all filepaths by hash
        """
        if file_hash not in self.by_hash_files.keys():
            self.by_hash_files[file_hash] = []
        try:
            self.by_hash_files[file_hash].append(file_path)
        except KeyError:
            print "**** DupFinder.DataMinder#new_hash_file"
            pass

    def new_file_hash(self, file_hash=None, file_path=None):
        """
        Only called once by DupFinder.DataMinder#gen_spt_data
        Creates self.by_file_hash - a dict of hashes by file_path
        """
        if file_path not in self.by_file_hash.keys():
            self.by_file_hash[file_path] = []
        try:
            self.by_file_hash[file_path].append(file_hash)
        except KeyError:
            print "**** DupFinder.DataMinder#new_file_hash"
            pass

    def create_entry(self, file_hash=None, dir_name=None, file_path=None):
        if file_hash not in self.by_hash_dir_file.keys():
            self.by_hash_dir_file[file_hash] = {}
        if dir_name not in self.by_hash_dir_file[file_hash]:
            self.by_hash_dir_file[file_hash][dir_name] = []
        try:
            self.by_hash_dir_file[file_hash][dir_name].append(file_path)
        except KeyError:
            print "****"
            pass

    def flash_entries(self):
        """
        {hash: {dir: [files]}}
        the following is necessary to strip out hashes that only contain one result
        within a dir, there should be > 1 files
        if a hash has > 1 dir then that too is a keeper
        DupFinder.DataMinder#gen_spt_data is called to compile all statistics
        """
        tmp_dict = {out_k: {in_k: in_v for in_k, in_v in out_v.items()
                            if (len(out_v) == 1 and len(in_v) > 1) or len(out_v) > 1}
                    for out_k, out_v in self.by_hash_dir_file.items()}
        """
        this next step removes all the empty entries ... this is the only way I can think to do it
        """
        self.by_hash_dir_file = {k: v for k, v in tmp_dict.iteritems() if len(v) > 0}
        self.gen_spt_data()
        # print "by_hash_dir_file:\n", pp.pprint(self.by_hash_dir_file)

    def get_files_byhash(self, dir_list=None):
        files_byhash = {}
        tmp_dict = {}
        for dir_name in dir_list:
            dir_name = str(dir_name)
            tmp_dict = {k: v for k, v in self.by_hash_files.iteritems() if any(dir_name in s for s in v)}
            files_byhash.update(tmp_dict)
        OrderedDict(sorted(files_byhash.items(), key=lambda t: len(t[1])))
        return files_byhash

    def del_by_list_of_files(self, files_to_move=None):
        for file_path in files_to_move:
            file_hash = self.by_file_hash[file_path]
            for dir_name, file_list in self.by_hash_dir_file[file_hash].items():
                if file_path in file_list:
                    self.by_hash_dir_file[file_hash][dir_name].remove(file_path)
        self.flash_entries()

    def get_dirs_with_dups(self):
        dup_dirs = self.by_dir_file.keys()
        dup_dirs.sort()
        return dup_dirs

    
class DupFinder(object):
    def __init__(self, acfg):
        search_dir = acfg['SEARCH_SCOPE']
        print "Dup checking %s" % search_dir
        self.dm = DataMinder()
        self.dest_dir = acfg['FINAL_RESTING_PLACE']
        self.appl_root = acfg['APPL_ROOT']
        self.pics_root = acfg['PICS_ROOT']
        self.appl_pics_root = acfg['APPL_PICS_ROOT']
        self.num_files_moved = 0
        self.find_dup(search_dir)
        self.num_dirs_reviewed = 0
        self.num_img_dups = 0
        self.num_files_confirmed = None

    def get_dirs_with_dups(self):
        """
        Called by the jQueryUI.DirTree.makeTree routine
        :return: List of all directories containing duplicates
        """
        return self.dm.get_dirs_with_dups()

    def find_dup(self, parent_folder):
        """
        searches for duplicate img files from the parent down
        :param parent_folder: directory to search for dups
        :return: None, loads two data structures:
            self.dups: format {hash:[list of file pathnames]}
            self.dir_has_dups: format {dirname:[list of hashes]}
        """
        img_types = ['.jpg', '.jpe', '.jpeg']
        for dname, subdirs, fileList in os.walk(parent_folder):
            if dname is not self.dest_dir:  # filter out dest dir
                for filename in fileList:
                    fname, fext = os.path.splitext(filename)
                    if fext in img_types:
                        path = os.path.join(dname, filename)
                        file_hash = hashlib.md5(open(path, 'rb').read()).hexdigest()
                        path = self.normalize_pics_root(path)
                        dir_name = self.normalize_pics_root(dname)
                        self.dm.create_entry(file_hash=file_hash, dir_name=dir_name, file_path=path)
        self.dm.flash_entries()

    def normalize_pics_root(self, path):
        path = path.replace(self.pics_root + '\\', "")
        path = path.replace(self.appl_pics_root + '\\', "")
        return path

    def confirmer(self):
        results = []
        self.num_files_confirmed = 0
        for dname, subdirs, fileList in os.walk(self.appl_root + self.dest_dir):
            for filename in fileList:
                self.num_files_confirmed += 1
                path = os.path.join(dname, filename)
                file_hash = hashlib.md5(open(path, 'rb').read()).hexdigest()
                if file_hash not in self.dm.by_hash_files.keys():
                    path = path.replace(self.appl_root, '')
                    path = path.replace('\\', '/')
                    results.append([path, filename])
        return results

    def get_img_urls(self, dir_list):
        """
        a list of dirs are passed in
        retrieve all urls for the duplicate images listed for those dirs
        {out_k: {in_k: [in_v]}} ... out_v is the {in_k: [in_v]} section
        self.dedups[file_hash][dir_name] = [list of dup img urls]
        """
        self.num_dirs_reviewed = len(dir_list)
        img_urls = self.dm.get_files_byhash(dir_list=dir_list)
        self.num_img_dups = len(img_urls)
        return img_urls

    def move_to_final_resting_place(self, files_to_move):
        self.num_files_moved = len(files_to_move)
        for old_filepath in files_to_move:
            old_filepath = "{}/static/media/pics{}".format(self.appl_root,
                                                           old_filepath.replace(
                                                               '\\', '/'))
            new_filepath = self.appl_root + self.dest_dir + "/" + ntpath.basename(
                old_filepath)
            try:
                os.rename(old_filepath, new_filepath)
            except WindowsError:
                base, ext = os.path.splitext(new_filepath)
                print base + '_' + ext
                os.rename(new_filepath, base + '_' + ext)
                os.rename(old_filepath, new_filepath)
        self.dm.del_by_list_of_files(files_to_move)

if __name__ == '__main__':
    # search_scope = r"\_from Otto\_before pictures\1990's"
    # df = DupFinder(search_dir=r"C:\Users\Michele\Pictures" + search_scope,
    #                dest_dir='/static/media/pics/__delete these pictures, they are duplicates___',
    #                appl_root='C:/Users/Michele/PycharmProjects/DupFinder'
    #                )
    # df.get_dirs_with_dups()

    # for dname, subdirs, fileList in os.walk(r"C:\Users\Michele\Pictures"):
    #     print "hello"

    root = r"C:\Users\Michele\Pictures"
    for item in os.listdir(root):
        ritem = os.path.join(root, item)
        if os.path.isdir(ritem):
            print ritem

    # print "dedups ({}):\n".format(len(df.dedups))
    # pp.pprint(df.dedups)
    #
    # files_to_move = [ "_from Otto\\_before pictures\\1990's\\1995\\1995 0301 08.jpg",
    #                   "_from Otto\\_before pictures\\1990's\\1993\\19930115 - 11.jpg",
    #                   "_from Otto\\_before pictures\\1990's\\1993\\199304 - Becky & Gina - Copy.jpg"]
    # df.del_dedup_entry(files_to_move)

    # dups = df.dups
    # print "Dups type/len : ", type(dups), "/", len(dups)
    # print "Dups: ", df.pp.pprint(dups)
    #
    # dhd = df.dir_has_dups
    # print "Dir has Dups type/len : ", type(dhd), "/", len(dhd)
    # print "Dir has Dups: ", df.pp.pprint(dhd)
    #
    # dwd = df.dirs_with_dups()
    # print "Dirs with Dups type/len : ", type(dwd), "/", len(dwd)
    # print "Dirs with Dups: ", df.pp.pprint(dwd)
