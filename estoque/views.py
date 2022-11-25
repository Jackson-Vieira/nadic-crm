from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.shortcuts import redirect

from .models import Empresa, Product, Inventory, Order
from .forms import EmpresaModelForm, EstoqueModelForm, OrderModelForm

# class RegistryInventory(View):
#     form_class = ''
#     initial = {'key': 'value'}
#     template_name = 'form_template.html'

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect('/success/')
#         return render(request, self.template_name, {'form': form})

def home(request):
    if request.user.is_authenticated:
        pass
        #return HttpResponseRedirect(reverse('estoque:empresa'))
    return render(request, template_name='estoque/index.html')

@login_required
def empresa(request):
    template_name = 'estoque/pages/empresa.html'

    args = {
        'owner': request.user,
    }
    empresa = Empresa.objects.filter(**args).first()
    context = {'empresa':empresa}
    return render(request, template_name, context=context)

@login_required
def registros(request):
    # CHECK IF USER HAS A EMPRESA
    template_name = 'estoque/pages/orders.html'
    empresa = Empresa.objects.filter(owner=request.user).first()
    orders = Order.objects.filter(empresa=empresa)
    context = {
        'orders': orders
    }

    return render(request, template_name, context)

@login_required
def estoques(request):
    template_name = 'estoque/pages/inventorys.html'
    args = {
        'owner': request.user,
    }
    empresa = Empresa.objects.filter(**args).first() # FIX: APENAS UMA EMPRESA POR USUARIO
    estoques = Inventory.objects.filter(empresa=empresa) 
    context = {'inventorys':estoques}
    return render(request, template_name, context=context)

@login_required
def estoque(request, pk):
    template_name = 'estoque/pages/inventory.html'
    args = {
        'owner': request.user,
    }
    empresa = Empresa.objects.filter(**args).first() # FIX: APENAS UMA EMPRESA POR USUARIO
    estoques = Inventory.objects.filter(empresa=empresa)
    estoque = get_object_or_404(estoques, pk=pk)
    products = Product.objects.filter(inventory=estoque)

    context = {'products':products}
    return render(request, template_name, context=context)

@login_required
def product(request, pk_estoque, pk_product):
    template_name = 'estoque/pages/product.html'
    args = {
        'owner': request.user,
    }
    empresa = Empresa.objects.filter(**args).first() # FIX: APENAS UMA EMPRESA POR USUARIO
    estoques = Inventory.objects.filter(empresa=empresa)
    estoque = get_object_or_404(estoques, pk=pk_estoque)

    products = Product.objects.filter(inventory=estoque)
    product = get_object_or_404(products, pk=pk_product)

    context = {'product':product}
    return render(request, template_name, context=context)

#FORMS
@login_required
def new_empresa(request):

    form = EmpresaModelForm(None or request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_empresa = form.save(commit=False)
            new_empresa.owner = request.user
            new_empresa.save()
            return HttpResponseRedirect(reverse('estoque:empresa'))
        

    return redirect(reverse('estoque:home'))

# @login_required
# def new_product(request):
#     form = ProdutModelForm(None or request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             product = form.save()
#             return HttpResponseRedirect(reverse('estoque:estoque'), args=(product.id))
#     template_name = 'estoque/forms/product_create_form.html'
#     context = {'form': form}
#     return render(request, template_name=template_name, context=context)

@login_required
def new_estoque(request):
    form = EstoqueModelForm(None or request.POST)
    if request.method == 'POST':
        if form.is_valid():
            estoque = form.save(commit=False)
            empresa = Empresa.objects.get(owner=request.user)
            estoque.empresa = empresa
            estoque.save()
        return HttpResponseRedirect(reverse('estoque:estoques'))

    template_name = 'estoque/forms/estoque_create_form.html'
    context = {
        'form': form,
        }
    return render(request, template_name=template_name, context=context)

@login_required
def edit_estoque(request, pk):
    estoque = get_object_or_404(Inventory, pk=pk)
    form = EstoqueModelForm(instance=estoque)
    if request.method == 'POST':
        form = EstoqueModelForm(instance=estoque, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('estoque:estoques'))
        print(form.errors)
    template_name = 'estoque/forms/estoque_edit_form.html'
    context = {
        'estoque':estoque,
        'form': form,
        }
    return render(request, template_name=template_name, context=context)


@login_required
def delete_estoque(request, pk):
    estoque = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        estoque.delete()
        return HttpResponseRedirect(reverse('estoque:estoques'))

    template_name = 'estoque/forms/confirm_delete_form.html'
    context = {
        'estoque':estoque
        }
    return render(request, template_name=template_name, context=context)

@login_required
def delete_estoque(request, pk):
    estoque = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        estoque.delete()
        return HttpResponseRedirect(reverse('estoque:estoques'))

    template_name = 'estoque/forms/confirm_delete_form.html'
    context = {
        'estoque':estoque
        }
    return render(request, template_name=template_name, context=context)


@login_required
def new_registro(request):
    form = OrderModelForm(None or request.POST)
    if request.method == 'POST':
        if form.is_valid():
            registry = form.save(commit=False)
            empresa = Empresa.objects.get(owner=request.user)
            registry.empresa = empresa
            product = get_object_or_404(Product, pk=request.POST.get('product'))
            registry.product = product
            registry.save()
            return HttpResponseRedirect(reverse('estoque:registros'))

    empresa = Empresa.objects.get(owner=request.user)
    args = {
        'empresa':empresa
    }

    inventorys = Inventory.objects.filter(**args)
    template_name = 'estoque/forms/order_create_form.html'
    context = {
        'form': form,
        'inventorys': inventorys,
        }


    return render(request, template_name=template_name, context=context)