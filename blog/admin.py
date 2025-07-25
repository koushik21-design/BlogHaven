from django.contrib import admin
from blog.models import Category,Blog,Comment,Like,Dislike

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    list_display=('title','category','author','status','is_featured')
    search_fields=('id','title','category__category_name','status')
    list_editable=('is_featured',)

admin.site.register(Category)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Dislike)
