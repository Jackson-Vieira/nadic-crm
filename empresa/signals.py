from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Product, Registry, Inventory, Company, RegistrySituation


@receiver(post_save, sender=Product)
def create_product_inventory(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(product=instance)

@receiver(post_save, sender=Registry)
def verify_registry(sender, instance, created, **kwargs):
    if created:
        # IDEA: Celery task

        # get product
        registry = instance
        product = registry.product
    
        # get inventory product
        inventory = Inventory.objects.get(pk=product.inventory.id)

        # validate registry
        product_quantity_registry = registry.product_quantity
        if(product_quantity_registry > inventory.quantity):
            # change situation
            registry.situation = RegistrySituation.REJECTED
            registry.save()
        else:
            # get the company product
            product_company = Company.objects.get(pk=product.company.name)
            # change the product quantity inventory
            inventory.quantity -= product_quantity_registry
            product_company.total_billing += product_quantity_registry*registry.product_price
            inventory.save()
            product_company.save()
            # change situation
            registry.situation = RegistrySituation.APPROVED
            registry.save()