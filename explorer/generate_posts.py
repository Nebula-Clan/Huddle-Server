from authentication.models import User
from community.models import Community
from posts.models import Post
from hashtag.models import PostHashtag
from follow.models import UserFollowing
from likes.models import PostLike

def related_community(user):

    communities = user.in_community()
    for community in communities:
        com_posts = Post.objects.filter(community = community.id)

    hashtags = []
    for post in com_posts:
        hashtags.extend(PostHashtag.objects.filter(post = post.id).values_list('hashtag'))

    hashtags_set = set(hashtags)

    posts_found =[]
    for hashtag in hashtags_set:
        posts_found.extend(PostHashtag.objects.filter(hashtag = hashtag).values_list('post'))
    
    return posts_found

def related_followings(user):
    
    followings = UserFollowing.objects.filter(user = user).values_list('following_user')

    posts = []
    for following in followings:
        followings_2 = UserFollowing.objects.filter(user = following).values_list('following_user')
        for following_2 in followings_2:
            posts.extend(Post.objects.filter(author = following_2))
    
    return posts
    
def related_likes(user):
    
    posts_liked = PostLike.objects.filter(user = user.id).values_list('post')
    return posts_liked
    
    hashtags = []
    for post in posts_liked:
        hashtags.extend(PostHashtag.objects.filter(post = post))
    
    hashtags_set = set(hashtags)

    posts_found = []
    for hashtag in hashtags_set:
        posts_found.extend(PostHashtag.objects.filter(hashtag = hashtag))
    
    return posts_found
