from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete= models.CASCADE)
    raitingAuthor = models.SmallIntegerField(default= 0)


    def update_raiting(self):
        posRat = self.post_set.aggregate(postRat = Sum('raiting'))
        pRat = 0
        pRat += posRat.get('postRat')

        commentRat = self.authorUser.comment_set.aggregate(commRat = Sum('raiting'))
        cRat = 0
        cRat += commentRat.get('commRat')

        self.raitingAuthor = pRat*3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length= 64, unique= True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete= models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length= 2, choices= CATEGORY_CHOICES, default= ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add= True)
    postCategory = models.ManyToManyField(Category, through= 'PostCategory')
    title = models.CharField(max_length= 128)
    text = models.TextField()
    raiting = models.SmallIntegerField(default= 0)

    def like(self):
        self.raiting += 1
        self.save()

    def dislike(self):
        self.raiting -= 1
        self.save()

    def preview(self):
        return '{} ...'.format(self.text[0:123]) # Метод для избавления от проблем с конкатенацией!


class PostCategory(models.Model):
    postTrough = models.ForeignKey(Post, on_delete= models.CASCADE)
    categoryTrough = models.ForeignKey(Category, on_delete= models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete= models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete= models.CASCADE)
    text = models.TextField()
    dateComment = models.DateTimeField(auto_now_add= True)
    raiting = models.SmallIntegerField(default=0)

    def like(self):
        self.raiting += 1
        self.save()

    def dislike(self):
        self.raiting -= 1
        self.save()