from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_init, post_init

from django.core.exceptions import ValidationError

class Empresa(models.Model):
    name = models.CharField(
        'name', 
        max_length=200
        )
    email = models.EmailField('email')
    owner = models.ForeignKey(
        User, 
        related_name='empresa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )
    is_active = models.BooleanField(
        'is active', 
        default=True
        )
    faturamento_total  = models.PositiveIntegerField(
        'faturamento', 
        null=False,
        blank=True,
        default=0
        )


class Inventory(models.Model): #ProductManager
    empresa = models.ForeignKey(
        Empresa, 
        on_delete=models.CASCADE, 
        related_name='invetorys', 
        null=False,
        blank=False,
        )
    quantity = models.PositiveIntegerField(
        'quantity', 
        null=False,
        blank=False,
        )


class TypeProdutChoices(models.TextChoices):
    generico = 'genérico'
    clothing = 'roupas'
    food = 'comida'
    drug = 'rémedio'
class Product(models.Model):
    inventory = models.OneToOneField(
        Inventory, 
        on_delete=models.CASCADE, 
        related_name='products',
        null=False,
        blank=False
        )

    name = models.CharField('name', max_length=200)
    description = models.TextField('description', max_length=500)
    price = models.FloatField(
        validators=[MinValueValidator(1)],
        null=False,
        blank=False,
        default=1,
    )

    tipo = models.CharField(
        max_length=10,
        choices=TypeProdutChoices.choices,
        null=True,
        blank=True
    )
    fabricatedAt = models.DateField(
        'fabricated at', 
        null=False, 
        blank=False)


class Sale(models.Model):
    empresa = models.ForeignKey(
        Empresa, 
        on_delete=models.CASCADE, 
        related_name='sales'
        )
    boughtAt = models.DateTimeField('bought at', auto_now_add=True)


class OrderSituation(models.TextChoices):
    approved = 'aprovada'
    rejected = 'rejeitada'
    pending = 'pendente'
class Order(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        null=None,
        blank=None,
        )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)]
        )
    createdAt = models.DateTimeField('created at', auto_now_add=True)
    registry = models.ForeignKey(
        Sale, 
        on_delete=models.CASCADE, 
        related_name='orders',
        null=True,
        blank=True,
        )

    situation = models.CharField(
        'situation',
        max_length=15,
        blank=True,
        null=False,
        choices=OrderSituation.choices,
        default=OrderSituation.pending
    )


@receiver(pre_save, sender=Order)
def registry_order(sender, instance, **kwargs):
    inventory = instance.product.inventory
    
    if inventory.quantity >= instance.quantity:
        empresa = inventory.empresa
        inventory.quantity -= instance.quantity # Diminuir o estoque
        empresa.faturamento_total += instance.product.price * instance.quantity # Aumentar faturamento da empresa
        empresa.save()
        inventory.save()
        instance.situation = OrderSituation.approved
        return 

    instance.situation = OrderSituation.rejected
    return