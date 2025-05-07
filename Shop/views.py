from django.shortcuts import render,redirect
from django.http import HttpResponse, request
#from PayTm import Checksum
from .models import Book,Contact,Orders,OrderUpdate
from django.contrib.auth.models import User
from django.contrib import messages
import json
from math import ceil
from django.contrib.auth import authenticate,login,logout
#from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import razorpay
#MERCHANT_KEY = '0lZBMF6FcEim!sgV'

def Index(request):
    #params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
    allproduct=[]
    category_of_books=Book.objects.values('category','id')
    items_in_category={item["category"] for item in category_of_books}
    for categories in items_in_category:
        products = Book.objects.filter(category=categories)
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) + (n // 4))
        allproduct.append([products,range(1,nSlides),nSlides])
    params={'allproduct':allproduct}
    return render(request, "Shop/index.html",params)

#matching the text of search
def searchMatch(query,item):
    query_lower=query.lower()
    if query_lower in item.desc or query_lower in item.book_name or query_lower in item.category or query_lower in item.desc.lower() or query_lower in item.book_name.lower() or query_lower in item.category.lower() or query_lower in item.desc.upper() or query_lower in item.book_name.upper() or query_lower in item.category.upper() :
        return True
    else:
        return False

#Search logic is created here

def Search(request):
    query=request.GET.get("search")
    allproduct = []
    category_of_books = Book.objects.values('category', 'id')
    items_in_category = {item["category"] for item in category_of_books}
    for categories in items_in_category:
        products_Cat = Book.objects.filter(category=categories)
        products=[item for item in products_Cat if searchMatch(query,item)]
        n = len(products)
        nSlides = n // 4 + ceil((n / 4) + (n // 4))
        if len(products)!=0:
            allproduct.append([products, range(1, nSlides), nSlides])
    params = {'allproduct': allproduct,"msg":""}
    if len(allproduct) == 0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search Query"}
    return render(request,'Shop/search.html',params)

# Create your views here.
def About(request):
    return render(request,"Shop/about.html")
def Tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json},default = str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error" }')

    return render(request,"Shop/tracker.html")


def Checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        amount= request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address=request.POST.get('address1','')+ " "+request.POST.get('address2','')
        city=request.POST.get('city','')
        zip_code=request.POST.get('zip_code','')
        state=request.POST.get('state','')
        orders= Orders(name=name,items_json=items_json, email=email, phone=phone, address=address, city=city, zip_code=zip_code, state=state,amount=amount)
        orders.save()
        update = OrderUpdate(order_id=orders.order_id, update_desc="The order has been placed")
        update.save()
        clear_cart_after_placing_orders= True
        id = orders.order_id
        return render(request, "Shop/checkout.html", {"clear_cart_after_placing_orders":clear_cart_after_placing_orders,'id':id})

        '''param_dict = {
            'MID': 'NFAIem42744345843154',
            'ORDER_ID': str(Orders.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request, 'Shop/paytm.html', {'param_dict': param_dict})'''
    return render(request, 'Shop/checkout.html')


    #razor_pay_key_id = 'rzp_test_DcNOFoHEMNkTyJ'
    #key_secret = 'CIVeRYWCLhRjnmdKfJpjBPPx'
    #client = razorpay.Client(auth=(razor_pay_key_id, key_secret))
    #payment= client.order.create({'amount':Orders.amount ,'currency':'INR','payment_capture':1})

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

    # validation for contact form
        if len(phone)!=10:
            messages.error(request,"Please Enter a Valid Phone Number")
            return redirect("/shop/contact")
        if not phone.isnumeric():
            messages.error(request,"Please Enter Numbers Only in Phone Number")
            return redirect("/shop/contact")
        if not name.isalpha():
            messages.error(request,"Please Enter Alphabet Only in Name")
            return redirect("/shop/contact")
        if len(desc)<30:
            messages.error(request,"Please Elobrate More To Know Your Problem")
            return redirect("/shop/contact")
# save the compliment here
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        contact_submitted = True
        return render(request, "Shop/contact.html",{"contact_submitted":contact_submitted})
    return render(request,'Shop/contact.html')
def BookView(request,myid):
    book=Book.objects.filter(id=myid)
    return render(request,"Shop/bookview.html",{"book":book[0]})

#payment gateway
'''@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})'''

def handleSignUp(request):
    # get the post parameter from user
    if request.method == "POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname = request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        #validation for singup form
        if len(username)<10:
            messages.error(request,"! Username is too short !")
            return redirect('/shop')
        if  username.isnumeric():
            messages.error(request, "! Username must be combination of alphabet and numbers  !")
            return redirect('/shop')
        if username.isalpha():
            messages.error(request, "! Username must be combination of alphabet and numbers  !")
            return redirect('/shop')
        if pass1!=pass2:
            messages.error(request,"! The password was not match 2nd time !")
            return redirect('/shop')
        # Create the user
        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your Book BAZAAR Account has been created Successfully")
        return redirect('/shop')
    else:
        return render(request,"Shop/signup.html")

#function that handle login activities
def handleLogin(request):
    if request.method == "POST":
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpass']

        user= authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,"Sucessfully Logged In")
            return redirect('/shop')
        else:
            messages.error(request,"Invalid Credentials Please try again")
            return redirect('/shop')
    else:
        return HttpResponse('404 Page not found..')

#function that handle Logout activities
def handleLogout(request):
    logout(request)
    messages.success(request, "Sucessfully Logged Out")
    return redirect('/shop')
def paytm(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        zip_code = request.POST.get('zip_code', '')
        state = request.POST.get('state', '')
        orders = Orders(name=name, items_json=items_json, email=email, phone=phone, address=address, city=city,zip_code=zip_code, state=state, amount=amount)
        orders.save()
        update = OrderUpdate(order_id=orders.order_id, update_desc="The order has been placed")
        update.save()
        clear_cart_after_placing_orders =True
        id = orders.order_id
        return render(request,"Shop/paytm.html", {"clear_cart_after_placing_orders":clear_cart_after_placing_orders,'id':id})
    return render(request,"Shop/paytm.html")