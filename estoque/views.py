from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required

from django.urls import reverse


from django.forms import inlineformset_factory
from .models import Empresa, Product, Inventory, Sale, Order

from .forms import EmpresaModelForm, ProdutModelForm, EstoqueModelForm, SaleFormSet

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
def estoques(request):
    template_name = 'estoque/pages/inventorys.html'
    args = {
        'owner': request.user,
    }
    empresa = Empresa.objects.filter(**args).first() # FIX: APENAS UMA EMPRESA POR USUARIO
    estoques = Inventory.objects.filter(empresa=empresa)
    #products = Product.objects.filter(inventory__in=estoques)
    
    context = {'inventorys':estoques}
    return render(request, template_name, context=context)

@login_required
def estoque(request, pk):
    template_name = 'estoque/pages/generic_list.html'
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
    if request.method == 'POST':
        form = EmpresaModelForm(None or request.POST)
        if form.is_valid():
            new_empresa = form.save(commit=False)
            new_empresa.owner = request.user
            new_empresa.save()
        return HttpResponseRedirect(reverse('estoque:empresas'))
    
@login_required
def new_product(request):
    form = ProdutModelForm(None or request.POST)
    if request.method == 'POST':
        if form.is_valid():
            product = form.save()
        return HttpResponseRedirect(reverse('estoque:estoque'), args=(product.id))

    template_name = 'estoque/forms/product_create_form.html'
    context = {'form': form}
    
    return render(request, template_name=template_name, context=context)

@login_required
def new_estoque(request):
    form = EstoqueModelForm(None or request.POST)
    if request.method == 'POST':
        if form.is_valid():
            estoque = form.save()
        return HttpResponseRedirect(reverse('estoque:estoque', args=(estoque.id)))

    template_name = 'estoque/forms/estoque_create_form.html'
    context = {'form': form}
    return render(request, template_name=template_name, context=context)

@login_required
def new_sale(request):
    pass