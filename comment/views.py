from django.shortcuts import render
from authentication.models import User
from .models import PostComment
from posts.models import Post
from posts.serializer import PostSerializer
from .serializers import PostCommentSerializer
from rest_framework.decorators import api_view
from http import HTTPStatus
from django.http.response import JsonResponse
# Create your views here.

@api_view(['POST'])
def submit_comment(request):
    username = request.data.get('author')
    post_id = request.data.get('post')
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({'message' : "User not found!"}, status=HTTPStatus.NOT_FOUND)
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse({'message' : "Post not found!"}, status=HTTPStatus.NOT_FOUND)
    comment = PostCommentSerializer(data=request.data)
    if(comment.is_valid()):
        comment.save()
    else:
        return JsonResponse({'message': 'Something wrong in comment data.'}, status=HTTPStatus.BAD_REQUEST)
    return JsonResponse({'message': 'Comment submitted.'}, status=HTTPStatus.CREATED)


@api_view(['POST'])
def get_post_comments(request):
    post_id = request.data.get('post_id')
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse({'message' : "Post not found!"}, status=HTTPStatus.NOT_FOUND)
    comments = PostComment.objects.filter(post=post_id)
    if (comments == None):
        return JsonResponse({'post_id': post_id, 'comments_count': 0, 'comments': []}, status=HTTPStatus.FOUND)
    post_comments = []
    for comment in list(comments):
        post = Post.objects.filter(id=comment.post).first()
        post_comments.append(PostSerializer(post).data)
    return JsonResponse({'post_id': post_id, 'comments_count': len(post_comments), 'comments': post_comments}, status=HTTPStatus.FOUND)



@api_view(['POST'])
def get_user_comments(request):
    username = request.data.get('username')
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({'message' : "User not found!"}, status=HTTPStatus.NOT_FOUND)
    comments = PostComment.objects.filter(author=user.id)
    if (comments == None):
        return JsonResponse({'username': username, 'comment_count': 0, 'comments': []}, status=HTTPStatus.FOUND)
    user_comments = []
    for comment in list(comments):
        user_comments.append(PostCommentSerializer(comment).data)
    return JsonResponse({'username': username, 'comment_count': len(user_comments), 'comments': user_comments}, status=HTTPStatus.FOUND)