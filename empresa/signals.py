from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Product, Registry, Inventory, Company, RegistrySituation

@receiver(post_save, sender=Registry)
def verify_registry(sender, instance, created, **kwargs):
    if created:
        # idea: celery task
        # pegar o produto
        registry = instance
        product = registry.product
    
        # pegar o inventário do produto
        inventory = Inventory.objects.get(pk=product.inventory.id)

        # validar o registro
        product_quantity_registry = registry.product_quantity
        if(product_quantity_registry > inventory.quantity):
            #mudar a situação
            registry.situation = RegistrySituation.REJECTED
            registry.save()
        else:
            # pegar a empresa do produto
            product_company = Company.objects.get(pk=product.company.id)
            # diminuir o estoque do produto
            inventory.quantity -= product_quantity_registry
            product_company.total_billing += product_quantity_registry*registry.product_price
            inventory.save()
            product_company.save()
            # mudar a situação
            registry.situation = RegistrySituation.APPROVED
            registry.save()