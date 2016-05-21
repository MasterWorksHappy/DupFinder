from flask import Flask, render_template, request, redirect, url_for, flash

from DupFinder import DupFinder
from dir_walk import DirWalker

app = Flask(__name__)
app.secret_key = 'mam'
dw = DirWalker()
df = DupFinder()


@app.route("/")
def get_dirs():
    flash("pushing on to Directories Selection")
    return render_template(
        'get_paths.html',
        page_title='Select Directories',
        jsonTreeData=dw.dirTree)


@app.route("/get_paths", methods=['POST'])
def get_paths():
    if request.method == 'POST':
        # dir_indexes = request.get_json()
        # dir_indexes = json.loads(request.args.get('dirIdxs'))
        dw.setIndex(request.get_json())
        # dw.setIndex(request.form.getlist('dirIdxs'))
        dw.setSearchDirs()
        flash("pushing on to Show Me the Money")
        return redirect(url_for('show_me_the_money'))


@app.route("/show_me_the_money")
def show_me_the_money():
    df.searchDirs(dw.dirList)
    urls = df.getURLResults()
    if len(urls) == 0:  # no dups found
        flash("pushing on to Good Job")
        return render_template(
            'Good Job.html',
            page_title='Good Job!')
    else:  # results ready to be displayed

        flash("pushing on to Duplication Results Display")
        return render_template(
            'duply.html',
            page_title='Results',
            results=urls)


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
