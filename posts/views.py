from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.http.response import JsonResponse
from .models import Post
from .models import Content
from category.models import Category
from community.models import Community
from authentication.models import User
from authentication.serializers import UserSerializer
from authentication.authenticators import SimpleAuthenticator
from .serializer import *
from user_profile.serializers import PublicProfileSerializer
from likes.models import PostLike
from errors.error_repository import *
from errors.serializers import ErrorSerializer
from hashtag.serializers import HashtagListSerializer
from hashtag.views import submit_post_hashtags
from category.models import categories as categories_list
from .home_post_helper import *
from huddle.settings import PCOUNT
from category.methods import *
from draft.models import DraftPost
# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request, is_draft = False):
    author = request.user
    author_id = author.id

    # is_draft = request.data.get('is_draft', False)

    title = request.data.get('title', '')
    content = request.data.get('content', '') # A base64 string for psot content
    category = request.data.get('category', None)
    content_type = request.data.get('content_type', 'OT') # AV: ArticleView, OI: OnlyImage, OT: OnlyText
    description = request.data.get('description', '')
    community_name = request.data.get('community_name')
    hashtags = request.data.get('hashtags')
    
    
    community = Community.objects.filter(name = community_name).first()
    if community is None and not (community_name is None or community_name == ''):
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_400_BAD_REQUEST)
    
    if community_name == '':
        community_name = None

    if category is None or category is "":
        post_category = None
    else:
        if len(category) > 2:
            category = next((cat[0] for cat in categories_list if cat[1] == category), 'XXXX')
        post_category = Category.objects.filter(name = category).first()
        if post_category is None:
            return JsonResponse({"error" : get_error_serialized(100, 'This category is not allowed').data}, status = status.HTTP_400_BAD_REQUEST)
    

    header_image = request.data.get('header_image')

    post_content = Content(content_type = content_type, content_text = content)
    post_content.save()

    if is_draft:
        to_create_post = DraftPost(title = title, description = description, post_content = post_content,
                                category = post_category, community = community, author = author)
    else:
        to_create_post = Post(title = title, description = description, post_content = post_content,
                                category = post_category, community = community, author = author)
    to_create_post.save()

    # adding image field after saving post in database because of image name is generated based on post_id
    # and post_id is declared after saving post in database
    to_create_post.header_image = header_image
    to_create_post.save(update_fields = ['header_image'])
    hashtags = HashtagListSerializer(data=request.data)
    if(hashtags.is_valid()):
        texts = hashtags.data['hashtags']
        value = submit_post_hashtags(to_create_post, texts)
        print(value)
    serialized_post = PostSerializer(to_create_post).data
    return JsonResponse({"post_created" : serialized_post, "message" : f"Post created successfuly. author ID: {author_id}, post content ID: {post_content.id}"})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, is_draft = False):
    author = request.user
    post_id = request.query_params.get('id', None)
    if post_id is None:
        return JsonResponse({"error" : get_error_serialized(103, 'id field is required').data}, status = status.HTTP_400_BAD_REQUEST)
    if is_draft:
        post = DraftPost.objects.filter(id = post_id).first()
    else:
        post = Post.objects.filter(id = post_id).first()
    if post is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Post not found!').data}, status = status.HTTP_400_BAD_REQUEST)
    if author.id == post.author_id:
        post.delete()
        return JsonResponse({"message" : f"Post with ID:{post_id} deleted successfuly"})
    else:
        return JsonResponse({"error" : ErrorSerializer(get_error(106)).data}, status = status.HTTP_403_FORBIDDEN)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, is_draft = False):
    post_id = request.data.get('id')
    if is_draft:
        post = DraftPost.objects.filter(id = post_id).first()
    else:
        post = Post.objects.filter(id = post_id).first()

    if post is None:
        return JsonResponse({"error" : get_error_serialized(100, 'Post not found!').data}, status = status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    if post.author_id != user.id:
        return JsonResponse({"error" : ErrorSerializer(get_error(106)).data}, status = status.HTTP_403_FORBIDDEN)
    
    # 'title', 'description', 'content', 'header_image' are valid for field update
    new_title = request.data.get('title', None)
    new_des = request.data.get('description', None)
    new_content = request.data.get('content', None)
    new_image = request.data.get('header_image', None)
    
    if new_title is not None:
        post.title = new_title
        post.save(update_fields = ['title'])

    if new_des is not None:
        post.description = new_des
        post.save(update_fields = ['description'])
    
    if new_content is not None:
        content_id = post.post_content_id
        content_finded = Content.objects.filter(id = content_id).first()
        content_finded.content_text = new_content
        content_finded.save(update_fields = ['content_text'])

    if new_image is not None:
        post.header_image = new_image
        post.save(update_fields = ['header_image'])
    
    return JsonResponse({"message" : "All fields updated successfuly"})


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([SimpleAuthenticator])
def get_user_posts(request):
    username = request.query_params.get('username', None)
    viewer = request.query_params.get('viewer', None)

    try:
        offset_str = request.query_params.get('offset', None)
        if not(offset_str is None): offset = int(offset_str)
    except:
        return JsonResponse({"error" : get_error_serialized(110, 'offset must be integer').data})
    
    if(username is None):
        return JsonResponse({"error" : ErrorSerializer(get_error(103)).data}, status = status.HTTP_400_BAD_REQUEST)
    author = User.objects.filter(username = username).first()
    if(viewer is None and not request.user.is_anonymous):
        viewer = request.user.username
    if author is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_404_NOT_FOUND)
    
    author_id = author.id
    
    all_posts = list(Post.objects.filter(author = author_id))
    all_posts.sort(key = lambda post : post.date_created, reverse = True)
    
    if not(offset_str is None):
        all_posts = all_posts[PCOUNT * offset: PCOUNT * (offset + 1)]
    
    print(all_posts)
    serialized_posts = PostSerializer(all_posts, many = True, context = {"author_depth" : False, 'content_depth' : False, 'viewer': viewer}).data

    serialized_author = PublicProfileSerializer(author).data
    
    return JsonResponse({"author" : serialized_author, "all_user_posts" : serialized_posts})


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([SimpleAuthenticator])
def get_short_post(request):
    post_id = request.query_params.get('id', None)
    viewer = request.query_params.get('viewer', None)
    if post_id is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(103)).data}, status = status.HTTP_400_BAD_REQUEST)
    post = Post.objects.filter(id = post_id).first()
    if(viewer is None and not request.user.is_anonymous):
        viewer = request.user.username
    if post is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_404_NOT_FOUND)

    serialized_post = PostSerializer(post, context = {"content_depth" : False, "author_depth" : True, 'viewer': viewer}).data

    return JsonResponse({"post" : serialized_post})

