from .views import PostView, TagView, SubscriptionView
from django.urls import path
# Users should be able to browse all the tags and 
# see all the posts for a specific tag.

# A Post should contain title, text and tags (multiple). 
# A post can also have audio.

# Users should be able to search posts by title, user's name or text.

urlpatterns = [
    path('post', PostView.as_view()),
    # like, dislike, viewed
    path('post/<int:pk>/<str:action>', PostView.as_view()),
    path('tag', TagView.as_view()),
    path('subscribe', SubscriptionView.as_view()),
]