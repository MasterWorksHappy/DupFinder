from flask import Flask, render_template, request, redirect, url_for

from DupFinder import DupFinder
from ImgDirs import ImgDirs

FINAL_RESTING_PLACE = '/static/media/pics/__delete these pictures, they are duplicates___'
LOCAL_ROOT = 'C:/Users/Michele/PycharmProjects/DupFinder'
DEBUG = False
SECRET_KEY = 'mam'

app = Flask(__name__)
app.config.from_object(__name__)
imgDirs = ImgDirs()
dupFinder = DupFinder()


@app.route("/")
def get_dirs():
    """Displays to the user all possible image directories for selection"""
    return render_template(
        'get_paths.html',
        page_title='Select Directories',
        jsonTreeData=imgDirs.get_all_img_dirs())


@app.route("/get_paths", methods=['POST'])
def get_paths():
    """Parses the json data for the img dir indexes selected by the user"""
    if request.method == 'POST':
        imgDirs.set_img_dirs_to_search(request.get_json())
        return redirect(url_for('show_me_the_money'))


@app.route("/show_me_the_money")
def show_me_the_money():
    """Executes the duplicate finder on the list of img dirs selected by the user.  Displays the dups to the user."""
    dupFinder.searchDirs(imgDirs.get_img_dirs_to_search())
    results = dupFinder.getTreeResults()
    if len(results) == 0:  # no dups found
        return render_template(
            'Good Job.html',
            page_title='Good Job!')
    else:  # results ready to be displayed
        return render_template(
            'getDupsToDelete.html',
            page_title='Results',
            num_dirs_searched=len(imgDirs.get_img_dirs_to_search()),
            num_dups_found=len(results),
            jsonTreeData=results)


@app.route("/moveTheFiles", methods=['POST'])
def move_the_files():
    """Moves the dup files selected by the user to a directory for manual removal by the user."""
    if request.method == 'POST':
        file_indexes_to_move = request.get_json()
        dupFinder.move_images(file_indexes_to_move, app.config['FINAL_RESTING_PLACE'], app.config['LOCAL_ROOT'])
        return redirect(url_for('success'))


@app.route("/success")
def success():
    return render_template(
        'success.html',
        page_title='Success',
        num_moved=dupFinder.num_files_moved,
        dup_dir="C:/Users/Michele/Pictures/__delete these pictures, they are duplicates___")


@app.route("/x")
def about():
    return render_template(
        'about.html',
        page_title='About')


if __name__ == '__main__':
    # app.run()
    # # app.run(debug=False)
    # app.run(debug=True)
    app.run(host="0.0.0.0", port="33")  # http://192.168.1.16:33
    # app.run(debug=True, use_debugger=True, use_reloader=True)
