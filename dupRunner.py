from flask import Flask, render_template, request, redirect, url_for

from DupFinder import DupFinder
from dir_walk import DirWalker

app = Flask(__name__)
app.secret_key = 'mam'
dw = DirWalker()
df = DupFinder()

@app.route("/")
def get_dirs():
    return render_template(
        'get_paths.html',
        page_title='Select Directories',
        jsonTreeData=dw.dirTree)


@app.route("/get_paths", methods=['POST'])
def get_paths():
    if request.method == 'POST':
        dw.setSearchDirs(request.get_json())
        return redirect(url_for('show_me_the_money'))

@app.route("/show_me_the_money")
def show_me_the_money():
    df.searchDirs(dw.dirList)
    # results1 = df.getURLResults()
    results = df.getTreeResults()
    if len(results) == 0:  # no dups found
        return render_template(
            'Good Job.html',
            page_title='Good Job!')
    else:  # results ready to be displayed
        return render_template(
            'getDupsToDelete.html',
            page_title='Results',
            jsonTreeData=results)
        # return render_template(
        #     'duply.html',
        #     page_title='Results',
        #     results=results)


@app.route("/moveTheFiles", methods=['POST'])
def moveTheFiles():
    if request.method == 'POST':
        pass
        # dw.setSearchDirs(request.get_json())
        # return redirect(url_for('show_me_the_money'))

@app.route("/x")
def about():
    return render_template(
        'about.html',
        page_title='About')


if __name__ == '__main__':
    # # app.run(debug=False)
    # app.run(debug=True)
    # app.run()
    # app.run(host="0.0.0.0", port="33")
    app.run(debug=True, use_debugger=True, use_reloader=True)
