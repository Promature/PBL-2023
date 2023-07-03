from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from myApp.models import *
import json
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

#admin admin@gmail.com Admin@36#3
# Create your views here.
def base(request):
    return render(request, "base.html")

def index(request):
    productCount = bookView.objects.all().count()
    products = bookView.objects.order_by('?').all()
    
    if request.method=="GET":
        key = request.GET.get('searchctg')
        if key != None:
            return searchProd(request)
    data = {
        "title":"Home", 'product':products, 'productCnt':productCount,
        'allProduct':products
    }
    return render(request,"index.html",data)

def loginUser(request):
    data = {
        "title":"Login"
    }
    if request.method=="POST":
        # name = request.POST.get('username')
        mail = request.POST.get('email')
        pwd = request.POST.get('password')

        user = authenticate( email = mail, password = pwd)

        if user is not None:
            #backend authenticate
            login(request, user)
            return redirect('/')
        
        else:
            messages.warning(request, "Inavalid credentials!!")
            return render(request,"login.html",data)
    return render(request,"login.html",data)

def logoutUser(request):
    data = {
        "title":"Logout"
    }
    
    logout(request)
    messages.success(request, "You have been loged out succesfully.")
    return redirect("/")


def signupUser(request):
    data = {
        "title":"Signup"
    }
    if request.method == "POST":
        #get post parameters
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #check for empty fields & faulty fields
        if not name.isalnum():
            messages.warning(request, "Username must be alphanumeric.")
            return redirect("/login")
        
        #unique username
        for i in User.objects.all():
            if i.username==name:
                messages.warning(request, "Cannot create user - Username already exists")
                return redirect("/login")

          #unique email  
        for i in User.objects.all():
            if i.email==email:
                messages.warning(request, "Cannot create user - Email already exists")
                return redirect("/login")

            
        
        if not fname.isalpha() or not lname.isalpha():
            messages.warning(request, "First name and last name must contain only alphabets")
            return redirect("/login")
        
        
        # obj = SignupUser(name = name,email = email, password = password)
        #create user
        user = User.objects.create_user(email, password)
        user.first_name = fname
        user.last_name = lname
        user.name = name
        user.mobile = mobile
        user.area_live = address
        user.save()
        messages.success(request,"User successfully created")
        # obj.save()
        return redirect('Login')
    else:
        return HttpResponse('404-Not Found')
    

def bookview(request, bookname):
    products = bookView.objects.get(name = bookname)
    area = products.sold_by.all()[0].area_live
    ownerF = products.sold_by.all()[0].first_name
    ownerL = products.sold_by.all()[0].last_name
    params = {'product':products, 'area':area, 'ownerName':ownerF+" "+ownerL}
    
    return render(request,"bookview.html",params)

def searchProd(request):
    productCount = bookView.objects.all().count()
    products = bookView.objects.all()

    if request.method=="GET":
        fltProd = request.GET.get('searchctg')
        if fltProd != None:
            products = bookView.objects.filter(name__icontains=fltProd)

    data = {
        "title":"Home", 'product':products[productCount-3:], 'productCnt':productCount,
        'allProduct':products
    }
    return render(request,"searchProd.html", data)

def sellbook(request):
    if request.user.is_anonymous:
        messages.warning(request, "Kindly login")
        return redirect("/login")
     
    if request.method == "POST":
        name = request.POST.get('bname')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        pub_date = request.POST.get('pub_date')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        bimage = request.FILES.get('bimg')
        time_used = request.POST.get('time-used')
        #currently active user
        user = request.user
        # Create a new book object
    
        obj = bookView(name=name,author=author,bookimage =bimage,genre = genre ,pub_date=pub_date,price=price, desc = desc, time_used = time_used)
        obj.save()
        # Add the new book to the 'books_sold' field of the currently active user
        user.books_sold.add(obj)
        messages.success(request,"Book added successfully.")
        return render(request,'sellbook.html')
    return render(request,'sellbook.html')

def profile(request):
    if request.user.is_anonymous:
        messages.warning(request, "Kindly login to view profile-page")
        return redirect("/login")
    
    data = {
        'bought_books':request.user.books_bought.all(),
        'sold_books':request.user.books_sold.all()
    }
    return render(request,'profile.html',data)

def cover(request):
    return render(request,"cover.html")

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        messages.warning(request, "Kindly login to proceed.")
        return redirect("/login")
    products = bookView.objects.all()
    context = {'products':products, 'cartItems':cartItems}

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        # orders = Order.objects.filter(customer=customer, complete=False)
        # items = []
        orders, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = orders.orderitem_set.all()
        #total number products purchased
        item_count=0
        item_count = orders.get_cart_items
        
        # for order in orders:
        #     items += list(orders.orderitem_set.all())

        #overall product price total
        total = 0
        for item in items:
            total += item.product.price
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        messages.warning(request, "Kindly login to proceed.")
        return redirect("/login")  
    
    context = {'items':items, 'total':total, 'item_count':item_count, 'order':orders}
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = int(data['productId']) 
    action = data['action']
    print('Action:', action)
    print('Product:',productId)

    customer = request.user.customer
    product = bookView.objects.get(id = productId)
   # Retrieve the most recent incomplete order for the customer
    order = Order.objects.get(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order= order, product = product)
    orderItem.save()
    messages.success(request, "message: Item added to cart.")
    return JsonResponse({'message': 'Item added to cart.'})

def save_shipping_address(request):
    if request.method == 'POST':
        # Assuming the request body is in JSON format
        data = json.loads(request.body)
        firstName= data.get('firstName')
        lastName= data.get('lastName')
        email= data.get('email')
        address = data.get('address')
        city = data.get('city')
        state = data.get('state')
        zip = data.get('zip')

        # Save the shipping address
        customer=request.user.customer
        currOrder = Order.objects.get(customer=customer, complete =False)
        shipping_address = ShippingAddress(
            customer=request.user.customer,
            order = currOrder,
            address=address,
            city=city,
            state=state,
            zipcode=zip
        )
        shipping_address.save()
        #add books bought
        books = currOrder.orderitem_set.values_list('product', flat=True)
        user = request.user
        user.books_bought.add(*books)

        # Get book details for the email message
        book_details = []
        for book_item in currOrder.orderitem_set.all():
            book = book_item.product
            owner = book.sold_by.first()  # Assuming there is only one owner for a book
            book_details.append({
                'name': book.name,
                'owner_name': owner.first_name+" "+owner.last_name,
                'owner_mobile': owner.mobile,
                'owner_email': owner.email
            })

        
        #update your current order status
        currOrder.complete = True
        currOrder.save()
        messages.success(request, "message: Your order has been placed successfully. Check email for further details.")
        #send email to customer
        subject = "Order Placed!"
        details = ""
        for i in book_details:
            details += i['name']+"   "+i['owner_name']+"   "+i['owner_mobile']+"   "+i['owner_email']+"\n"

        message = "Hello "+firstName+" "+lastName+" Thanks for using SecondChanceBooks.\nHere are your order details:\n|  BookTitle  |  Owner  |  Mobile  |  Email  |\n"+details
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
       
        #Return a JSON response32
        
        return JsonResponse({'message': 'Shipping address saved successfully'})

    return JsonResponse({'message': 'Invalid request method'}, status=400)