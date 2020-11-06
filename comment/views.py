from django.shortcuts import render
from authentication.models import User
from .models import Comment, PostReply, CommentReply
from posts.models import Post
from posts.serializer import PostSerializer
from user_profile.serializers import PublicProfileSerializer
from .serializers import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from http import HTTPStatus
from django.http.response import JsonResponse
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_post_comment(request):
    username = request.data.get('author')
    post_id = request.data.get('post')
    content = request.data.get('content')
    if not(content and post_id and username):
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({'message' : "User not found!"}, status=HTTPStatus.NOT_FOUND)
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse({'message' : "Post not found!"}, status=HTTPStatus.NOT_FOUND)
    data = {'author' : user.id, 'content' : content}
    comment = CommentSerializer(data=data)
    if(comment.is_valid()):
        comment.save()
    else:
        return JsonResponse(comment.errors, status=HTTPStatus.BAD_REQUEST)
    data = {'post': post_id, 'reply': comment.instance.id}
    reply_post = PostReplySerializer(data=data)
    if(reply_post.is_valid()):
        reply_post.save()
    else :
        return JsonResponse(reply_post.errors, status=HTTPStatus.BAD_REQUEST)
    return JsonResponse({'message': 'Comment submitted.', 'comment' : comment.data}, status=HTTPStatus.CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_reply_comment(request):
    username = request.data.get('author')
    reply_to = request.data.get('reply_to_id')
    content = request.data.get('content')
    if not(username and reply_to and content):
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({'message' : "User not found!"}, status=HTTPStatus.NOT_FOUND)
    comment = Comment.objects.filter(id=reply_to).first()
    if(comment is None):
        return JsonResponse({'message' : "Comment not found!"}, status=HTTPStatus.NOT_FOUND)
    data = {'author' : user.id, 'content' : content}
    new_comment = CommentSerializer(data=data)
    if(new_comment.is_valid()):
        new_comment.save()
    else:
        return JsonResponse(new_comment.errors, status=HTTPStatus.BAD_REQUEST)
    data = {'reply_to': reply_to, 'reply': new_comment.instance.id}
    reply_comment = CommentReplySerializer(data=data)
    if(reply_comment.is_valid()):
        reply_comment.save()
    else :
        return JsonResponse(reply_comment.errors, status=HTTPStatus.BAD_REQUEST)
    return JsonResponse({'message': 'Comment submitted.', 'comment': new_comment.data}, status=HTTPStatus.CREATED)
@api_view(['GET'])
def get_post_comments(request):
    post_id = request.query_params.get('post_id', None)
    depth = request.query_params.get('depth', None)
    startIdx = request.query_params.get('start_index', None)
    length = request.query_params.get('max_len', None)
    reply_len = request.query_params.get('max_reply_len', None)
    
    if not(depth and post_id and startIdx and length):
        return JsonResponse({"message": "Bad Request!"}, status=HTTPStatus.BAD_REQUEST)
    try:
        startIdx = int(startIdx)
        length = int(length)
        depth = int(depth)
    except:
        return JsonResponse({"message": "Inter conversion error!"}, status=HTTPStatus.BAD_REQUEST)
    post = Post.objects.filter(id=post_id).first()
    if(post is None):
        return JsonResponse({'message' : "Post not found!"}, status=HTTPStatus.NOT_FOUND)
    post_comments = PostReply.objects.filter(post=post_id)
    result = []
    post_comments = list(post_comments)
    total_comments = len(post_comments)
    if(startIdx >= len(post_comments)):
        return JsonResponse({"message": "Invalid start index!"}, status=HTTPStatus.BAD_REQUEST)
    post_comments = post_comments[startIdx: startIdx + length]
    for comment in list(post_comments):
        comment = comment.reply
        if(comment is None):
            continue
        result.append(PostCommentsSerializer(comment, context={'depth' : str(depth - 1), 'max_len' : reply_len}).data)
    return JsonResponse({'post_id': post_id, 'total_comments' : total_comments, 'retrived_comments_count': len(result), 'comments': result}, status=HTTPStatus.FOUND)

@api_view(['GET'])
def get_reply_comments(request):
    reply_to = request.query_params.get('reply_to', None)
    depth = request.query_params.get('depth', None)
    startIdx = request.query_params.get('start_index', None)
    length = request.query_params.get('max_len', None)
    reply_len = request.query_params.get('max_reply_len', None)
    if not(depth and reply_to and startIdx and length):
        return JsonResponse({"message": "Bad Request!"}, status=HTTPStatus.BAD_REQUEST)
    try:
        startIdx = int(startIdx)
        length = int(length)
    except:
        return JsonResponse({"message": "Inter conversion error!"}, status=HTTPStatus.BAD_REQUEST)
    comment = Comment.objects.filter(id=reply_to).first()
    if(comment is None):
        return JsonResponse({'message' : "Comment not found!"}, status=HTTPStatus.NOT_FOUND)
    return JsonResponse(PostCommentsSerializer(comment, context={'depth' : depth , 'max_len' : reply_len}).data, status=HTTPStatus.FOUND)

@api_view(['GET'])
def get_user_comments(request):
    username = request.query_params.get('username')
    if not(username):
        return JsonResponse({"message": "Bad Request!"}, status=HTTPStatus.BAD_REQUEST)
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({'message' : "User not found!"}, status=HTTPStatus.NOT_FOUND)
    # print(user.id)
    # comments = Comment.objects.filter(author=user.id)
    # if (comments == None):
    #     return JsonResponse({'username': username, 'comment_count': 0, 'comments': []}, status=HTTPStatus.FOUND)
    # user_comments = []
    # for comment in list(comments):
    #     user_comments.append(CommentSerializer(comment).data)
    return JsonResponse(data=UserCommentSerializer(user).data, status=HTTPStatus.FOUND)