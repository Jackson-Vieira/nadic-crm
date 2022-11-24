from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_init, post_init
from django.core.exceptions import ValidationError

class Empresa(models.Model):
    name = models.CharField(
        'nome', 
        max_length=200,
        unique=True,
        )
    email = models.EmailField(
        'email', 
        unique=True, 
        null=False,
        blank=False
        )
    owner = models.ForeignKey(
        User, 
        verbose_name='dono',
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
        'faturamento total', 
        null=False,
        blank=True,
        default=0
        )

    def __str__(self):
        return self.name

class TypeProdutChoices(models.TextChoices):
    generico = 'genérico'
    clothing = 'roupas'
    food = 'comida'
    drug = 'rémedio'
class Product(models.Model):
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

    def __str__(self):
        return self.name


class Inventory(models.Model): #ProductManager
    product = models.OneToOneField(
        Product, 
        on_delete=models.CASCADE, 
        related_name='inventory',
        null=False,
        blank=False
        )

    empresa = models.ForeignKey(
        Empresa, 
        on_delete=models.CASCADE, 
        related_name='inventory', 
        null=False,
        blank=False,
        )

    quantity = models.PositiveIntegerField(
        'quantity', 
        null=False,
        blank=False,
        )


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