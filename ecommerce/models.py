from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)  # يمكن أن يكون فارغًا
    description = models.TextField(default='وصف افتراضي')
    price = models.DecimalField(max_digits=6 , decimal_places=2)
    digital = models.BooleanField(default=True)  # لا داعي لـ null=True مع BooleanField
    image = models.ImageField(upload_to='products/', default='default_image.jpg')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # تسجيل وقت الإنشاء تلقائيًا
    type = models.CharField(max_length=50, choices=[
        ('electronics', 'إلكترونيات'),
        ('fashion', 'موضة'),
        ('home', 'أدوات منزلية'),
        ('books', 'كتب'),
    ], blank=True)  # يمكن أن يكون فارغًا

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']  # ترتيب تنازلي بناءً على تاريخ الإنشاء



class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, related_name='customer')
    
    product_favorites = models.ManyToManyField(Product, related_name='product_favorites')

    address1 = models.CharField(max_length=100, null=True, blank=False) 
    address2 = models.CharField(max_length=100, null=True, blank=False)
    city = models.CharField(max_length=100, null=True, blank=False)
    state = models.CharField(max_length=100, null=True, blank=False)
    zip_code = models.CharField(max_length=100, null=True, blank=False)
    phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='orders')
    ordered_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')
    details = models.ManyToManyField(Product, through='OrderDetails')
    transaction_id = models.CharField(max_length=200, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # إضافة الحقل الجديد لحساب الإجمالي

    def __str__(self):
        return f"Order {self.transaction_id} by {self.user.username}"



class OrderDetails(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE, related_name='orders_items')
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=6 , decimal_places=2)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User" + self.order.user.username + 'product' + self.product.name + 'order id:' + str(self.order.id)
 

    class Meta:
        ordering = ['-added_date']  # ترتيب تنازلي بناءً على تاريخ الإنشاء



class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    ship_address = models.CharField(max_length=255)
    ship_phone = models.CharField(max_length=20)
    card_number = models.CharField(max_length=20)
    card_expire = models.CharField(max_length=5)  # MM/YY
    security_code = models.CharField(max_length=4)  # CVC

