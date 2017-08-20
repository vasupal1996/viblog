from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from post.models import Post , Tag



class Activity(models.Model):
    LIKE = 'L'
    DISLIKE = 'D'
    ACTIVITY_TYPE = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    )
    user = models.ForeignKey(User)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPE)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.activity_type

    def create_activity(user, post, atype):
        if user in User.objects.filter(username=user.username):
            print ('here')
            if (atype == 'L' or atype == 'D'):    
                print('here1')
                activity = Activity()
                activity.user = user
                activity.activity_type = atype
                activity.post = post
                activity.save()
                return (True)
            else:
                return (False)
        
    def calculate_activity(post, atype):
        values = Activity.objects.filter(activity_type = atype, post=post).count()
        return (values)

    
    # def create_comment(user, post, comment):
    #     post_comment = Comment(user=user, post=post, comment=comment)
    #     comment.save()
    #     return (True)

    # def get_comment(post):
    #     comments = Comment.objects.filter(post=post)
    #     return (comments)



# class PostFeed(models.Model):

#     activity = models.ForeignKey(Activity, null=True, blank=True)
#     user = models.ForeignKey(User, null=True, blank=True)
#     topics = models.CharField(max_length=None)
#     tags = models.ForeignKey(Tag, null=True, blank=True)


#     def __str__(self):
#         self.topics

#     class Meta:
#         db_table = ''
#         managed = True
#         verbose_name = 'PostFeed'
#         verbose_name_plural = 'PostFeeds'


    # def create_topics(topics, *args, **kwargs)
    # topics = topics.strip()
    # topic_list = topic.split(',')

    # user = request.user
    

    # for topic in topic_list:
    #     if topic:
    #         t, created = PostFeed.get_or_create(topics=topic, )
