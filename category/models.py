from django.db import models

categories = [
    ('A', 'Art'),
    ('H', 'Health'),
    ('M', 'Music'),
    ('FS', 'Film & Series'),
    ('SP', 'Sport'),
    ('P', 'Politics'),
    ('C', 'Computers'),
    ('FA', 'Fashion'),
    ('FO', 'Food'),
    ('TR', 'Travel'),
    ('G', 'Games'),
    ('SC', 'Science'),
    ('NA', 'Nature'),
    ('PS', 'Psychology'),
    ('PR', 'Programming'),
    ('F', 'Fun'),
    ('NE', 'News'),
    ('M', 'Meme'),
    ('TE', 'Technology'),
    ('B', 'Book And Wrting')
]

icons = [
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no',
    'no'
]

def update_category_table():
    for counter in range(len(categories)):
        cat = categories[counter]
        icon = icons[counter]
        finded_category = Category.objects.filter(name = cat[0]).first()
        if not (finded_category is None):
            if finded_category.icon == icon: continue
        category = Category(name = cat[0], icon = icon)
        category.save()

class Category(models.Model):

    CategoryChoices = categories
    icon = models.CharField(max_length = 100, null = False)
    name = models.CharField(max_length = 50, choices = CategoryChoices, null = False, primary_key = True)
