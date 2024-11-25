from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return all pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return a picture by id"""
    picture = [picture for picture in data if picture["id"] == id]
    if picture:
        return jsonify(picture[0]), 200

    return {"message": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """create a picture"""
    picture = request.get_json()
    if any(p["id"] == picture["id"] for p in data):
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """update a picture"""
    picture = request.get_json()
    for i, p in enumerate(data):
        if p["id"] == id:
            data[i] = picture
            return jsonify(picture), 201

    return jsonify({"Message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """delete a picture"""
    for i, p in enumerate(data):
        if p["id"] == id:
            data.pop(i)
            return jsonify({"message": "picture deleted"}), 204

    return jsonify({"Message": "picture not found"}), 404
