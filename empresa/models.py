from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_init, post_init


from django.core.exceptions import ValidationError

class Company(models.Model):
    owner = models.OneToOneField(
        User, 
        related_name='empresa',
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        )
    name = models.CharField(
        'name', 
        max_length=200,
        null=False,
        blank=False,
        )
    email = models.EmailField('email', null=True, blank=True)
    total_billing  = models.FloatField(default=0)

class TypeProdutChoices(models.TextChoices):
    GENERIC = 'generic'
    FOOD = 'food'
    DRUG = 'drug'
    OTHER = 'other'
class Product(models.Model):
    company = models.ForeignKey(
        
    )
    name = models.CharField('name', max_length=200)
    description = models.TextField('description', max_length=200)
    price = models.FloatField(
        validators=[MinValueValidator(0.1)], # Implement GreaterThanZeroValueValidator
        null=False,
        blank=False,
    )
    product_type = models.CharField(
        max_length=10,
        choices=TypeProdutChoices.choices,
        null=False,
        blank=False,
    )

class Inventory(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory',
    )
    quantity = models.PositiveIntegerField(
        'quantity', 
        null=False,
        blank=False,
        )

class RegistrySituation(models.TextChoices):
    APPROVED = 'approved'
    REJECTED = 'rejjected'
    PENDING = 'pending'
class Registry(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.DO_NOTHING,
        null=False,
        blank=False,
        )
    product_price = None
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
        default=RegistrySituation.pending
    )


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