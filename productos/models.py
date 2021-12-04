from _testcapi import matmulType

from django.db import models

# Create your models here.

from django.db import models
from datetime import datetime

from django.http import HttpResponse


class Product_type(models.Model):
    product_type_name = models.CharField(max_length=50)

    class Meta:
        db_table: 'PRODUCT_TYPE'

    def __str__(self):
        return self.product_type_name


class Provider(models.Model):
    name = models.CharField(max_length=45)
    nit = models.CharField(max_length=45)
    url = models.CharField(max_length=45)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=45)

    class Meta:
        db_table: 'PROVIDER'

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    fk_id_product_type = models.ForeignKey(Product_type, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table: 'PRODUCT'

    def __str__(self):
        return self.product_name


class Product_provider(models.Model):
    fk_id_provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    bar_code = models.CharField(max_length=45 , null=True)
    stock = models.IntegerField(null=True)
    fk_id_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table: 'PRODUCT_PROVIDER'

    def __str__(self):
        return self.bar_code


class Price_product(models.Model):
    sale_price = models.DecimalField(max_digits=13, decimal_places=2)
    shop_price = models.DecimalField(max_digits=13, decimal_places=2)
    start_date = models.DateField()
    user_update = models.CharField(max_length=40)
    date_update = models.DateField(null=True)
    fk_id_product_provider = models.ForeignKey(Product_provider, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table: 'PRICE_PRODUCT'

    def __str__(self):
        return str(self.shop_price)


class Tax(models.Model):
    tax_value = models.DecimalField(max_digits=5, decimal_places=2)
    tax_name = models.CharField(max_length=20)
    creation_date = models.DateField()

    class Meta:
        db_table: 'TAX'

    def __str__(self):
        return str(self.tax_value)

class Tax_price_product(models.Model):
    fk_id_tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    fk_id_price_product = models.ForeignKey(Price_product, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table: 'TAX_PRICE_PRODUCT'

    def __str__(self):
        return str(self.fk_id_tax)


class Person(models.Model):
    person_name = models.CharField(max_length=45)
    person_last_name = models.CharField(max_length=45)
    person_address = models.CharField(max_length=45)
    # opcional
    person_phone = models.CharField(max_length=45)
    # ********
    person_dni = models.CharField(max_length=10)

    class Meta:
        db_table: 'PERSON'

    def __str__(self):
        return self.person_name



class Person_type(models.Model):
    person_type_name = models.CharField(max_length=45)

    class Meta:
        db_table: 'PERSON_TYPE'

    def __str__(self):
        return self.person_type_name


class Person_person_type(models.Model):
    fk_id_person_type = models.ForeignKey(Person_type, on_delete=models.CASCADE, null=True)
    fk_id_person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table: 'PERSON_PERSON_TYPE'

    def __str__(self):
        return str(self.fk_id_person_type)




class Ticket(models.Model):
    # id_ticket = models.IntegerField()
    half_payment = models.DecimalField(max_digits=15, decimal_places=2)
    ticket_date = models.DateField()
    fk_id_person_cachier = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='fk_id_person_cachier',
                                             null=True)
    fk_id_person_costumer = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='fk_id_person_costumer',
                                              null=True)

    class Meta:
        db_table: 'TICKET'

    def __str__(self):
        return str(self.half_payment)



class Ticket_detail(models.Model):
    amount = models.IntegerField(null=True)
    fk_id_tax_price_product = models.ForeignKey(Tax_price_product, on_delete=models.CASCADE, null=True)
    fk_id_ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    devolution_request = models.DateField(null=True)
    devolution_approved = models.DateField(null=True)
    description_devolution = models.CharField(max_length=45)

    # fk_id_person_administrator = models.ForeignKey()

    class Meta:
        db_table: 'TICKET_DETAIL'

    def __str__(self):
        return str(self.half_payment)





