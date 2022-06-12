from django.contrib import admin
from .models import Post, Caption, Feed

admin.site.register(Caption)
admin.site.register(Post)
admin.site.register(Feed)

# Register your models here.
