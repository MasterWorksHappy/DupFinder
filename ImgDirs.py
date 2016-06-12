# import os
# import pprint
#
#
# class ImgDirs(object):
#     def __init__(self, dir_ext=None):
#         self.pp = pprint.PrettyPrinter(indent=4)
#         self._search_root = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) +
#                                              r"\\static\\media\\pics" + dir_ext)
#         self._dir_id_keys = {}
#         self._search_dirs = []
#         # self._all_img_dirs = self._load_all_img_dirs()
#
#     def get_all_img_dirs(self):
#         """return the list of all image directories"""
#         return self._all_img_dirs
#
#     def get_img_dirs_to_search(self):
#         """return the list of directories selected by the user"""
#         return self._search_dirs
#
#     def set_img_dirs_to_search(self, indexes):
#         """create the list of directories selected by the user from the indexes returned from the ui"""
#         self._search_dirs = []
#         for index in indexes:
#             index = index.encode('ascii')
#             self._search_dirs.append(self._get_dir_path(index))
#
#     def _get_dir_path(self, key):
#         """use the provided key to lookup and return the dir path"""
#         key = int(key)
#         x = None
#         if key in self._dir_id_keys.keys():
#             x = self._dir_id_keys[key]
#         return x
#
#
#
