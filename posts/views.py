from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.http.response import JsonResponse
from .models import Post
from .models import Content
from authentication.models import User
from authentication.serializers import UserSerializer
from .serializer import *
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    author = request.user
    author_id = author.id

    title = request.data.get('title')
    content = request.data.get('content') # A base64 string for psot content
    category = request.data.get('category')
    content_type = request.data.get('content_type') # AV: ArticleView, OI: OnlyImage, OT: OnlyText
    description = request.data.get('description')

    header_image = request.FILES['header_image']

    post_content = Content(content_type = content_type, content_text = content)
    post_content.save()

    to_create_post = Post(title = title, description = description, post_content = post_content, category = category, author = author)
    to_create_post.save()

    # adding image field after saving post in database because of image name is generated based on post_id
    # and post_id is declared after saving post in database
    to_create_post.header_image = header_image
    to_create_post.save(update_fields = ['header_image'])

    serialized_post = PostSerializer(to_create_post).data
    return JsonResponse({"post_created" : serialized_post, "message" : f"Post created successfuly. author ID: {author_id}, post content ID: {post_content.id}"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request):
    author = request.user
    post_id = request.data.get('post_id')
    if Post.objects.filter(id = post_id).exists():
        if author.id == Post.objects.filter(id = post_id).first().author_id:
            Post.objects.filter(id = post_id).first().delete()
            return JsonResponse({"message" : f"Post with ID:{post_id} deleted successfuly"})
        else:
            return JsonResponse({"message" : f"This user with ID:{author.id} is not allowed"}, status = status.HTTP_403_FORBIDDEN)
    else:
        return JsonResponse({"message" : f"Post with ID:{post_id} does not exits"}, status = status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request):
    post_id = request.data.get('post_id')
    user = request.user
    if not(Post.objects.filter(id = post_id).first().author_id == user.id):
        return JsonResponse({"message" : "This user is not allowed"}, status = status.HTTP_403_FORBIDDEN)

    fields_to_update = request.data.get('fields_update')
    # 'title', 'description', 'content', 'category' are valid for field update

    if len(fields_to_update) == 0:
        return JsonResponse({"message" : "No field is sended to update!"})

    if 'title' in fields_to_update:
        try:
            new_title = request.data.get('title')
        except:
            return JsonResponse({"message" : "No title field is sended!"}, status = status.HTTP_400_BAD_REQUEST)
        post_finded = Post.objects.filter(id = post_id).first()
        post_finded.title = new_title
        post_finded.save(update_fields = ['title'])

    if 'description' in fields_to_update:
        try:
            new_description = request.data.get('description')
        except:
            return JsonResponse({"message" : "No description is sended!"}, status = status.HTTP_400_BAD_REQUEST)
        post_finded = Post.objects.filter(id = post_id).first()
        post_finded.description = new_description
        post_finded.save(update_fields = ['description'])
    
    if 'content' in fields_to_update:
        try:
            new_content = request.data.get('content')
        except:
            return JsonResponse({"message" : "No content field is sended!"}, status = status.HTTP_400_BAD_REQUEST)
        content_id = Post.objects.filter(id = post_id).first().post_content_id
        content_finded = Content.objects.filter(id = content_id).first()
        content_finded.content_text = new_content
        content_finded.save(update_fields = ['content_text'])

    if 'category' in fields_to_update:
        try:
            new_category = request.data.get('category')
        except:
            return JsonResponse({"message" : "No category field is sended!"}, status = status.HTTP_400_BAD_REQUEST)
        post_finded = Post.objects.filter(id = post_id).first()
        post_finded.category = new_category
        post_finded.save(update_fields = ['category'])
    
    return JsonResponse({"message" : "All fields updated successfuly"})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_posts(request):
    username = request.data.get('username')
    author = User.objects.filter(username = username).first()

    if author is None:
        return JsonResponse({"message" : f"User with username: {username} does not exist!"}, status = status.HTTP_404_NOT_FOUND)
    
    author_id = author.id
    all_posts = Post.objects.filter(author = author_id)
    serialized_posts = []
    for post in all_posts:
        serialized_posts.append(PostSerializer(post).data)

    serialized_author = PublicProfileSerializer(author).data
    
    return JsonResponse({"author" : serialized_author, "all_user_posts" : serialized_posts})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_post(request):
    post_id = request.data.get('post_id')
    post = Post.objects.filter(id = post_id).first()
    if post is None:
        return JsonResponse({"message", "Post not found!"}, status = status.HTTP_404_NOT_FOUND)
    author = User.objects.filter(id = post.author_id).first()

    serialized_post = PostSerializer(post).data
    serialized_author = UserSerializer(author).data

    return JsonResponse({"author" : serialized_author, "post" : serialized_post})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_content(request):
    content_id = request.data.get('content_id')
    content = Content.objects.filter(id = content_id).first()
    if post is None:
        return JsonResponse({"message", "Content not found!"}, status = status.HTTP_404_NOT_FOUND)
    serialized_content = ContentSerializer(content).data
    return JsonResponse({"content" : serialized_content})
    