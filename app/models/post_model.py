from datetime import datetime
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")

db = client["kenzie"]


class Post:

    def __init__(self, title: str, author: str, tags: list, content: str) -> None:
        self._id = self.id_generator()
        self.title = title
        self.author = author
        self.content = content
        self.tags = tags
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def create_post(self):
        db.posts.insert_one(self.__dict__)
    
    @staticmethod
    def id_generator():
        all_posts = db.posts.find()
        list_posts = [post for post in all_posts]

        try:
            last_post_id = list_posts[-1]["_id"]
            return last_post_id + 1
        
        except:
            return 1

    @staticmethod
    def get_db_posts():
        posts = db.posts.find()
        return posts

    @staticmethod
    def update_time():
        return datetime.now()

    @staticmethod
    def delete_post(post_id):
        deleted_post = db.posts.find_one_and_delete({"_id": int(post_id)})
        return deleted_post

    @staticmethod
    def update_post(post_id, data):
        post = db.posts.find_one({"_id": int(post_id)})
        try:
            post_keys = list(post.keys())
            data_keys = list(data.keys())
            for keys in data_keys:
                if not keys in post_keys:
                    return {"message": "Invalid JSON request"}
            updated_post = db.posts.find_one_and_update({"_id": int(post_id)}, {"$set": {**data}})
            return updated_post
        
        except:
            return {"message": "Id not found"}
        
    @staticmethod
    def read_post_by_id(post_id):
        post = db.posts.find_one({"_id": int(post_id)})
        return post