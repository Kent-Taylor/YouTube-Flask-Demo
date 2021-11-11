from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

my_app = Flask(__name__)

base_file = os.path.abspath(os.path.dirname(__file__))
my_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_file, "app.sqlite")

db = SQLAlchemy(my_app)
marsh = Marshmallow(my_app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    link = db.Column(db.String(300), unique=False)

    def __init__(self, title, link):
        self.title = title
        self.link = link

class ProjectSchema(marsh.Schema):
    class Meta:
        fields = ("title", "link")

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


# this will create a single project:
@my_app.route("/project", methods =["POST"])
def add_project():
    title = request.json["title"]
    link = request.json["link"]

    new_project = Project(title, link)

    db.session.add(new_project)
    db.session.commit()

    project = Project.query.get(new_project.id)
    return(project_schema.jsonify(project))

# This endpoint will query ALL the projects in our database:
@my_app.route("/projects", methods=["GET"])
def get_projects():
    all_projects = Project.query.all()
    result = projects_schema.dump(all_projects)
    return(jsonify(result))

# This endpoint will query a specific project:
@my_app.route("/project/<id>", methods=["GET"])
def get_project(id):
    project = Project.query.get(id)
    return(project_schema.jsonify(project))

# This endpoint will update a specific project:
@my_app.route("/project/<id>", methods=["PUT"])
def project_update(id):
    project = Project.query.get(id)
    title = request.json["title"]
    link = request.json["link"]

    project.title = title
    project.link = link

    db.session.commit()
    return project_schema.jsonify(project)


# This endpoint will delete 1 record at a time:
@my_app.route("/project/<id>", methods=["DELETE"])
def project_delete(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()

    return(f"Project ID:{id} was successsfully deleted!")


if __name__ == "__main__":
    my_app.run(debug=True)

