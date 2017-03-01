import ConfigParser
import logging
import pprint
import urllib
import datetime

from flask import Flask, Blueprint, render_template, \
    request, redirect, url_for, jsonify

from DupFinder import DupFinder
from jQueryUtils import DirTreeUI, ImgTreeUI

"""
    dupRunner.py
    
    SETUP
    1) Create a symbolic link in the ..\static\media directory:
       mklink /D pics "C:\Users\Maste\_My Stuff\Pictures"

    Dup Runner Process Flow
    1) At server start, dup finder runs and creates the master list of dup pics and their dirs
    2) Users are offered a list of dirs to select for review
    3) User is presented their list of dirs and all file dups in common with that dir
    4) User selects the files they want moved to the dir for deletion

    NOTES
    GET - Client requests data from the server
    POST - Client submits data to be processed by the server

    JS
    alert("treeData: ", treeData)

    http://stackoverflow.com/questions/20810630/how-to-use-flask-jinja2-url-for-with-multiple-parameters
    https://github.com/vakata/jstree/issues/1056
    http://stackoverflow.com/questions/24131181/lazy-loading-with-jstree
    https://www.javascripting.com/view/jstree#populating-the-tree-using-ajax-and-lazy-loading-nodes
"""


logger = logging.getLogger('dupDestroyer')

dupRunner = Blueprint('dupRunner', __name__,
                      template_folder='templates', static_folder='static')

pp = pprint.PrettyPrinter(indent=4)
cfg = ConfigParser.ConfigParser()
cfg.read('DupDestroyer.ini')

FINAL_RESTING_PLACE = cfg.get('Pics', 'trash')
SEARCH_SCOPE = cfg.get('Pics', 'scope')
PICS_ROOT = cfg.get('Pics', 'proot')
APPL_ROOT = cfg.get('Appl', 'aroot')
APPL_PICS_ROOT = cfg.get('Appl', 'aproot')
WEB_PICS_ROOT = cfg.get('Appl', 'wproot')
app = Flask(__name__)
app.config.from_object(__name__)


def log_msg(**kwargs):
    msg = "\n\t\t"
    for k, v in kwargs.iteritems():
        if isinstance(v, dict) or isinstance(v, list):
            v = "\n" + pp.pformat(v)
        msg += '%s: %s, ' % (k, v)
    return msg

print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
logger.debug(log_msg(
    search_scope=SEARCH_SCOPE,
    msg='Dir being checked for dups'))
dup_finder = DupFinder(app.config)
dir_tree = DirTreeUI(app.config, dup_finder.get_dirs_with_dups())
img_tree = ImgTreeUI()
dir_tree.make_tree(dup_finder.get_dirs_with_dups())
# dir_tree.make_tree(dup_finder.dm.get_dirs_with_dups())
print "Duplicate search complete ..."
print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))

@dupRunner.route("/")
def get_dirs():
    """
        Displays to the user image dirs containing dups for selection
    """
    logger.debug(log_msg(
        method=request.method))
    return render_template(
        'dupRunner/get_paths.html',
        num_hashes_found=dup_finder.dm.num_uniq_files,
        num_dirs_reviewed=dup_finder.dm.num_dirs_reviewed,
        page_title='Select Directories'
    )


# @dupRunner.route('/an')
# # def get_dirs():
# def index():
#     return render_template('dupRunner/index.html')


# @dupRunner.route('/_add_numbers')
# def add_numbers():
#     a = request.args.get('a', 0, type=int)
#     b = request.args.get('b', 0, type=int)
#     return jsonify(result=a + b)


@dupRunner.route('/get_dir')
def get_dir():
    rq_id = request.args.get('id', '', type=str)
    branch = dir_tree.get_tree_branch_dict(rq_id)
    logger.debug(log_msg(
        method=request.method,
        route=request.path,
        rq_id=rq_id,
        branch=branch
    ))
    return jsonify(branch)


# @dupRunner.route('/get_a_dir', defaults={'id': ''}, methods=['GET', 'POST'])
# @dupRunner.route('/get_a_dir/<path:id>', methods=['POST'])
# # @dupRunner.route('/get_a_dir', methods=['POST'])
# def get_a_dir(id=None):
#     """
#         Displays to the user an image dir containing dups for selection
#     """
#     # rq_id = request.args.get('id', '#', type=str)
#     rq_id = request.args.get('id', type=str)
#     if id:
#         parent_id = str(urllib.unquote(id))
#     elif rq_id:
#         parent_id = str(urllib.unquote(rq_id))
#     else:
#         parent_id = '#'
#     if parent_id == "'\\''":
#         parent_id = '#'
#     logger.debug(log_msg(
#         method=request.method,
#         route=request.path,
#         rq_id=rq_id,
#         id=id,
#         parent_id=parent_id))
#     if request.method == 'POST':
#         if parent_id is '#':
#             return jsonify(dir_tree.get_tree_branch_dict('#'))
#         else:
#             return redirect(url_for('dupRunner.get_a_dir'))
#     else:  # it is a GET
#         return jsonify(dir_tree.get_tree_branch_dict(parent_id))
#         # return render_template(
#         #     'dupRunner/get_paths.html',
#         #     num_hashes_found=dup_finder.dm.num_uniq_files,
#         #     num_dirs_reviewed=dup_finder.dm.num_dirs_reviewed,
#         #     page_title='Select Directories',
#         #     jsonTreeData=dir_tree.get_tree_branch_dict(parent_id)
#         # )


