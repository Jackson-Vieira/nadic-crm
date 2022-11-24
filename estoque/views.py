from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse


from django.urls import reverse


from .forms import EmpresaModelForm

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

def empresas(request):
    template_name = 'form_template.html'

    context = {}

    return render(request, template_name, context=context)


def new_empresa(request):
    if request.method == 'POST':
        empresa = EmpresaModelForm(request.POST)

        if empresa.is_valid():
            new_empresa = empresa.save(commit=False)
            new_empresa.owner = request.user
            new_empresa.save()

        return HttpResponse("Do something")
