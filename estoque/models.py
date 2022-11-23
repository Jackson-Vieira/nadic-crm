from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator


class Company(models.Model):
    name = models.CharField(
        'name', 
        max_length=200
        )
    email = models.EmailField('email')
    owner = models.ForeignKey(
        User, 
        related_name='company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )
    is_active = models.BooleanField(
        'is active', 
        default=True
        )
    total_vendas  = models.PositiveIntegerField(
        'total vendas', 
        null=False,
        blank=True,
        default=0
        )

class Inventory(models.Model):
    empresa = models.ForeignKey(
        Company, 
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
    inventory = models.ForeignKey(
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
    saled = models.BooleanField(
        'saled', 
        default=False,
        null=False, 
        blank=True,
        )
    tipo = models.CharField(
        max_length=10,
        choices=TypeProdutChoices.choices,
        null=True,
    )
    fabricatedAt = models.DateField(
        'fabricated at', 
        null=False, 
        blank=False)

class Sale(models.Model):
    empresa = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        related_name='sales'
        )
    boughtAt = models.DateTimeField('bought at', auto_now_add=True)

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