@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([SimpleAuthenticator])
def get_full_post(request):
    post_id = request.query_params.get('id', None)
    viewer = request.query_params.get('viewer', None)
    if post_id is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(103)).data}, status = status.HTTP_400_BAD_REQUEST)

    post = Post.objects.filter(id = post_id).first()
    if(viewer is None and not request.user.is_anonymous):
        viewer = request.user.username
    if post is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_404_NOT_FOUND)
    
    serialized_post = PostSerializer(post, context = {'viewer': viewer}).data

    return JsonResponse({"post" : serialized_post})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_content(request):
    content_id = request.query_params.get('id', None)
    if(content_id is None):
        return JsonResponse({"error" : ErrorSerializer(get_error(103)).data}, status = status.HTTP_400_BAD_REQUEST)
    content = Content.objects.filter(id = content_id).first()
    if content is None:
        return JsonResponse({"error" : ErrorSerializer(get_error(100)).data}, status = status.HTTP_404_NOT_FOUND)
    serialized_content = ContentSerializer(content).data
    return JsonResponse({"content" : serialized_content})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home_posts(request):
    user = request.user
    order_key = request.query_params.get('order_key', 'new') # hot, new, top
    if not order_key in ['hot', 'new', 'top']:
        return JsonResponse({"error" : ErrorSerializer(get_error(108)).data}, status = status.HTTP_400_BAD_REQUEST)
    
    category_filter = request.query_params.get('category_filter', None)
    if (category_filter is not None) and (len(category_filter) > 2):
        cf_mapped = categoryname_mapper(category_filter)
        if cf_mapped is not None: category_filter = cf_mapped 
    
    try:
        offset_str = request.query_params.get('offset', None)
        if not(offset_str is None) : offset = int(offset_str)
    except:
        return JsonResponse({"error" : get_error_serialized(110, 'offset must be integer').data})
    
    communities = [com.id for com in user.in_community.all()]
    posts = []
    for community_id in communities:
        if (category_filter is None) or (category_filter == ''):
            posts_temp = Post.objects.filter(community = community_id)
        else:
            posts_temp = Post.objects.filter(community = community_id, category = category_filter)
        for post in posts_temp:
            posts.append(post)
    
    ordered_posts = order_posts(posts, order_key)
    
    if not (offset_str is None):
        ordered_posts = ordered_posts[PCOUNT * offset:PCOUNT * (offset + 1)]

    serialized_posts = PostSerializer(ordered_posts, context = {"author_depth" : True, "content_depth" : False, "viewer" : user.username}, many = True)
    return JsonResponse({"posts" : serialized_posts.data})