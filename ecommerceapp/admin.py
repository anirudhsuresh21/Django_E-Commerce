from django.contrib import admin
from ecommerceapp.models import Contact, Product, Orders, OrderUpdate, Services, ServiceAppointments, Cart
# from ecommerceapp.models import
# from ecommerceapp.models import

# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(Services)
admin.site.register(ServiceAppointments)
admin.site.register(Cart)
