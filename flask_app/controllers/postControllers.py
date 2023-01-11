from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.user import Users

@app.route("/")
def index():
    users = Users.get_all()
    print(users)
    return render_template("read.html", all_users = users)

@app.route('/create_user', methods=["POST"])
def create_friend():
    if Users.validate_user(request.form):
        data = {
            "fname": request.form["fname"],
            "lname" : request.form["lname"],
            "email" : request.form["email"]
        }
        Users.save(data)
        return redirect('/')
    else:
        return redirect('/user/new')

@app.route('/user/new')
def newUser():
    return render_template("create.html")

@app.route('/user/edit/<int:id>')
def edit(id):
    data ={
        "id":id
    }
    return render_template("edit.html", user=Users.get_user(data))

@app.route('/user/update', methods=["POST"])
def update():
    Users.update(request.form)
    return redirect("/")

@app.route('/user/destroy/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Users.destroy(data)
    return redirect('/')

@app.route('/user/show/<int:id>')
def show(id):
    data ={
        "id":id
    }
    return render_template("show.html", user=Users.get_user(data))