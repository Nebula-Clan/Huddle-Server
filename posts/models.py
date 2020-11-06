from django.db import models
from authentication.models import User
# Create your models here.

def get_image_directory(instance, filename):
    ext = filename.split('.')[-1]
    return f'uploads/header_images/{instance.id}.{ext}'

class Post(models.Model):
    CategoryChoices = [
        ('SPORT', 'Sport'),
        ('SOCIAL', 'Social'),
        ('PROGRAMMING', 'Programming'),
        ('PLITICAL', 'Political'),
        ('CINEMA', 'Movie And Cinema'),
        ('HEALTH', 'Health'),
        ('MUSIC', 'Music'),
        ('GAMING', 'Gaming'),
        ('FUN', 'Fun'),
        ('NEWS', 'News'),
        ('MEME', 'Memes'),
        ('TECH', 'Technology'),
        ('AD', 'Art And Design'),
        ('FOOD', 'Food'),
        ('EDU', 'Education'),
        ('SCIENCE', 'Science'),
        ('BOOK', 'Book And Wrting'),
        ('BEUTY', 'Beuty'),
        ('DISCUSSION', 'Discussion'),
        ('QA', 'Q & A'),
        ('MEDICIAN', 'Medician'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length = 50)
    header_image = models.ImageField(upload_to = get_image_directory, null = True)
    description = models.CharField(max_length = 200, default = "")
    post_content = models.OneToOneField('posts.content', on_delete = models.CASCADE)
    category = models.CharField(choices = CategoryChoices, max_length = 20, default = 'OTHER')
    date_created = models.DateTimeField(auto_now = True)
    author = models.ForeignKey('authentication.User', on_delete = models.CASCADE)


class Content(models.Model):
    TypeContentChioces = [('AV', 'Article View'), ('OT', 'Only Text'), ('OI', 'Only Image')]
    content_type = models.CharField(choices = TypeContentChioces, max_length = 2, default = 'OI')
    content_text = models.TextField()
