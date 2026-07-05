from django.contrib import admin
from .models import Award, Comment, Follow, Like, Vote

admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Vote)
admin.site.register(Comment)
admin.site.register(Award)
