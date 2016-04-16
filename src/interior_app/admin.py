from django.contrib import admin
from .models import (PortfolioObject, 
                     Photo,
                     Category,
                     Tag, 
                     Article, 
                     ArticlePhoto,
                     Sort,
                     Subscriber,
                     Feedback)

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Subscriber)
admin.site.register(Feedback)
admin.site.register(Sort)

class PhotoInline(admin.TabularInline):
    model = Photo
    
class PortfolioObjectAdmin(admin.ModelAdmin):
    inlines = [PhotoInline,]
    list_display = ["address", "area", "sort"]
        
    class Meta:
        model = PortfolioObject

admin.site.register(PortfolioObject, PortfolioObjectAdmin)

class ArticlePhotoInline(admin.TabularInline):
    model = ArticlePhoto
    
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticlePhotoInline,]
    list_display = ["title", "pub_date"]
        
    class Meta:
        model = Article

admin.site.register(Article, ArticleAdmin)