from django.http import JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from ecommerceapp.models import Contact,Product,OrderUpdate,Orders, Services, ServiceAppointments
from math import ceil
from ecommerceapp import keys
MERCHANT_KEY=keys.MK
import json
from django.views.decorators.csrf import  csrf_exempt
from PayTm import Checksum
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from datetime import date
import json
import re
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Cart, Product

# from models import Orders
#from PayTm import Checksum
# Create your views here.

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'product_id')  # Changed from id to product_id
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds}
    return render(request, "index.html", params)

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"We will get back to you soon..")
        return render(request,"contact.html")


    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")



def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    # Get cart items for the user
    cart_items = Cart.objects.filter(user_id=request.user.id)
    cart_total = sum(item.total_price for item in cart_items)

    if request.method == "POST":
        # Process the order
        try:
            order = Orders.objects.create(
                items_json=", ".join([item.product_name for item in cart_items]),
                amount=cart_total,
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                address1=request.POST.get('address1'),
                address2=request.POST.get('address2'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                zip_code=request.POST.get('zip_code'),
                phone=request.POST.get('phone')
            )
            
            # Generate order ID
            oid = f"{order.order_id}WeShopCart"
            order.oid = oid
            order.or_id = oid
            order.save()

            # Create order update
            OrderUpdate.objects.create(
                order_id=order.order_id,
                update_desc="The order has been placed",
                or_id=oid,
                email=request.user.username
            )

            # Clear the cart after successful order
            cart_items.delete()

            return render(request, 'gateway.html', {
                'dict1': {
                    'ORDER_ID': oid,
                    'TXN_AMOUNT': str(cart_total)
                }
            })

        except Exception as e:
            messages.error(request, f"Error processing order: {str(e)}")
            return redirect('checkout')

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total
    }
    return render(request, "checkout.html", context)

def paytm(request):
    if request.method == "POST":
        or_id = request.POST.get('id','')
        txn_amt = request.POST.get('amt','')
        cardno = request.POST.get('cardNumber','')
        cvv = request.POST.get('cvv','')
        googlepay = request.POST.get('googlepay','')
        print(googlepay)
        dict = {
            'oid' : or_id,
            'amt' : txn_amt
        }
        dict1 = {
            'ORDER_ID': or_id,
            'TXN_AMOUNT': str(txn_amt)
        }
        upi_regex = r"^[A-Za-z0-9_.-]+@[A-Za-z]+\w*$"
        regex = "^5[1-5][0-9]{14}|^(222[1-9]|22[3-9]\\d|2[3-6]\\d{2}|27[0-1]\\d|2720)[0-9]{12}$"
        r = re.compile(regex)
        print(cardno)
        if cardno == "":
            if re.match(upi_regex, googlepay):
                return render(request, 'paytm.html', {'dict': dict})
            else:
                messages.warning(request, "Please enter a valid UPI Id")
                return render(request, 'gateway.html',{'dict1': dict1})
        elif cardno != "":
            if (re.search(r, cardno)):
                return render(request, 'paytm.html', {'dict': dict})
            elif re.search("^4[0-9]{12}(?:[0-9]{3})?$", cardno):
                return render(request, 'paytm.html', {'dict': dict})
            elif re.search("^3[47][0-9]{13}$", cardno):
                return render(request, 'paytm.html', {'dict': dict})
            else:
                messages.warning(request, "Please enter a valid Credit/Debit Card Number")
                return render(request, 'gateway.html',{'dict1': dict1})

        if cvv == "":
            return render(request, 'paytm.html', {'dict': dict})
        elif (re.search("^[0-9]{3, 4}$", cardno)):
            messages.warning(request, "Please enter a valid Credit/Debit Card CVV Number")
            return render(request, 'gateway.html',{'dict1': dict1})
            
        print(request.POST)
        print('1')
        
    
        return render(request,'paytm.html',{'dict':dict})
    
    # return render(request,'paytm.html',{'dict':dict})
    return render(request, 'paytm.html')

