from django.shortcuts import render,redirect
from ecommerceapp.models import Contact,Product,OrderUpdate,Orders
from django.contrib import messages
from math import ceil
from ecommerceapp import keys
from django.conf import settings
MERCHANT_KEY=keys.MK
import json
from django.views.decorators.csrf import  csrf_exempt
from PayTm import Checksum
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from authshop.utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
from datetime import date
import json
import re
# from models import Orders
#from PayTm import Checksum
# Create your views here.

def index(request):
    allProds = []
    catprods = Product.objects.values('category','id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}

    return render(request,"index.html",params)
    #return render(request,"index.html")

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
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        item =""
        
        # json_string = '{"pr6":[1,"APPLE iPhone 13","59999"]}'

        # Parse the JSON string into a Python dictionary
        data = json.loads(items_json)

        # Iterate through all key-value pairs in the dictionary
        for key, value in data.items():
            identifier = value[0] if isinstance(value, list) and len(value) > 0 else None
            name1 = value[1] if isinstance(value, list) and len(value) > 1 else None
            price = value[2] if isinstance(value, list) and len(value) > 2 else None

            print(f"Key: {key}")
            print(f"Identifier: {identifier}")
            print(f"Name: {name1}")
            item = name1
            print(f"Price: {price}")

        Order = Orders(items_json=item,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="The order has been placed")
        update.save()
        id = Order.order_id
        oid=str(id)+"WeShopCart"
        
        print(amount)
        filter2 = Orders.objects.filter(order_id=Order.order_id)
        
        for post1 in filter2:
            post1.oid = oid
            post1.or_id = oid
            post1.save()

        filter3 = OrderUpdate.objects.filter(order_id=Order.order_id)
        
        for post3 in filter3:
            post3.or_id = oid
            post3.email = email
            post3.save()
        
        thank = True
        # id = Order.order_id
        # oid=str(id)+"WeShopCart"
        # Order = Orders(or_id=oid)
        # Order.save()
        dict1 = {
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount)
        }
 #PAYMENT INTEGRATION

        # id = Order.order_id
        # oid=str(id)+"ShopyCart"
        # param_dict = {

        #     'MID':keys.MID,
        #     'ORDER_ID': oid,
        #     'TXN_AMOUNT': str(amount),
        #     'CUST_ID': email,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID': 'WEB',
        #     'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'gateway.html',{'dict1':dict1})
    
        
    return render(request, 'checkout.html')


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
    items=Orders.objects.filter(email=currentuser)
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
    # print(currentuser)
    return render(request,"profile.html",context)


def terms(request):
    return render(request,'terms.html')

def privacy(request):
    return render(request,'privacy.html')