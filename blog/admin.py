from django.contrib import admin

from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    list_filter = ('user', )
    search_fields = ('title', 'body')


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
