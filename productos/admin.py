from django.contrib import admin
from productos.models import Price_product, Product_type,Product,Product_provider,Provider,Tax_price_product,Tax,Ticket_detail,Ticket,Person,Person_person_type,Person_type
# Register your models here.

class price_prod_Admin(admin.ModelAdmin):
    fields = ("user_update",
              "date_update",
              "sale_price",
              "shop_price",
              "start_date",)
class prod_type_Admin(admin.ModelAdmin):
    list_filter = ['product_type_name']

# poder registrar en el admin
admin.site.register(Price_product,price_prod_Admin)
admin.site.register(Product_type,prod_type_Admin)
admin.site.register(Product)
admin.site.register(Product_provider)
admin.site.register(Provider)
admin.site.register(Tax)
admin.site.register(Tax_price_product)
admin.site.register(Ticket)
admin.site.register(Ticket_detail)
admin.site.register(Person)
admin.site.register(Person_type)
admin.site.register(Person_person_type)

