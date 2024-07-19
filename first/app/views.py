from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .form import signUp,ProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http  import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Home item class

class ProductView(View):
 def get(self,request):
  topwears=Product.objects.filter(category='TW')
  bottomwears=Product.objects.filter(category='BW')
  mobiles=Product.objects.filter(category='M')
  laptop=Product.objects.filter(category='L')
  return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,
                                         'mobiles':mobiles,'laptop':laptop})



@login_required()
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user,product=product).save()
 return redirect('/showcart')



def address(request):
 addres=Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'addres':addres})




def buy_now(request):
 return render(request, 'app/buynow.html')



def bottomwear(request):
 bottom = Product.objects.filter(category='BW')
 return render(request, 'app/bottomwear.html',{'bottom': bottom})




def checkout(request):
 user=request.user
 add=Customer.objects.filter(user=user)
 items=Cart.objects.filter(user=user)
 amount = 0.0
 totalamount=0.0
 shipping_amount = 70.0
 cart_product = [p for p in Cart.objects.all() if
                 p.user == request.user]  # provide the list off all items stored in cart database
 if cart_product:
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
  totalamount=amount+shipping_amount
 return render(request, 'app/checkout.html',{'add':add, 'total':totalamount, 'items':items})




def laptop(request ,company=None):
 if company == None:
  laptop = Product.objects.filter(category='L')
 elif company=='Hp' or company=='Dell' or company=='Apple':
  laptop=Product.objects.filter(category='L').filter(brand=company)
 return render(request,'app/laptop.html',{'laptop':laptop})





def minus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]  # provide the list off all items stored in cart database
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
   data = {
    'quantity': c.quantity,
    'amount': amount,
    'totalamount': amount + shipping_amount
   }
   return  JsonResponse(data)




def mobile(request,data=None):
 if data ==None:
     mobiles=Product.objects.filter(category='M')
 elif data=='Vivo' or data=='Samsung' or data=='Iphone':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
   mobiles = Product.objects.filter(category='M').filter( discounted_price__lt=2500)
 elif data == 'above':
   mobiles = Product.objects.filter(category='M').filter( discounted_price__gt=2500)
 return render(request, 'app/mobile.html',{'mobiles':mobiles})





def orders(request):
 order=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order':order})




# click on item and show detail
class ProductDetailView(View):
 def get(self,request,pk):
  product=Product.objects.get(pk=pk)
  already_cart=False
  if request.user.is_authenticated:
   already_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request,'app/productdetail.html',{'product':product,'already':already_cart})




def profile(request):
 if request.method=='POST':
   fm=ProfileForm(request.POST)
   if fm.is_valid():
    fm.save()
 fm=ProfileForm()
 return render(request, 'app/profile.html',{'form':fm})




def plus_cart(request):
 if request.method=='GET':
  prod_id=request.GET['prod_id']
  c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user ==request.user]  # provide the list off all items stored in cart database
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
   data = {
    'quantity': c.quantity,
    'amount': amount,
    'totalamount': amount + shipping_amount
   }
   return  JsonResponse(data)





def payment_done(request):
 user=request.user
 custid=request.GET.get('custid')
 customer=Customer.objects.get(id=custid)
 cart=Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
  c.delete()
 return redirect("orders")





def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  user = request.user
  try:
   cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=user))
   cart_item.delete()

   amount = 0.0
   shipping_amount = 70.0
   cart_products = Cart.objects.filter(user=user)
   for p in cart_products:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount

   data = {
    'amount': amount,
    'totalamount': amount + shipping_amount,
    'empty_cart': cart_products.count() == 0
   }
   return JsonResponse(data)
  except Cart.DoesNotExist:
   return JsonResponse({'error': 'Item does not exist in cart'}, status=404)





def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)  # Query set of all items stored in the cart database
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]  # List of all items stored in the cart database
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shipping_amount
  return render(request, 'app/addtocart.html',
                 {'carts': cart, 'total': total_amount, 'ship': shipping_amount, 'amount': amount})




def sign_up(request):
 if request.method == 'POST':
  fm =signUp(request.POST)
  if fm.is_valid():
   # messages.success(request,'Congratulations! Account create Succefully')
   fm.save()
 fm = signUp()
 return render(request, 'app/customerregistration.html', {'form':fm})





def topwear(request):
 top=Product.objects.filter(category='TW')
 return render(request,'app/topwear.html',{'top':top})
