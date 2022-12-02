from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

class Company(models.Model):
    owner = models.OneToOneField(
        User, 
        related_name='company',
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        )
    name = models.CharField(
        'name', 
        max_length=200,
        null=False,
        blank=False,
        unique=True,
        primary_key=True,
        )
    email = models.EmailField('email', null=True, blank=True)
    total_billing  = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)

class TypeProdutChoices(models.TextChoices):
    GENERIC = 'generic'
    FOOD = 'food'
    DRUG = 'drug'
    OTHER = 'other'
class Product(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    name = models.CharField('name', max_length=200, unique=True)
    description = models.TextField('description', max_length=200)
    price = models.FloatField(
        validators=[MinValueValidator(0.1)], # Implement GreaterThanZeroValueValidator
        null=False,
        blank=False,
        default=1,
    )
    product_type = models.CharField(
        max_length=10,
        choices=TypeProdutChoices.choices,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory',
    )
    quantity = models.PositiveIntegerField(
        'quantity', 
        blank=True,
        default=0
        )

class RegistrySituation(models.TextChoices):
    APPROVED = 'approved'
    REJECTED = 'rejjected'
    PENDING = 'pending'
class Registry(models.Model):
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        )
    product = models.ForeignKey(
        Product, 
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        )
    product_price = models.FloatField(
        validators=[MinValueValidator(0.1)], # Implement GreaterThanZeroValueValidator
        null=False,
        blank=False,
    )
    product_quantity = models.IntegerField(
        validators=[MinValueValidator(1)]
        )
    created_at = models.DateTimeField('created at', auto_now_add=True)

    situation = models.CharField(
        'situation',
        max_length=15,
        blank=True,
        null=False,
        choices=RegistrySituation.choices,
        default=RegistrySituation.PENDING
    )

    def total_price(self):
        return self.product_price * self.product_quantity

# @receiver(pre_save, sender=Order)
# def registry_order(sender, instance, **kwargs):
#     inventory = instance.product.inventory
    
#     if inventory.quantity >= instance.quantity:
#         empresa = inventory.empresa
#         inventory.quantity -= instance.quantity # Diminuir o estoque
#         empresa.faturamento_total += instance.product.price * instance.quantity # Aumentar faturamento da empresa
#         empresa.save()
#         inventory.save()
#         instance.situation = OrderSituation.approved
#         return 

#     instance.situation = OrderSituation.rejected
#     return