from .models import Product, Order, OrderDetails,Customer,Payment
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse 
from django.contrib.auth.models import User
from django.contrib import messages,auth
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import auth
import requests
import json
import re




def index(request):
    context = {}
    return render(request, 'ecommerce/index.html', context)


def signup(request):
    if request.method == 'POST':
        # تعريف المتغيرات
        fname = lname = address1 = address2 = city = state = zip_code = email = username = password = terms = confirm_password = is_added = phone = None

        # التحقق من وجود البيانات في الطلب
        if 'fname' in request.POST:
            fname = request.POST['fname']
        else:
            messages.error(request, 'Error In First Name')

        if 'lname' in request.POST:
            lname = request.POST['lname']
        else:
            messages.error(request, 'Error In Last Name')

        if 'address1' in request.POST:
            address1 = request.POST['address1']
        else:
            messages.error(request, 'Error In Address1')

        if 'address2' in request.POST:
            address2 = request.POST['address2']
        else:
            messages.error(request, 'Error In Address2')

        if 'city' in request.POST:
            city = request.POST['city']
        else:
            messages.error(request, 'Error In City')

        if 'state' in request.POST:
            state = request.POST['state']
        else:
            messages.error(request, 'Error In State')

        if 'zip_code' in request.POST:
            zip_code = request.POST['zip_code']
        else:
            messages.error(request, 'Error In Zipcode')

        if 'email' in request.POST:
            email = request.POST['email']
        else:
            messages.error(request, 'Error In Email')

        if 'username' in request.POST:
            username = request.POST['username']
        else:
            messages.error(request, 'Error In Username')

        if 'password' in request.POST:
            password = request.POST['password']
        else:
            messages.error(request, 'Error In Password')

        if 'confirm_password' in request.POST:
            confirm_password = request.POST['confirm_password']
        else:
            messages.error(request, 'Error In Confirm Password')

        if 'phone' in request.POST:
            phone = request.POST['phone']    

        if 'terms' in request.POST:
            terms = request.POST['terms']
        else:
            messages.error(request, 'Error In Phone')

        # التحقق من القيم وتحقق من الموافقة على الشروط
        if fname and lname and address1 and address2 and city and state and zip_code and email and username and phone and confirm_password:
            if terms == 'on':
                if password and confirm_password:
                    if password != confirm_password:
                        messages.error(request, 'كلمة المرور وتأكيدها غير متطابقين')
                        return render(request, 'users/signup.html', {
                            'fname': fname,
                            'lname': lname,
                            'address1': address1,
                            'address2': address2,
                            'city': city,
                            'state': state,
                            'zip_code': zip_code,
                            'email': email,
                            'username': username,
                            'password': password,
                            'phone' : phone,
                        })
                # التحقق من إذا كان اسم المستخدم موجودًا
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'هذ الاسم مستخدم من قبل')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'هذا البريد مستخدم من قبل')
                    else:
                        pattern = r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(pattern, email):
                            user = User.objects.create_user(
                                first_name=fname,
                                last_name=lname,
                                username=username,
                                email=email,
                                password=password,
                            )
                            user.save()
                            customer = Customer(
                                user=user,
                                address1=address1,
                                address2=address2,
                                city=city,
                                state=state,
                                zip_code=zip_code,
                                phone=phone,
                            )
                            customer.save()
                            #تنظيف المدخلات بعد التسجيل
                            fname = ''
                            lname = ''
                            username = ''
                            email = '' 
                            password = ''
                            address1 = ''
                            address2 = ''
                            city = ''
                            state = ''
                            zip_code = ''
                            phone = ''
                            messages.success(request, 'تم التسجيل بنجاح')
                            return redirect('login')
                            #لأخفاء النموزج بعد التسجيل 
                            is_added = True
                        else:
                            messages.error(request, 'تحقق من لأيميل')
            else:
                messages.error(request, 'يجب الموافقة على الشروط ')
        else:
            messages.error(request, 'تأكد من المدخلات')

        return render(request, 'users/signup.html', {
            'fname': fname,
            'lname': lname,
            'address1': address1,
            'address2': address2,
            'city': city,
            'state': state,
            'zip_code': zip_code,
            'email': email,
            'username': username,
            'password': password,
            'phone' : phone,
            'is_added': is_added,
        })

    else:
      return render(request, 'users/signup.html',{'title':'SignUp'})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  # تصحيح المفتاح هنا
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if 'rememberme' in request.POST:
                # إذا كان قد اختار "تذكرني"، جعل الجلسة تستمر لمدة أطول (مثال: 30 يومًا)
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 يومًا
            else:
                # إذا لم يختار "تذكرني"، يتم ضبط الجلسة لتنتهي عند غلق المتصفح
                request.session.set_expiry(0)
            auth.login(request, user)
            return redirect('index')  # التوجيه لصفحة أخرى بعد تسجيل الدخول بنجاح
        else:
            messages.error(request, 'تأكد من اسم المستخدم أو كلمة المرور.')
            return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html',{'title':'Login'})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')    


