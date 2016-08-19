import pprint

from flask import Flask, render_template, request, redirect, url_for

import config
from DupFinder import DupFinder
from jQueryUtils import DirTreeUI, ImgTreeUI

"""
    SETUP
    1) Create a symbolic link in the ..\static\media directory:
       mklink /D pics "C:\Users\Maste\_My Stuff\Pictures"

    Dup Runner Process Flow
    1) At server start, dup finder runs and creates the master list of dup pics and their dirs
    2) Users are offered a list of dirs to select for review
    3) User is presented their list of dirs and all file dups in common with that dir
    4) User selects the files they want moved to the dir for deletion
"""

FINAL_RESTING_PLACE = config.pathnames['trash']
# FINAL_RESTING_PLACE = '/static/media/pics/__delete these pictures, they are duplicates___'
LOCAL_ROOT = '"C:\Users\Maste\_My Stuff\PycharmProjects\DupFinder"'
DEBUG = False
SECRET_KEY = 'mam'
# SEARCH_SCOPE = config.pathnames['test']
SEARCH_SCOPE = r"_from Otto\_before pictures\1990's"
app = Flask(__name__)
app.config.from_object(__name__)

dup_finder = DupFinder(search_dir=r"C:\Users\Maste\_My Stuff\Pictures\\" + app.config['SEARCH_SCOPE'],
                       dest_dir=app.config['FINAL_RESTING_PLACE'],
                       local_root=app.config['LOCAL_ROOT']
                       )
dir_tree = DirTreeUI(app.config['SEARCH_SCOPE'])
img_tree = ImgTreeUI()
pp = pprint.PrettyPrinter(indent=4)
dir_tree.make_tree(dup_finder.dm.get_dirs_with_dups())


@app.route("/")
def get_dirs():
    """Displays to the user image dirs containing dups for selection"""
    # dup_dir_tree = dir_tree.get_dir_tree(dup_finder.dm.get_dirs_with_dups())
    return render_template(
        'get_paths.html',
        num_hashes_found=dup_finder.dm.num_uniq_files,
        num_dirs_reviewed=dup_finder.dm.num_dirs_reviewed,
        jsonTreeData=dir_tree.get_tree_dict(),
        page_title='Select Directories')


@app.route("/get_a_dir", methods=['GET', 'POST'])
def get_a_dir():
    """Displays to the user an image dir containing dups for selection"""
    id = request.args.get('id')
    print "id: >", id, "<"
    if not id:
        id = '#'
    return render_template(
        'get_paths.html',
        num_hashes_found=dup_finder.dm.num_uniq_files,
        num_dirs_reviewed=dup_finder.dm.num_dirs_reviewed,
        page_title='Select Directories',
        jsonTreeData=dir_tree.get_tree_branch_dict(id))


@app.route("/get_more_dirs/<id>", methods=['GET', 'POST'])
def get_more_dirs(id):
    """Displays to the user image dirs containing dups for selection"""
    return render_template(
        'get_paths.html',
        num_hashes_found=dup_finder.dm.num_uniq_files,
        num_dirs_reviewed=dup_finder.dm.num_dirs_reviewed,
        page_title='Select Directories',
        jsonTreeData=dir_tree.get_tree_branches(id))


@app.route("/get_paths", methods=['POST'])
def get_paths():
    """Parses the json data for the img dir indexes selected by the user"""
    if request.method == 'POST':
        img_tree.make(dup_finder.get_img_urls(request.get_json()))
        return redirect(url_for('show_me_the_money'))


@app.route("/show_me_the_money")
def show_me_the_money():
    """Executes the duplicate finder on the list of img dirs selected by the user.  Displays the dups to the user."""
    print "show_me_the_money"
    if len(img_tree.tree_list) == 0:  # no dups found
        return render_template(
            'Good Job.html',
            page_title='Good Job!')
    else:  # img_tree.tree_results ready to be displayed
        return render_template(
            'getDupsToDelete.html',
            page_title='Results',
            num_dirs_searched=dup_finder.num_dirs_reviewed,
            num_dups_found=dup_finder.num_img_dups,
            jsonTreeData=img_tree.tree_list)


@app.route("/moveTheFiles", methods=['POST'])
def move_the_files():
    """Moves the dup files selected by the user to a directory for manual removal by the user."""
    print "move_the_files"
    if request.method == 'POST':
        dup_finder.move_to_final_resting_place(
            request.get_json()
        )
        return redirect(url_for('success'))


@app.route("/success")
def success():
    print "success"
    return render_template(
        'success.html',
        page_title='Success',
        num_moved=dup_finder.num_files_moved,
        dup_dir="C:/Users/Michele/Pictures/__delete these pictures, they are duplicates___")


@app.route("/confirmer")
def confirmer():
    print "confirmer"
    return render_template(
        'confirmer.html',
        issues=dup_finder.confirmer(),
        num_reviewed=dup_finder.num_files_confirmed,
        page_title='Confirmer')


@app.route("/x")
def about():
    print "about"
    return render_template(
        'about.html',
        page_title='About')


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port="33")  # localhost:33
    app.run(debug=True, use_debugger=True, use_reloader=True)
