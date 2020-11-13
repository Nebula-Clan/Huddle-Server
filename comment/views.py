from django.shortcuts import render
from authentication.models import User
from .models import Comment, PostReply, CommentReply
from posts.models import Post
from posts.serializer import PostSerializer
from user_profile.serializers import PublicProfileSerializer
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from http import HTTPStatus
from django.http.response import JsonResponse
from authentication.authenticators import SimpleAuthenticator
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_post_comment(request):
    user = request.user
    post_id = request.data.get('post')
    content = request.data.get('content')
    if not(content and post_id and user):
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
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
    return JsonResponse({'message': 'Comment submitted.', 'comment' : DisplayCommentSerializer(comment.instance).data}, status=HTTPStatus.CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_reply_comment(request):
    user = request.user
    reply_to = request.data.get('reply_to_id')
    content = request.data.get('content')
    if not(user and reply_to and content):
        return JsonResponse({'message' : "Bad request!"}, status=HTTPStatus.BAD_REQUEST)
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
    return JsonResponse({'message': 'Comment submitted.', 'comment': DisplayCommentSerializer(new_comment.instance).data}, status=HTTPStatus.CREATED)
@api_view(['GET'])
@authentication_classes([SimpleAuthenticator])
def get_post_comments(request):
    post_id = request.query_params.get('post_id', None)
    depth = request.query_params.get('depth', '0')
    startIdx = request.query_params.get('start_index', None)
    length = request.query_params.get('max_len', None)
    reply_len = request.query_params.get('max_reply_len', None)
    viewer = request.query_params.get('viewer')
    if not(depth and post_id and startIdx and length):
        return JsonResponse({"message": "Bad Request!"}, status=HTTPStatus.BAD_REQUEST)
    try:
        startIdx = int(startIdx)
        length = int(length)
        depth = int(depth)
    except:
        return JsonResponse({"message": "Inter conversion error!"}, status=HTTPStatus.BAD_REQUEST)
    if(viewer is None and  not request.user.is_anonymous):
        viewer = request.user.username
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
        result.append(RepliedCommentSerializer(comment, context={'depth' : str(depth - 1), 
                                                                 'max_len' : reply_len, 
                                                                 'viewer' : viewer, 
                                                                 'start_index': startIdx}).data)
    return JsonResponse({'post_id': post_id, 'total_comments' : total_comments, 'retrived_comments_count': len(result), 'comments': result}, status=HTTPStatus.OK)

@api_view(['GET'])
@authentication_classes([SimpleAuthenticator])
def get_reply_comments(request):
    reply_to = request.query_params.get('reply_to', None)
    depth = request.query_params.get('depth', None)
    startIdx = request.query_params.get('start_index', None)
    length = request.query_params.get('max_len', None)
    reply_len = request.query_params.get('max_reply_len', None)
    viewer = request.query_params.get('viewer')
    if not(depth and reply_to and startIdx and length):
        return JsonResponse({"message": "Bad Request!"}, status=HTTPStatus.BAD_REQUEST)
    try:
        startIdx = int(startIdx)
        length = int(length)
    except:
        return JsonResponse({"message": "Inter conversion error!"}, status=HTTPStatus.BAD_REQUEST)
    if(viewer is None and  not request.user.is_anonymous):
        viewer = request.user.username
    comment = Comment.objects.filter(id=reply_to).first()
    if(comment is None):
        return JsonResponse({'message' : "Comment not found!"}, status=HTTPStatus.NOT_FOUND)
    return JsonResponse(RepliedCommentSerializer(comment, context={'depth' : depth, 
                                                                    'start_index' : startIdx , 
                                                                    'max_len' : reply_len, 
                                                                    'viewer' : viewer,
                                                                    'start_index': startIdx}).data, status=HTTPStatus.OK)

@api_view(['GET'])
@authentication_classes([SimpleAuthenticator])
def get_user_comments(request):
    username = request.query_params.get('username')
    viewer = request.query_params.get('viewer')
    if not(username):
        return JsonResponse({"message": "Bad Request!"}, status=HTTPStatus.BAD_REQUEST)
    if(viewer is None and  not request.user.is_anonymous):
        viewer = request.user.username
    user = User.objects.filter(username=username).first()
    if(user is None):
        return JsonResponse({'message' : "User not found!"}, status=HTTPStatus.NOT_FOUND)
    return JsonResponse(data=UserCommentSerializer(user, context = {'viewer' : viewer}).data, status=HTTPStatus.OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request):
    user = request.user
    comment_id = request.data.get('id', None)
    if comment_id is None:
        return JsonResponse({"message": "Bad Request!"}, status=HTTPStatus.BAD_REQUEST)
    comment = Comment.objects.filter(id=comment_id, author=user.id).first()
    if(comment is None):
        return JsonResponse({"message": "Comment not found!"}, status=HTTPStatus.NOT_FOUND)
    comment.delete()
    return JsonResponse({'message': "Comment deleted successfully."}, status=HTTPStatus.OK)