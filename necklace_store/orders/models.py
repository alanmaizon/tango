from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

class ChainType(models.Model):
    type_name = models.CharField(max_length=255)
    price = models.FloatField()

    def __str__(self):
        return self.type_name

class ChainLength(models.Model):
    length = models.CharField(max_length=255)
    price = models.FloatField()

    def __str__(self):
        return self.length

class Material(models.Model):
    material_name = models.CharField(max_length=255)
    price = models.FloatField()

    def __str__(self):
        return self.material_name

class FontStyle(models.Model):
    style_name = models.CharField(max_length=255)

    def __str__(self):
        return self.style_name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"

class Product(models.Model):
    custom_name = models.CharField(max_length=12)
    final_price = models.FloatField(null=True, blank=True)
    stock_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=now)
    chain_type = models.ForeignKey(ChainType, on_delete=models.PROTECT)
    chain_length = models.ForeignKey(ChainLength, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    font_style = models.ForeignKey(FontStyle, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products", blank=True, null=True)

    def calculate_final_price(self):
        print(f"Chain Type Price: {self.chain_type.price if self.chain_type else 'None'}")
        print(f"Chain Length Price: {self.chain_length.price if self.chain_length else 'None'}")
        print(f"Material Price: {self.material.price if self.material else 'None'}")
        self.final_price = (
            (self.chain_type.price if self.chain_type else 0) +
            (self.chain_length.price if self.chain_length else 0) +
            (self.material.price if self.material else 0)
        )

    def generate_stock_code(self):
        print(f"Chain Type: {self.chain_type.type_name if self.chain_type else 'None'}")
        print(f"Chain Length: {self.chain_length.length if self.chain_length else 'None'}")
        print(f"Material: {self.material.material_name if self.material else 'None'}")
        code_parts = [
            self.chain_type.type_name.upper() if self.chain_type else "",
            self.chain_length.length.replace(" ", "-").upper() if self.chain_length else "",
            self.material.material_name[0].upper() if self.material else ""
        ]
        self.stock_code = "-".join(code_parts)


    def save(self, *args, **kwargs):
        self.calculate_final_price()
        self.generate_stock_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.custom_name