def product1(request):
    products = Product.objects.all()
    context = {'products': products, 'title': 'product1'}
    return render(request, 'ecommerce/product1.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # جلب المنتج بناءً على معرفه
    return render(request, 'ecommerce/product_detail.html', {'product': product})


def search_view(request):

    return render(request, 'ecommerce/search.html' ,{'title':'Search'})


def search_results(request):
    name = request.GET.get('name', '')
    description = request.GET.get('description', '')
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    price = request.GET.get('price', None)

    # بدءًا بجلب جميع المنتجات
    products = Product.objects.all()

    # فلترة حسب الاسم
    if name:
        products = products.filter(name__icontains=name)

    # فلترة حسب الوصف
    if description:
        products = products.filter(description__icontains=description)

    # فلترة حسب الحد الأدنى للسعر
    if min_price:
        try:
            min_price = float(min_price)
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass  # إذا كانت القيمة غير صالحة يتم تجاهل الفلتر 

    # فلترة حسب الحد الأقصى للسعر
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass  # إذا كانت القيمة غير صالحة يتم تجاهل الفلتر 

    # فلترة حسب السعر الفردي
    if price:
        try:
            price = float(price)
            products = products.filter(price=price)
        except ValueError:
            pass  # إذا كانت القيمة غير صالحة يتم تجاهل الفلتر

    context = {
        'products': products,
        'title': 'SearchResults'
    }
    return render(request, 'ecommerce/search_results.html', context)


    if request.method == 'POST' and 'btnsave' in request.POST:
        if request.user is not None and request.user.id is not None:
            customer = Customer.objects.get(user=request.user)

            # جلب القيم من الطلب POST
            fname = request.POST.get('fname', '').strip()
            lname = request.POST.get('lname', '').strip()
            email = request.POST.get('email', '').strip()
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            address1 = request.POST.get('address1', '').strip()
            address2 = request.POST.get('address2', '').strip()
            city = request.POST.get('city', '').strip()
            state = request.POST.get('state', '').strip()
            zip_code = request.POST.get('zip_code', '').strip()

            if fname and lname and email and username and password and address1 and address2 and city and state and zip_code:
                # تحديث بيانات المستخدم
                request.user.first_name = fname
                request.user.last_name = lname
                request.user.username = username
                request.user.email = email

                # تحديث كلمة المرور إذا تغيرت
                if not password.startswith('pbkdf2_sha256$'):
                    request.user.set_password(password)

                request.user.save()

                # تحديث بيانات العميل
                customer.address1 = address1
                customer.address2 = address2
                customer.city = city
                customer.state = state
                customer.zip_code = zip_code
                customer.save()

                # إعادة تسجيل الدخول في حالة تغيير كلمة المرور
                auth.login(request, request.user)

                messages.success(request, 'تم تحديث البيانات بنجاح')
            else:
                messages.error(request, 'تأكد من صحة المدخلات.')
        else:
            messages.error(request, 'المستخدم غير موجود.')

        return redirect('profile')

    else:
        if request.user is not None:
            customer = Customer.objects.get(user=request.user)

            # جلب القيم الحالية
            context = {
                'fname': request.user.first_name,
                'lname': request.user.last_name,
                'username': request.user.username,
                'email': request.user.email,
                'password': request.user.password,
                'address1': customer.address1,
                'address2': customer.address2,
                'city': customer.city,
                'state': customer.state,
                'zip_code': customer.zip_code,
            }
            return render(request, 'users/profile.html', context)
        else:
            return redirect('login')


def profile(request):
    if request.method == 'POST' and 'btnsave' in request.POST:
        if request.user is not None and request.user.id is not None:
            customer = Customer.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname']  and request.POST['email']  and request.POST['username'] and request.POST['password'] and  request.POST['address1'] and request.POST['phone']  and request.POST['address2'] and request.POST['city'] and request.POST['state'] and request.POST['zip_code']:
                request.user.first_name = request.POST['fname']
                request.user.last_name = request.POST['lname']
                request.user.username = request.POST['username']
                # request.user.email = request.POST['email']
                customer.address1 = request.POST['address1']
                customer.address2 = request.POST['address2']
                customer.city = request.POST['city']
                customer.state = request.POST['state']
                customer.zip_code = request.POST['zip_code']
                customer.phone = request.POST['phone']

                if not request.POST['password'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['password'])
                request.user.save()
                customer.save()
        
                auth.login(request, request.user)
                messages.success(request, 'تم تغير البينات بنجاح')
            else:
                messages.error(request, 'تاكد من المدخلات')
        return redirect('profile_view')
    else:
        if request.user is not None:
            customer = Customer.objects.get(user=request.user)
            address1 = customer.address1
            address2 = customer.address2
            city = customer.city
            state = customer.state
            zip_code = customer.zip_code
            phone = customer.phone

            fname = request.user.first_name
            lname = request.user.last_name
            username = request.user.username
            email = request.user.email
            password = request.user.password
            phone = customer.phone

            context = {
                'fname': fname,
                'lname': lname,
                'username': username,
                'email': email,
                'password': password,
                'phone' : phone,
                'address1': address1,
                'address2': address2,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'phone' : phone,
                'title': 'Change A Profile'
            }
            return render(request, 'users/profile.html', context)
        else:
            return redirect('login')


def profile_view(request):
    context = {
        'title':'YourProfile'
    }

    return render(request, 'users/profile_view.html', context)


def product_favorites(request, pk):
    if request.user.is_authenticated and not request.user.is_anonymous:
        # جلب المنتج أو عرض خطأ إذا لم يكن موجودًا
        product_favorites = get_object_or_404(Product, pk=pk)

        # التحقق إذا كان المنتج موجودًا بالفعل في المفضلة
        customer = get_object_or_404(Customer, user=request.user)
        if customer.product_favorites.filter(pk=product_favorites.pk).exists():
            messages.success(request, 'هذا المنتج مضاف مسبقًا إلى المفضلة.')
        else:
            customer.product_favorites.add(product_favorites)
            messages.success(request, 'تم إضافة المنتج إلى المفضلة بنجاح.')

        # توجيه إلى صفحة تفاصيل المنتج
        return redirect('product_detail', pk=pk)
    else:
        # إذا لم يكن المستخدم مسجل الدخول
        messages.error(request, 'يجب تسجيل الدخول لاستخدام هذه الخاصية.')
        return redirect('login')  # تأكد من اسم نمط تسجيل الدخول الصحيح


def show_product_favorites(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        customer = Customer.objects.get(user=request.user)
        favorite_products = customer.product_favorites.all()
        context = {
        'favorite_products':favorite_products
        }
    return render(request, 'ecommerce/show_product_favorites.html', context)    


def add_to_cart(request):
    if request.user.is_authenticated:
        product_id = request.GET.get('product_id')
        quantity = request.GET.get('quantity')
        price = request.GET.get('price')

        # التحقق من المدخلات
        if product_id and quantity and price:
            product = Product.objects.get(id=product_id)
        else:
            messages.error(request, 'هذا المنتج غير متاح')
            return redirect('product_degital')    

        # الحصول على الطلب الحالي أو إنشاء طلب جديد
        order = Order.objects.filter(user=request.user, complete=False).first()
        if not order:
            order = Order.objects.create(
                user=request.user,
                ordered_date=timezone.now(),
                complete=False
            )
            messages.success(request, 'تم إنشاء طلب جديد.')

        # التحقق من وجود المنتج في تفاصيل الطلب
        order_detail = OrderDetails.objects.filter(order=order, product=product).first()
        if order_detail:
            # تحديث الكمية فقط إذا كان المنتج موجودًا
            order_detail.quantity += int(quantity)
            order_detail.save()
            messages.success(request, f"تم تحديث كمية المنتج {product.name} في الطلب.")
        else:
            # إضافة منتج جديد إلى تفاصيل الطلب
            OrderDetails.objects.create(
                product=product,
                price=float(price),
                order=order,
                quantity=int(quantity)
            )
            messages.success(request, f"تمت إضافة {product.name} إلى الطلب.")

        return redirect('/product1/' + str(product_id))
    else:
        messages.error(request, 'يجب أن تسجل الدخول لتتمكن من شراء المنتجات.')
        return redirect('login')


def cart(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.filter(user=request.user, complete=False).exists():
            order = Order.objects.get(user=request.user, complete=False)
            orderdetails = OrderDetails.objects.filter(order=order)
            total = 0
            for sup in orderdetails:
                total += sup.price * sup.quantity
            context = {
                'order': order,
                'orderdetails': orderdetails,
                'total': total,
            }
            return render(request, 'ecommerce/cart.html', context)
    return render(request, 'ecommerce/cart.html')


def remove_from_cart(request,pk):
    if request.user.is_authenticated and not request.user.is_anonymous:
        orderdetails = OrderDetails.objects.get(pk=pk)
        # بتاكد ان المستخدم المسجل الدخول هوا الي يقدر يحذف منتجاتو فقط وميقدرش يحذف منتجات شخص اخر
        if orderdetails.order.user == request.user:
           orderdetails.delete()
    return redirect('cart')  


def update_cart_quantity(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            action = request.POST.get('action')
            if action:
                orderdetails = get_object_or_404(OrderDetails, pk=pk)
                if action == 'increase':
                    orderdetails.quantity += 1
                elif action == 'decrease' and orderdetails.quantity > 1:
                    orderdetails.quantity -= 1
                orderdetails.save()
                messages.success(request, f'Quantity updated successfully!')
    return redirect('cart')             



def payment(request):
    # تعيين القيم الافتراضية
    context = None
    ship_address = None
    ship_phone = None
    card_number = None
    card_expire = None
    security_code = None
    is_added = False

    # التحقق من وجود الحقول المطلوبة في الطلب
    if request.method == 'POST' and all(field in request.POST for field in ['payment', 'card_number', 'card_expire', 'security_code', 'ship_phone', 'ship_address']):
        print(request.POST)  # تأكد من الحقول المرسلة

        # استخراج الحقول من الطلب
        ship_address = request.POST.get('ship_address')
        ship_phone = request.POST.get('ship_phone')
        card_number = request.POST.get('card_number')
                
        # استخراج وتنسيق تاريخ انتهاء البطاقة
        card_expire = request.POST.get('card_expire')

        # تحقق من التنسيق: MM/YY أو MM/YYYY
        if len(card_expire) == 7:  # إذا كان التنسيق هو MM/YYYY
            card_expire = card_expire[:5]  # تحويل إلى MM/YY (نحتفظ فقط بالأجزاء MM/YY)

        # تحقق من تنسيق MM/YY
        if not (len(card_expire) == 5 and card_expire[2] == '/'):
            messages.error(request, 'يرجى إدخال تاريخ انتهاء البطاقة بتنسيق MM/YY.')
            return redirect('payment')
        
        security_code = request.POST.get('security_code')

        if request.user.is_authenticated and not request.user.is_anonymous:
            # التحقق من وجود طلب غير مكتمل للمستخدم
            if Order.objects.filter(user=request.user, complete=False).exists():
                order = Order.objects.get(user=request.user, complete=False)
                # حفظ تفاصيل الدفع في نموذج "Payment"
                payment = Payment(
                    order=order,
                    ship_address=ship_address,
                    ship_phone=ship_phone,
                    card_number=card_number,
                    card_expire=card_expire,
                    security_code=security_code
                )
                payment.save()

                # تغيير حالة الطلب إلى مكتمل
                order.complete = True
                order.save()

                is_added = True
                messages.success(request, 'تم الدفع بنجاح')

                # تحضير البيانات التي سيتم عرضها بعد الدفع
                context = {
                    'ship_address': ship_address,
                    'ship_phone': ship_phone,
                    'card_number': card_number,
                    'card_expire': card_expire,
                    'security_code': security_code,
                    'is_added': is_added,  # تمرير is_added إلى القالب
                }
                return render(request, 'users/payment.html', context)
    
    else:
        if Order.objects.filter(user=request.user, complete=False).exists():
            order = Order.objects.get(user=request.user, complete=False)
            orderdetails = OrderDetails.objects.filter(order=order)

            total = 0
            for detail in orderdetails:
                total += detail.price * detail.quantity  # حساب المجموع الإجمالي للطلب

            # تحضير البيانات التي ستعرض قبل الدفع
            context = {
                'order': order,
                'orderdetails': orderdetails,
                'total': total,
            }

    # عرض صفحة الدفع (التأكيد أو عرض قبل الدفع)
    return render(request, 'users/payment.html', context)




# وظيفة استقبال إشعارات PayPal (Webhook)
@csrf_exempt  # تعطيل حماية CSRF لهذا الطلب
def paypal_webhook(request):
    if request.method == 'POST':
        # احصل على بيانات الطلب
        payload = request.body
        signature = request.headers.get('PayPal-Transmission-Sig')

        # تحقق من صحة البيانات عبر PayPal (يمكنك التحقق باستخدام Signature API الخاصة بـ PayPal إذا كنت ترغب)
        # هنا نحن نطبع البيانات للتحقق منها
        print("Webhook Payload:", payload)
        print("PayPal Signature:", signature)

        # يمكنك معالجة البيانات حسب الـ Event Type
        data = json.loads(payload)
        
        event_type = data.get('event_type')

        if event_type == "PAYMENT.SALE.COMPLETED":
            # التعامل مع عملية الدفع المكتملة
            print("Payment completed successfully!")
            # يمكنك معالجة الدفع هنا وإرسال إشعارات للمستخدم أو قاعدة البيانات

        elif event_type == "PAYMENT.SALE.DENIED":
            # التعامل مع الدفع المرفوض
            print("Payment was denied.")
            # يمكنك معالجة الدفع المرفوض هنا

        # رد على PayPal ببيانات النجاح
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failure', 'message': 'Invalid request'}, status=400)

# عند نجاح الدفع
def payment_success(request):
    # البحث عن الطلب بناءً على المستخدم والحالة (pending)
    order = get_object_or_404(Order, user=request.user, status='pending')
    
    # التحقق من وجود الطلب
    if order:
        # تحديث حالة الطلب إلى مكتمل
        order.complete = True  # تحديث حالة الطلب إلى "complete"
        order.status = 'paid'  # تغيير الحالة إلى "paid" إذا كان لديك هذا الحقل
        order.save()  # حفظ التغييرات في قاعدة البيانات
    
    # عرض قالب الدفع الناجح مع تفاصيل الطلب
    return render(request, 'users/payment_success.html', {'order': order})

# عند فشل الدفع
def payment_failure(request):
    return render(request, 'users/payment_failure.html')



def dashboard(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    order_details = OrderDetails.objects.all()
    
    # حساب الإجمالي لكل طلب
    for customer in customers:
        customer_orders = orders.filter(user=customer.user)
        
        for order in customer_orders:
            total = 0
            order_items = order_details.filter(order=order)
            for item in order_items:
                total += item.price * item.quantity
            order.total = total  # إضافة الإجمالي للطلب
            order.save()  # حفظ الإجمالي في قاعدة البيانات

    context = {
        'customers': customers,
        'orders': orders,
        'order_details': order_details,
    }

    return render(request, 'users/dashboard.html', context)



