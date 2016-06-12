import pprint

from flask import Flask, render_template, request, redirect, url_for

from DupFinder import DupFinder
from jQueryUtils import DirTreeUI, ImgTreeUI

"""
    Dup Runner Process Flow
    1) At server start, dup finder runs and creates the master list of dup pics and their dirs
    2) Users are offered a list of dirs to select for review
    3) User is presented their list of dirs and all file dups in common with that dir
    4) User selects the files they want moved to the dir for deletion
"""

FINAL_RESTING_PLACE = '/static/media/pics/__delete these pictures, they are duplicates___'
LOCAL_ROOT = 'C:/Users/Michele/PycharmProjects/DupFinder'
DEBUG = False
SECRET_KEY = 'mam'
SEARCH_SCOPE = r"_from Otto\_before pictures\1990's"
app = Flask(__name__)
app.config.from_object(__name__)
# imgDirs = ImgDirs(app.config['SEARCH_SCOPE'])
dup_finder = DupFinder(r'C:\Users\Michele\Pictures\\' + app.config['SEARCH_SCOPE'])
dir_tree = DirTreeUI(app.config['SEARCH_SCOPE'])
img_tree = ImgTreeUI()
pp = pprint.PrettyPrinter(indent=4)


@app.route("/")
def get_dirs():
    """Displays to the user image dirs containing dups for selection"""
    dup_dir_tree = dir_tree.get_dir_tree(dup_finder.dirs_with_dups())
    return render_template(
        'get_paths.html',
        page_title='Select Directories',
        jsonTreeData=dup_dir_tree)


@app.route("/get_paths", methods=['POST'])
def get_paths():
    """Parses the json data for the img dir indexes selected by the user"""
    if request.method == 'POST':
        img_tree.make(dup_finder.load_results_by_dirs(request.get_json()))
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
        # file_indexes_to_move = request.get_json()
        # print "request.get_json()\n\n:", pp.pprint(request.get_json())
        # dup_finder.move_images(file_indexes_to_move, app.config['FINAL_RESTING_PLACE'], app.config['LOCAL_ROOT'])
        dup_finder.move_to_final_resting_place(
            request.get_json(),
            app.config['FINAL_RESTING_PLACE'],
            app.config['LOCAL_ROOT']
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


@app.route("/x")
def about():
    print "about"
    return render_template(
        'about.html',
        page_title='About')


if __name__ == '__main__':
    # app.run()
    # # app.run(debug=False)
    # app.run(debug=True)
    # app.run(host="0.0.0.0", port="33")  # localhost:33
    app.run(debug=True, use_debugger=True, use_reloader=True)
