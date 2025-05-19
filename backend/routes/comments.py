from flask import Blueprint, request, jsonify, session
from pymongo import MongoClient
from bson import ObjectId

import os

comments_bp = Blueprint("comments", __name__) 

# connect to MongoDB using URI from environment variables
mongo_uri = os.environ.get("MONGO_URI", "mongodb://root:rootpassword@localhost:27017/mydatabase?authSource=admin")  #references: https://docs.python.org/3/library/os.html#os.environ
client = MongoClient(mongo_uri) #references: https://pymongo.readthedocs.io/en/stable/tutorial.html#connecting-to-mongodb
db = client.get_database("mydatabase")  # explicitly define the DB name for local pytest


@comments_bp.route("/api/comments", methods=["POST"])
def post_comment():
    user = session.get("user") #references: https://flask.palletsprojects.com/en/2.3.x/api/#flask.session
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()  #references: https://flask.palletsprojects.com/en/2.3.x/api/#flask.Request.get_json
    article_id = data.get("articleId")
    text = data.get("text")

    if not article_id or not text:
        return jsonify({"error": "Missing fields"}), 400

    #save the comment to MongoDB
    comment = {
        "articleId": article_id,
        "text": text,
        "user": user["email"]
    }

    result = db.comments.insert_one(comment) #references: https://pymongo.readthedocs.io/en/stable/tutorial.html#inserting-a-document
    comment["_id"] = str(result.inserted_id) #convert ObjectId to string so frontend can read it

    return jsonify(comment), 201

@comments_bp.route("/api/comments", methods=["GET"])
def get_comments():
    article_id = request.args.get("articleId")  #references: https://flask.palletsprojects.com/en/2.3.x/api/#flask.Request.args
    if not article_id:
        return jsonify({"error": "Missing articleId parameter"}), 400

    #find all comments that match this article ID
    comment_docs = db.comments.find({"articleId": article_id})  #eferences: https://pymongo.readthedocs.io/en/stable/tutorial.html#querying-for-more-than-one-document

    #convert MongoDB documents to plain Python dicts and convert ObjectId to string
    comments = []
    for doc in comment_docs:
        comment = {
            "_id": str(doc["_id"]),
            "articleId": doc["articleId"],
            "text": doc["text"],
            "user": doc.get("user", "unknown")
        }
        comments.append(comment)

    return jsonify(comments), 200

@comments_bp.route("/api/comments/<comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    user = session.get("user")  # get the current logged-in user from session

    # only allow moderators to delete comments
    if not user or user.get("email") != "moderator@hw3.com":
        return jsonify({"error": "Unauthorized"}), 403

    try:
        # update comment to show mods deleted or removed it
        result = db.comments.update_one(
            {"_id": ObjectId(comment_id)},  # filter: find by _id
            {"$set": {"text": "Your comment was removed by a moderator. "}} # update the comment to show it was removed
        )
        #references: https://www.mongodb.com/docs/manual/reference/method/db.collection.updateOne/

        # if no document matched the comment ID, return 404
        if result.matched_count == 0:
            return jsonify({"error": "Comment not found"}), 404

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

