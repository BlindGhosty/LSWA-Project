from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.forms import ModelForm, TextInput

class Post(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL)
  text = models.CharField(max_length=256, default="")
  pub_date = models.DateTimeField('date_posted')
  def __str__(self):
    if len(self.text) < 16:
      desc = self.text
    else:
      desc = self.text[0:16]
    return self.user.username + ':' + desc

class Following(models.Model):
  follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_follows")
  followee = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="user_followed")
  follow_date = models.DateTimeField('follow data')
  def __str__(self):
    return self.follower.username + "->" + self.followee.username

# Our recommendation model(s):
class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name="user_to_rec_for")
    recommended_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name="user_recommended")
    weight = models.DecimalField(max_digits=10, decimal_places=5, default=0.00000)
    def __str__(self):
      return self.follower.username + " ?-> " + self.followee.username

class time_recommendation_given(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name="user_with_rec")
    gen_date = models.DateTimeField('recommend date')

# Model Forms
class PostForm(ModelForm):
  class Meta:
    model = Post
    fields = ('text',)
    widgets = {
      'text': TextInput(attrs={'id' : 'input_post'}),
    }

class FollowingForm(ModelForm):
  class Meta:
    model = Following
    fields = ('followee',)

class MyUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    help_texts = {
      'username' : '',
    }
