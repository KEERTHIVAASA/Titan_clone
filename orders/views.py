from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import Cart_item
from orders.models import Order
from .forms import OrderForm
import datetime

def payments(request):
    return render(request,'orders/payments.html')
    
def place_order(request,total=0,quantity=0):
    current_user=request.user
    # if the catrcount<=0 then redirect back
    cart_items=Cart_item.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count <=0 :
        return redirect('store')
    
    grand_total=0
    tax=0
    discount=0
    for cart_item in cart_items:
        total += (cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
    tax=(3*total)/100
    discount=(10 * total)/100
    grand_total=total-discount + tax
    
    
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            #store all user info in the table
            data= Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            
            #generate order number
            
           

            # Get the current year, day, and month as integers
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))

            # Create a date object with the obtained year, day, and month
            d = datetime.date(yr, mt, dt)

            # Format the date as "ddmmYYYY"
            current_date = d.strftime("%d%m%Y")

            # Assuming you have a 'data' object with an 'id' attribute
             # Replace YourDataObject with the actual class of your data object
            order_number = current_date + str(data.id)

            # Assign the order number to the 'order_number' attribute of the 'data' object
            data.order_number = order_number

            data.save()
            
            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context={
                'order': order,
                'cart_items': cart_items,
                'total':total,
                'discount':discount,
                'tax':tax,
                'grand_total':grand_total,
            }
            return render(request,'orders/payments.html',context)
        else:
            return redirect('checkout')

