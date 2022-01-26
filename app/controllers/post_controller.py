from app.models.post_model import Post
from flask import jsonify, request

def generate_id():
	last_post = Post.id_generator()
	return last_post

def get_posts():
	all_posts = Post.get_db_posts()
	all_posts = list(all_posts)

	return jsonify(all_posts), 200

def create_new_post():
	try:
		data = request.get_json()
		post = Post(**data)
		post.create_post()
		return jsonify(post.__dict__), 201
	
	except:
		return{"message": "Invalid request"}, 400


def dell_post(post_id):

	deleted_post = Post.delete_post(post_id)
	if deleted_post:
		return jsonify(deleted_post), 200
	
	return {"message": "Invalid id"}, 404

def patch_post(post_id):
	data = request.get_json()
	data["updated_at"] = Post.update_time()
	update = Post.update_post(post_id, data)
	try:
		if update["message"] == "Id not found":
			return update, 404
		elif update["message"] == "Invalid JSON request":
			return update, 400
	except:
		return jsonify(update), 200

def get_post_by_id(post_id):
	post = Post.read_post_by_id(post_id)

	if post:
		return jsonify(post), 200
	
	return {"message": "Id not found"}, 404