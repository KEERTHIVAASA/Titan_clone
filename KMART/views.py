# from django.http import HttpResponse
# from django.shortcuts import render
# from store.models import Product,Review_rating

# def home(request):
#     products= Product.objects.all().filter(is_available=True).order_by('created_date')
    
#     #get reviews
#     for product in products:
#         reviews=Review_rating.objects.filter(product_id=product.id,status=True)
    
#     context={
#         'products' : products,
#         'reviews': reviews
#     }
#     return render(request,'home.html',context)
from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product, Review_rating

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    # Initialize an empty list to accumulate reviews
    all_reviews = []

    # Iterate through each product to fetch reviews
    for product in products:
        reviews = Review_rating.objects.filter(product_id=product.id, status=True)
        # Extend the all_reviews list with reviews for the current product
        all_reviews.extend(reviews)

    context = {
        'products': products,
        'reviews': all_reviews,  # Pass all_reviews instead of reviews
    }
    return render(request, 'home.html', context)
