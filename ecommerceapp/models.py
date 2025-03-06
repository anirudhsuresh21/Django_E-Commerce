from django.db import models
# from django.template.context_processors import request


# Create your models here.
class Contact(models.Model):
    # contact_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    desc=models.TextField(max_length=500)
    phonenumber=models.IntegerField()

    def __int__(self):
        return self.id
    


class Product(models.Model):
    CATEGORIES = [
        ('BRIDE', 'Bridal Collection'),
        ('GROOM', 'Groom Collection'),
        ('JEWELRY', 'Jewelry'),
        ('FOOTWEAR', 'Footwear'),
        ('ACCESSORIES', 'Accessories'),
    ]

    SUBCATEGORIES = {
        'BRIDE': [
            ('LEHENGA', 'Lehenga'),
            ('SAREE', 'Saree'),
            ('GOWN', 'Wedding Gown'),
            ('SUIT', 'Bridal Suit'),
        ],
        'GROOM': [
            ('SHERWANI', 'Sherwani'),
            ('SUIT', 'Wedding Suit'),
            ('INDO', 'Indo-Western'),
            ('KURTA', 'Kurta Set'),
        ],
        'JEWELRY': [
            ('NECKLACE', 'Necklace Sets'),
            ('EARRINGS', 'Earrings'),
            ('BANGLES', 'Bangles & Bracelets'),
            ('RINGS', 'Rings'),
            ('MANG_TIKA', 'Maang Tika'),
        ],
        'FOOTWEAR': [
            ('BRIDE_SHOES', 'Bridal Footwear'),
            ('GROOM_SHOES', 'Groom Footwear'),
        ],
        'ACCESSORIES': [
            ('CLUTCH', 'Clutches & Bags'),
            ('DUPATTA', 'Dupattas'),
            ('TURBAN', 'Turbans'),
            ('STOLE', 'Stoles & Shawls'),
        ],
    }

    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
        ('CUSTOM', 'Custom Size'),
    ]

    product_id = models.AutoField(primary_key=True)  # Remove default value
    product_name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    subcategory = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True)
    fabric = models.CharField(max_length=100, null=True, blank=True)
    # color = models.CharField(max_length=50)
    sizes_available = models.CharField(max_length=100,null=True)  # Store as comma-separated values
    stock = models.IntegerField(default=0,null=True)
    custom_sizing_available = models.BooleanField(default=False,null=True)
    alteration_available = models.BooleanField(default=False,null=True)
    # delivery_time = models.CharField(max_length=50, help_text="Estimated delivery time")
    
    # Multiple images support
    main_image = models.ImageField(upload_to='products/main/',null=True)
    image_2 = models.ImageField(upload_to='products/additional/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='products/additional/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='products/additional/', null=True, blank=True)
    
    # Additional wedding-specific fields
    occasion_type = models.CharField(max_length=50, help_text="e.g., Wedding, Reception, Sangeet", null=True, blank=True)
    style = models.CharField(max_length=50, help_text="e.g., Traditional, Modern, Fusion", null=True, blank=True)
    work_type = models.CharField(max_length=100, help_text="e.g., Zardozi, Sequin, Embroidery", null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    reviews_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product_name} - {self.category}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'subcategory']),
            models.Index(fields=['price']),
        ]

    @property
    def is_on_sale(self):
        return bool(self.sale_price)

    @property
    def discount_percentage(self):
        if self.sale_price:
            return int(((self.price - self.sale_price) / self.price) * 100)
        return 0


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json =  models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)    
    oid=models.CharField(max_length=150,blank=True)
    amountpaid=models.CharField(max_length=500,null=True)
    paymentstatus=models.CharField(max_length=20)
    phone = models.CharField(max_length=100,default="")
    or_id = models.CharField(max_length=100,default="")
    update_desc = models.CharField(max_length=5000,default="")
    delivered=models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name



class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    delivered=models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)
    or_id = models.CharField(max_length=100,default="")
    email = models.CharField(max_length=90,default="")

    def __str__(self):
        return self.update_desc[0:7] + "..."

class Services(models.Model):
    SERVICE_CATEGORIES = [
        ('Matchmaking', 'Matchmaking'),
        ('Wedding Planning', 'Wedding Planning'),
        ('Photography', 'Photography'),
        ('Catering', 'Catering'),
        ('Venue Booking', 'Venue Booking'),
        ('Makeup & Styling', 'Makeup & Styling'),
        ('Music & Entertainment', 'Music & Entertainment'),
    ]

    service_id = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=100)  # Name of the service provider
    email = models.EmailField(max_length=100, unique=True)  # Ensuring unique emails
    phone_no = models.CharField(max_length=15, unique=True)  # Contact number
    address = models.TextField()  # **Single field for full address**
    service_name = models.CharField(max_length=100)  # Service title
    service_category = models.CharField(max_length=50, choices=SERVICE_CATEGORIES, default='Matchmaking')  # Service Type
    description = models.TextField(null=True, blank=True)  # Detailed description
    price_range = models.CharField(max_length=100, null=True, blank=True)  # Example: "₹10,000 - ₹50,000"
    experience_years = models.IntegerField(null=True, blank=True)  # Experience in years
    website = models.URLField(null=True, blank=True)  # Business website
    profile_image = models.ImageField(upload_to='service_providers/', null=True, blank=True)  # Provider image/logo
    rating = models.FloatField(default=0.0)  # Average customer rating
    reviews_count = models.IntegerField(default=0)  # Number of customer reviews
    social_links = models.JSONField(null=True, blank=True)  # Store social media links
    available_days = models.CharField(max_length=100, null=True, blank=True)  # Example: "Monday-Saturday"
    working_hours = models.CharField(max_length=100, null=True, blank=True)  # Example: "9 AM - 7 PM"
    service_area_radius = models.IntegerField(null=True, blank=True)  # Serviceable area in km
    verified = models.BooleanField(default=False)  # Verified provider or not
    # created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets on creation
    # updated_at = models.DateTimeField(auto_now=True)  # Updates on modification

    def __str__(self):
        return f"{self.service_name} - {self.provider_name}"


class ServiceAppointments(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed')
    ]

    appointment_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    service = models.ForeignKey(
        Services, 
        on_delete=models.CASCADE,
        related_name='appointments',
        null=True  # Allow null temporarily for migration
    )
    service_name = models.CharField(max_length=100)
    appointment_date = models.DateField(null=True)
    appointment_time = models.TimeField(null=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    special_requests = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.customer_name} - {self.service_name} ({self.appointment_date})"

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)  # Can be linked to a User model if authentication is used
    product_id = models.IntegerField()  # Store the product ID instead of a ForeignKey
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.product_name} (x{self.quantity})"

    @property
    def total_price(self):
        """Returns total price based on quantity"""
        return self.quantity * (self.sale_price if self.sale_price else self.price)




