from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Product_gallery,Review_rating
from category.models import Category
from carts.models import Cart_item
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages


def store(request,category_slug=None):
    categories = None
    products = None
    
    if category_slug != None :
        categories = get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories).order_by('id')
        paginator= Paginator(products,1)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
        
    else:
        products= Product.objects.all().filter(is_available=True).order_by('id')
        paginator= Paginator(products,6)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=products.count()
    
    context={
        'products' : paged_products,
        'product_count' : product_count,
    }
    return render(request,'store/store.html',context)


def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=Cart_item.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        
    except Exception as e:
        raise e
    
    product_gallery= Product_gallery.objects.filter(product_id=single_product.id)
    
    #get reviews
    reviews=Review_rating.objects.filter(product_id=single_product.id,status=True)
    
    context={
        'single_product' : single_product,
        'in_cart' : in_cart,
        'product_gallery' : product_gallery,
        'reviews':reviews,
        
    }
        
    return render(request,'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET :
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=products.count()
        context={
            'products' : products,
            'product_count' :  product_count,
        }
    return render(request,'store/store.html',context)

def submit_review(request,product_id):
    url=request.META.get('HTTP_REFERER')
    if request.method =='POST':
        try:
            reviews=Review_rating.objects.get(user__id=request.user.id, product__id=product_id)
            form=ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'Thank you your Review has been updated.')
            return redirect(url)
            
        except Review_rating.DoesNotExist:
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=Review_rating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,'Thank you your Review has been Submitted.')
                return redirect(url)
            