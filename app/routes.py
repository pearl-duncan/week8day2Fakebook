from app import app
from flask import request
from flask_jwt_extended import jwt_required, current_user
from .models import Post
from .utils import bad_request_if_none

@app.route("/new")
@jwt_required()
def create_post():
    body = request.json

    if body is None:
        response = {
            "message": "invalid request body"
        }
        return response, 400
    
    image = body.get("img_url")
    if image is None or image =='':
        response = {
            "message": "invalid request"
        }
        return response, 400
        
    title = body.get("title")
    if title is None or title == "":
        response = {
            "message": "invalid request"
        }
        return response, 400
    
    caption = body.get("caption")
    if caption is None or caption == "":
        response = {
            "message": "invalid request"
        }
        return response, 400
    
    existing_post = Post.query.filter_by(title=title).one_or_none()
    if existing_post is not None:
        response = {
            "message": "that title is already in use"
        }
        return response, 400
    post = Post(title=title, caption=caption, created_by=current_user.id)
    post.create()
    response = {
        "message": "successfully created post",
        "post": post.to_response()
    }
    return response, 201

@app.route("/all")
def handle_get_all_posts():
    posts = Post.query.all()
    response = {
        "message": "posts retrieved",
        "posts": [post.to_response() for post in posts]
    }
    return response, 200

@app.route("/mine")
@jwt_required()
def handle_get_my_posts():
    posts = Post.query.filter_by(created_by=current_user.id).all()
    response = {
        "message": "posts retrieved",
        "posts": [post.to_response() for post in posts]
    }
    return response, 200

@app.route("/<post_id>")
@jwt_required()
def handle_get_one_post(post_id):
    post = Post.query.filter_by(id=post_id).one_or_none()
    if post is None:
        response = {
            "message": "post does not exist"
        }
        return response, 404
    response = {
        "message": "post found",
        "post": post.to_response() 
    }
    return response, 200

@app.route("/delete-post/<post_id>")
@jwt_required()
def handle_delete_post(post_id):
    post = Post.query.filter_by(id=post_id).one_or_none()
    if post is None:
        response = {
            "message": "post does not exist"
        }
        return response, 404
    if post.created_by != current_user.id:
        response = {
            "message":"you cant delete someone elses post"
        }
        return response, 401
    
    post.delete()
    response = {
        "message": f"post {post.id} deleted"
    }
    return response, 200



@app.route("/update-post/<post_id>")
@jwt_required()
def handle_update_post(post_id):
    body = request.json

    post = Post.query.filter_by(id=post_id).one_or_none()
    if post is None:
        response = {
            "message": "not found"
        }
        return response, 404
    if post.created_by != current_user.id:
        response = {"message":"not your post, can't edit"}
        return response, 401
    
    post.image = body.get("img_url", post.img_url)
    post.title = body.get("title", post.title)
    post.caption = body.get("caption", post.caption)
    
    post.update()
    response = {
        "message": "post updated",
        "post": post.to_response()
    }
    return response, 200