# @dupRunner.route("/get_more_dirs/<id>", methods=['GET', 'POST'])
# def get_more_dirs(id):
#     """
#         Displays to the user image dirs containing dups for selection
#     """
#     print "***** dupRunner.get_more_dirs"
#     return render_template(
#         'dupRunner.get_paths.html',
#         num_hashes_found=dup_finder.dm.num_uniq_files,
#         num_dirs_reviewed=dup_finder.dm.num_dirs_reviewed,
#         page_title='Select Directories',
#         jsonTreeData=dir_tree.get_tree_branches(id))


@dupRunner.route("/get_paths", methods=['POST'])
def get_paths():
    """
        Called when the user presses the submit button on the dir select screen
        Parses the json data for the img dir indexes selected by the user
    """
    img_dirs = request.get_json()
    logger.debug(log_msg(
        method=request.method,
        img_dirs=img_dirs))
    if request.method == 'POST':
        img_tree.make(dup_finder.get_img_urls(img_dirs))
        return redirect(url_for('dupRunner.show_me_the_money'))


@dupRunner.route("/show_me_the_money")
def show_me_the_money():
    """
        Executes the duplicate finder on the list of img dirs
        selected by the user.  Displays the dups to the user.
    """
    logger.debug(log_msg(
        method=request.method,
        img_tree_tree_dict=img_tree.tree_dict
    ))
    return render_template(
        'dupRunner/getDupsToDelete.html',
        page_title='Results',
        num_dirs_searched=dup_finder.num_dirs_reviewed,
        num_dups_found=dup_finder.num_img_dups)


@dupRunner.route('/get_pic')
def get_pic():
    pic_id = request.args.get('id', '', type=str)
    branch = img_tree.get_tree_branch_dict(pic_id)
    logger.debug(log_msg(
        method=request.method,
        route=request.path,
        rq_id=pic_id,
        branch=branch
    ))
    return jsonify(branch)


# @dupRunner.route("/show_me_the_money")
# def show_me_the_money():
#     """
#         Executes the duplicate finder on the list of img dirs
#         selected by the user.  Displays the dups to the user.
#     """
#     logger.debug(log_msg(
#         method=request.method,
#         img_tree_tree_list=img_tree.tree_list))
#     if len(img_tree.tree_list) == 0:  # no dups found
#         return render_template(
#             'dupRunner/Good Job.html',
#             page_title='Good Job!')
#     else:  # img_tree.tree_results ready to be displayed
#         return render_template(
#             'dupRunner/getDupsToDelete.html',
#             page_title='Results',
#             num_dirs_searched=dup_finder.num_dirs_reviewed,
#             num_dups_found=dup_finder.num_img_dups,
#             jsonTreeData=img_tree.tree_list)


@dupRunner.route("/moveTheFiles", methods=['POST'])
def move_the_files():
    """
        Moves the list of dup files selected by the user
        to a directory for review and manual removal by the user.
        PARAM : a list of files to be moved
    """
    dup_files = request.get_json()
    logger.debug(log_msg(
        method=request.method,
        dup_files=dup_files))
    if request.method == 'POST':
        dup_finder.move_to_final_resting_place(dup_files)
        return redirect(url_for('dupRunner.success'))


@dupRunner.route("/success")
def success():
    """
    """
    logger.debug(log_msg(
        method=request.method))
    return render_template(
        'dupRunner/success.html',
        page_title='Success',
        num_moved=dup_finder.num_files_moved,
        dup_dir=app.config['FINAL_RESTING_PLACE'])


@dupRunner.route("/confirmer")
def confirmer():
    """
    """
    logger.debug(log_msg(
        method=request.method))
    return render_template(
        'dupRunner/confirmer.html',
        issues=dup_finder.confirmer(),
        num_reviewed=dup_finder.num_files_confirmed,
        page_title='Confirmer')


@dupRunner.route("/x")
def about():
    """
    """
    logger.debug(log_msg(
        method=request.method))
    return render_template(
        'dupRunner/about.html',
        page_title='About')


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port="33")  # localhost:33
    app.run(debug=True, use_debugger=True, use_reloader=True)
