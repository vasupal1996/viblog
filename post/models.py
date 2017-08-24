import os

from bs4 import BeautifulSoup
from PIL import Image

from django.conf import settings

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.files import File

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.shortcuts import redirect, get_list_or_404

from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.utils.module_loading import import_string

from viblog.settings import MARKDOWNX_MARKDOWNIFY_FUNCTION

class Post(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    author = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True, auto_now=False)
    date_updated = models.DateField(auto_now=True, auto_now_add=False )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        # ordering = ('-date_created','-date_updated')

    def get_posts(author):
        try:
            list_posts = Post.objects.filter(author=author)
            print (list_posts)
            if list_posts is not None:
                return list_posts
            else:
                return False
        except Exception:
            return False
            
    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug': self.slug})

    def get_tags(self):
        tags = Tag.objects.filter(post=self)
        return tags

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(',')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(tag=tag.lower(), post=self)

    def get_comment(self):
        comments = Comment.objects.filter(post=self) 
        return comments

    def create_comments(post, user, comment):
        t, created = Comment.objects.get_or_create(post=post, comment=comment, user=user)

    def get_summary(self):
        if len(self.content) > 150:
            return '{0}...'.format(self.content[:350])
        else:
            return self.content
    
    def get_summary_as_markdown(self):
        markdownify = import_string(MARKDOWNX_MARKDOWNIFY_FUNCTION)
        return markdownify(self.get_summary())

    def get_thumbnail(self):    
        # markdownify = import_string(MARKDOWNX_MARKDOWNIFY_FUNCTION)
        # content = BeautifulSoup(markdownify(self.content))

        # try:
        #     img_link = content.findAll('img')[0].get('src')
        #     print (img_link)
        # except:
        #     img_link = 'http://howtorecordpodcasts.com/wp-content/uploads/2012/10/YouTube-Background-Pop-4.jpg'
        # return img_link
        markdownify = import_string(MARKDOWNX_MARKDOWNIFY_FUNCTION)
        content = BeautifulSoup(markdownify(self.content), "html5lib")
        try:
            img_link = content.findAll('img')[0].get('src')
        except:
            img_link = 'http://howtorecordpodcasts.com/wp-content/uploads/2012/10/YouTube-Background-Pop-4.jpg'
        return img_link


    # def get_likes(self, atype):
    #     values = Activity.objects.filter(activity_type = atype, post=post).count()
    #     return (values)

        
    # def get_likes(self):
    #     t = Activity.calculate_activity(self, atype='L')
    #     return t

    # def get_dislikes(self):
    #     t = Activity.calculate_activity(self, atype='D')
    #     return t

    # def create_like(self, user):
    #     Activity.create_activity(user, self, atype='L')

    # def create_dislike(self, user):
    #     Activity.create_activity(user, self, atype='D')


def pre_post(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_post, sender=Post)

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = "%s%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

class Tag(models.Model):
    tag = models.CharField(max_length=100, null=True, blank=True)
    post = models.ForeignKey(Post, null=True)    

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class Comment(models.Model):
    post = models.ForeignKey(Post)
    comment = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User) 

    def __str__(self):
        return self.comment