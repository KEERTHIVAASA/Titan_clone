from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product,Review_rating

def home(request):
    products= Product.objects.all().filter(is_available=True).order_by('created_date')
    
    #get reviews
    for product in products:
        reviews=Review_rating.objects.filter(product_id=product.id,status=True)
    
    context={
        'products' : products,
        'reviews': reviews
    }
    return render(request,'home.html',context)