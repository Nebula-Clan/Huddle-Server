from posts.models import Post
import datetime

def order_posts(posts, order_key):
    if order_key == 'new':
        posts.sort(key = lambda post : post.date_created, reverse = True)
    if order_key == 'top':
        posts.sort(key = lambda post : post.likes_number() + post.comments_number(), reverse = True)
    if order_key == 'hot':
        posts.sort(key = lambda post : post_tempreture(post), reverse = True)

    return posts
        
def post_tempreture(post):
    time_difference = datetime.datetime.now() - post.date_created.replace(tzinfo = None)
    if time_difference.days == 0:
        return (post.likes_number() + post.comments_number())
    return (post.likes_number() + post.comments_number()) // time_difference.days