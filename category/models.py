from django.db import models

categories = [
    ('A', 'Art'),
    ('B', 'Books'),
    ('C', 'Computers'),
    ('FA', 'Fashion'),
    ('FS', 'Films'),
    ('FO', 'Food'),
    ('FU', 'Fun'),
    ('G', 'Games'),
    ('T', 'TV Series'),
    ('H', 'Health'),
    ('M', 'Music'),
    ('NE', 'News'),
    ('NA', 'Nature'),
    ('P', 'Politics'),
    ('PS', 'Psychology'),
    ('SC', 'Science'),
    ('TE', 'Technology'),
    ('TR', 'Travel'),
]

icons = [
    'mdi-camera',
    'mdi-book',
    'mdi-memory',
    'mdi-hanger',
    'mdi-video-vintage',
    'mdi-silverware-variant',
    'mdi-emoticon',
    'mdi-gamepad-variant',
    'mdi-filmstrip',
    'mdi-hospital',
    'mdi-headphones',
    'mdi-newspaper',
    'mdi-pine-tree',
    'mdi-bank',
    'mdi-brain',
    'mdi-sigma',
    'mdi-laptop',
    'mdi-train-car'
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

    all_categories = Category.objects.all()
    categories_id = [cat[0] for cat in categories]
    for category in all_categories:
        if not(category.name in categories_id):
            Category.objects.get(name = category.name).delete()

class Category(models.Model):

    CategoryChoices = categories
    icon = models.CharField(max_length = 100, null = False)
    name = models.CharField(max_length = 50, choices = CategoryChoices, null = False, primary_key = True)
