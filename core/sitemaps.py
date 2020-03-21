from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    
    priority = 0.2
    
    def items(self):
        return Post.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_on