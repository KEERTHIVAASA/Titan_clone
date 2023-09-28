from django.contrib import admin
import admin_thumbnails
from .models import Product,Product_gallery

@admin_thumbnails.thumbnail('image')
class Productgalleryinline(admin.TabularInline):
    model=Product_gallery
    extra=1
    

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','category','modified_at','is_available')
    prepopulated_fields={
        'slug': ('product_name',)
    }
    inlines=[Productgalleryinline]
    
    

admin.site.register(Product,ProductAdmin)
admin.site.register(Product_gallery)
