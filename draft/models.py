from django.db import models

def get_image_directory(instance, filename):
    ext = filename.split('.')[-1]
    return f'uploads/header_images/{instance.id}.{ext}'

class DraftPost(models.Model):

    title = models.CharField(max_length = 50)
    header_image = models.ImageField(upload_to = get_image_directory, null = True)
    description = models.CharField(max_length = 200, default = "")
    post_content = models.OneToOneField('posts.Content', on_delete = models.CASCADE)
    category = models.ForeignKey('category.Category', on_delete = models.CASCADE, null = True)
    community = models.ForeignKey('community.Community', on_delete = models.CASCADE, null = True)
    date_created = models.DateTimeField(auto_now = True)
    author = models.ForeignKey('authentication.User', on_delete = models.CASCADE)
    reports_number = models.IntegerField(default = 0)

    def likes_number(self):
        from likes.models import PostLike
        return PostLike.objects.filter(post = self.id).count()

    def comments_number(self):
        from comment.models import PostReply
        return PostReply.objects.filter(post = self.id).count()