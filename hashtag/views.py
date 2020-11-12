
from http import HTTPStatus
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from .serializers import *
from posts.serializer import PostSerializer
from .models import *
from .edit_distance import *
#  Create your views here.
@api_view(['GET'])
def get_hashtag_posts(request):
    hashtag_text = request.query_params.get('text', None)
    if(hashtag_text is None):
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
    hashtag = Hashtag.objects.filter(text=hashtag_text).first()
    if(hashtag is None):
        return JsonResponse({'message' : "Hashtag not found!"}, status=HTTPStatus.NOT_FOUND)
    records = PostHashtag.objects.filter(hashtag=hashtag.id)
    posts = [record.post for record in records]
    return JsonResponse({'hashtag' : HashtagSerializer(hashtag).data, 'posts' : PostSerializer(posts, many=True).data}, status=HTTPStatus.OK)
    
@api_view(['GET'])
def get_similar_to(request):
    string = request.query_params.get('hashtag', None)
    if(string is None):
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
    hashtags = Hashtag.objects.all()
    edit_distances = {}
    for hashtag in hashtags:
        edit_distances[hashtag] = edit_distance(string, hashtag.text, len(string), len(hashtag.text))
    hashtags = sorted(list(hashtags), key= lambda h: edit_distances[h])
    result = [h for h in hashtags if edit_distances[h] < len(h.text)]
    return JsonResponse(HashtagSerializer(result, many=True).data, status=HTTPStatus.OK)


def submit_post_hashtags(post, hashtag_list):
    for text in hashtag_list:
        hashtag = Hashtag.objects.filter(text=text).first()
        if(hashtag is None):
            data={'text': text}
            hashtag = HashtagSerializer(data=data)
            if(hashtag.is_valid()):
                hashtag.save()
                hashtag = hashtag.instance
            else:
                return (False, hashtag.errors)
        post_hashtag = PostHashtag.objects.filter(post=post.id, hashtag=hashtag.id).first()
        if(post_hashtag is not None):
            continue
        post_hashtag = PostHashtagSerializer(data={'post': post.id, 'hashtag': hashtag.id})
        if(post_hashtag.is_valid()):
            post_hashtag.save()
        else:
            return (False, post_hashtag.errors)
    return True, "Succeed!"
        