def pay(request):
    if request.method == "POST":
        status = request.POST.get('status', '')
        or_id = request.POST.get('id', '')
        txn_amt = request.POST.get('amt', '')
        print(or_id)
        print(request.POST)
        # Extract numeric part from or_id
        # numeric_part = ''.join(filter(str.isdigit, or_id))
        # rid = int(numeric_part) if numeric_part else 0  # Default value of 0 if no numeric part
        if status == "SUCCESS":
            html = "ordersuccessful.html"
            filter22 = Orders.objects.filter(or_id=or_id)
            for post12 in filter22:
                post12.oid = or_id
                post12.amountpaid = txn_amt
                post12.paymentstatus = status
                post12.update_desc = "The order has been placed"
                post12.save()

        elif status=="FAILURE":
            html = 'failuremail.html'
            filter13 = Orders.objects.filter(or_id=or_id)
            for post13 in filter13:
                post13.amountpaid = txn_amt
                post13.paymentstatus = status
                post13.update_desc = "The order has not been placed"
                post13.save()

            filter14 = OrderUpdate.objects.filter(or_id=or_id)
            for post14 in filter14:
                post14.update_desc = "The order has not been placed"
                post14.save()

        user=request.user.username
        items=Orders.objects.filter(email=user)
        list = ""
        for i in items:
            list = i.items_json
            print(list)

        date1 = date.today()

        email_subject="Order Details"
        message=render_to_string(html,{
            'user':user,
            'orderid': or_id,
            'date' : date1,
            'amt' : txn_amt,
            'list' : list          

        })
        send_mail(email_subject,message,settings.EMAIL_HOST_USER,[user])

        data = {
            'oid': or_id,
            'amt': txn_amt,
            'stats': status
        }
        return render(request, 'paymentstatus.html', {'data': data})

    return render(request,'paymentstatus.html')

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')
    currentuser=request.user.username
    print(currentuser)
    items=Orders.objects.filter(email=currentuser)
    print(items)
    myid=""

    
    # for i in items:
    #     # print(i.oid)
    #     # print(i.order_id)
    #     myid=i.or_id
    #     # print(myid)
    #     # rid=myid.replace("WeShopCart","")
    #     # print(rid)
    # status=OrderUpdate.objects.filter(email=currentuser)
    # print(status)
    # for j in status:
    #     print(j.update_desc)
  
    context ={"items":items}
    print(context)
    # print(currentuser)
    return render(request,"profile.html",context)


def terms(request):
    return render(request,'terms.html')

def privacy(request):
    return render(request,'privacy.html')

def service_detail(request, service_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request,"Login & Try Again")
            return redirect('/auth/login')
        try:
            service_id=request.POST.get('service_id')
            service = get_object_or_404(Services, service_id=service_id)
            
            appointment = ServiceAppointments.objects.create(
                user_id=request.user.id,
                service=service,  # This is now properly handled
                service_name=service.service_name,
                appointment_date=request.POST.get('appointment_date'),
                appointment_time=request.POST.get('appointment_time'),
                customer_name=request.POST.get('customer_name'),
                customer_email=request.POST.get('customer_email'),
                customer_phone=request.POST.get('customer_phone'),
                special_requests=request.POST.get('special_requests', '')
            )
            
            # Send email notification
            subject = f'Appointment Confirmation - {service.service_name}'
            message = render_to_string('email/appointment_confirmation.html', {
                'appointment': appointment,
                'service': service,
            })
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [appointment.customer_email],
                html_message=message,
            )
            
            messages.success(request, 'Appointment booked successfully! Check your email for confirmation.')
            
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')
            
        return redirect('service_detail', service_id=service_id)
    service = get_object_or_404(Services, service_id=service_id)
    services = Services.objects.all()
    return render(request, 'service_detail.html', {'service': service, 'services': services})

def book_appointment(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')
    if request.method == 'POST':
        try:
            service_id=request.POST.get('service_id')
            service = get_object_or_404(Services, service_id=service_id)
            
            appointment = ServiceAppointments.objects.create(
                user_id=request.user.id,
                service=service,  # This is now properly handled
                service_name=service.service_name,
                appointment_date=request.POST.get('appointment_date'),
                appointment_time=request.POST.get('appointment_time'),
                customer_name=request.POST.get('customer_name'),
                customer_email=request.POST.get('customer_email'),
                customer_phone=request.POST.get('customer_phone'),
                special_requests=request.POST.get('special_requests', '')
            )
            
            # Send email notification
            subject = f'Appointment Confirmation - {service.service_name}'
            message = render_to_string('email/appointment_confirmation.html', {
                'appointment': appointment,
                'service': service,
            })
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [appointment.customer_email],
                html_message=message,
            )
            
            messages.success(request, 'Appointment booked successfully! Check your email for confirmation.')
            
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')
            
        return redirect('service_detail', service_id=service_id)
    
    return redirect('service_detail', service_id=service_id)

