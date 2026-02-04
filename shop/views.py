from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
import json
from .form import CustomUserForm
from.models import*
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
#request the homepage
def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,'index.html',{"products":products})


def cart_pages(request):
    if request .user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'cart.html',{'cart':cart})
    else:
        return redirect("/")
    

def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
        return redirect("/")
    

def addtocard(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            # print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status : Product Already to Card'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Card'},status=200)
                    else:
                        return JsonResponse({'status':'Product Stock Not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Card'},status=200)

    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)
    

def fav_pages(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        if request.user.is_authenticated:

            data = json.loads(request.body)
            product_id = data.get('pid')

            product = Product.objects.filter(id=product_id).first()
            if not product:
                return JsonResponse({'status': 'Product not found'}, status=404)

            if Favourite.objects.filter(user=request.user, product=product).exists():
                return JsonResponse({'status': 'Product Already in Favourite'}, status=200)
            else:
                Favourite.objects.create(user=request.user, product=product)
                return JsonResponse({'status': 'Product Added to Favourite'}, status=200)

        else:
            return JsonResponse({'status': 'Login to Add Favourite'}, status=401)

    return JsonResponse({'status': 'Invalid Access'}, status=400)




def favviewpage(request):
    if request .user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        return render(request,'fav.html',{'fav':fav})
    else:
        return redirect("/")
    

def delete_fav(request,fid):
    item = get_object_or_404(Favourite, id=fid, user=request.user)
    item.delete()
    return redirect("/favviewpage")


#request the login
def login_page(request):

    # If already logged in → go home
    if request.user.is_authenticated:
        return redirect("/")

    # If form submitted
    if request.method == 'POST':
        name = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(request, username=name, password=pwd)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in Successfully')
            return redirect("/")
        else:
            messages.error(request, "Invalid Username or Password")

    # For GET request → show login page
    return render(request, 'login.html')



#request the register page
def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration are Success You can login Now!")
            return redirect('/login')
    return render(request,'register.html',{'form':form})



#requesting the collecting page
def collection(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request, 'collection.html',{"catagory":catagory})



#reqesting the products pages
def collectionview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(catagory__name=name)
        return render(request, 'products/index.html',{"products":products,"catagory_name":name})
    else:
        messages.warning(request,"No such Catagory Found")
        return redirect('collection')
    

    
def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"products/products_details.html",{"products":products})
        else:
            messages.error(request,"no Such Category Found")
            return redirect('collection')
    else:
            messages.error(request,"no Such Category Found")
            return redirect('collection')


@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    total = 0
    for item in cart_items:
        total += item.product.selling_price * item.product_qty

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.product_qty,
            price=item.product.selling_price
        )

    cart_items.delete()   # clear cart

    return redirect('my_orders')



@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'my_orders.html', {'orders': orders})


    