def services_list(request):
    """View to display all available services"""
    services = Services.objects.all()
    return render(request, 'services.html', {'services': services})

def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)  # Changed from id to product_id
    return render(request, 'product_detail.html', {'product': product})


def product_api(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
        sizes = []
        if product.sizes_available:
            if isinstance(product.sizes_available, str):
                # If it's a string, split by comma and clean up
                sizes = [size.strip() for size in product.sizes_available.split(',') if size.strip()]
            elif isinstance(product.sizes_available, (list, tuple)):
                # If it's already a list/tuple
                sizes = list(product.sizes_available)
            else:
                # Default sizes if nothing else works
                sizes = ['S', 'M', 'L']

        data = {
            'id': product.product_id,
            'product_name': product.product_name,
            'price': str(product.price),
            'sale_price': str(product.sale_price) if product.sale_price else None,
            'discount_percentage': product.discount_percentage,
            'description': product.description,
            'main_image': str(product.main_image),
            'image_2': str(product.image_2) if product.image_2 else None,
            'image_3': str(product.image_3) if product.image_3 else None,
            'image_4': str(product.image_4) if product.image_4 else None,
            'fabric': product.fabric,
            'work_type': product.work_type,
            'stock': product.stock,
            'category': product.get_category_display(),
            'style': product.style,
            'occasion_type': product.occasion_type,
            'sizes_available': sizes,
            'custom_sizing_available': product.custom_sizing_available,
            # 'delivery_time': product.delivery_time,
            'alteration_available': product.alteration_available,
        }
        print("Sizes being sent:", sizes)  # Debug print
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


def mens(request):
    return render(request, 'mens.html')

def womens(request):
    return render(request, 'women.html')

def mens_collection(request):
    products = Product.objects.filter(category='GROOM').order_by('-created_at')
    context = {
        'products': products,
        'category_name': 'Groom Collection',
        'category_description': 'Explore our exclusive collection for the perfect groom'
    }
    return render(request, 'collection.html', context)

def womens_collection(request):
    products = Product.objects.filter(category='BRIDE').order_by('-created_at')
    context = {
        'products': products,
        'category_name': 'Bridal Collection',
        'category_description': 'Discover your dream wedding attire'
    }
    print("Products being sent:", products)  # Debug print
    return render(request, 'collection.html', context)

@login_required
@require_POST
def cart_add(request):
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        product = Product.objects.get(product_id=product_id)
        
        # Check if item already exists in cart
        cart_item, created = Cart.objects.get_or_create(
            user_id=request.user.id,
            product_id=product_id,
            defaults={
                'product_name': product.product_name,
                'price': product.price,
                'sale_price': product.sale_price,
                'quantity': quantity
            }
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        return JsonResponse(get_cart_data(request.user.id))
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_POST
def cart_remove(request):
    try:
        product_id = request.POST.get('product_id')
        Cart.objects.filter(user_id=request.user.id, product_id=product_id).delete()
        return JsonResponse(get_cart_data(request.user.id))
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_POST
def cart_update(request):
    try:
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        
        cart_item = Cart.objects.get(user_id=request.user.id, product_id=product_id)
        
        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
            
        return JsonResponse(get_cart_data(request.user.id))
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
@require_POST
def cart_clear(request):
    try:
        Cart.objects.filter(user_id=request.user.id).delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def cart_info(request):
    try:
        cart_data = get_cart_data(request.user.id)
        print("Cart data being sent:", cart_data)  # Debug print
        return JsonResponse(cart_data)
    except Exception as e:
        print("Error in cart_info:", str(e))  # Debug print
        return JsonResponse({
            'error': str(e),
            'total_items': 0,
            'items': [],
            'total_amount': 0
        })

def get_cart_data(user_id):
    try:
        cart_items = Cart.objects.filter(user_id=user_id)
        total_amount = sum(item.total_price for item in cart_items)
        
        data = {
            'total_items': cart_items.count(),
            'total_amount': float(total_amount),
            'items': [{
                'product_id': item.product_id,
                'product_name': item.product_name,
                'quantity': item.quantity,
                'price': float(item.price),
                'sale_price': float(item.sale_price) if item.sale_price else None,
                'total_price': float(item.total_price)
            } for item in cart_items]
        }
        return data
    except Exception as e:
        print("Error in get_cart_data:", str(e))
        raise