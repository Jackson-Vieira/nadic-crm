from django.shortcuts import render

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

def register(request):
    form = UserCreationForm(None or request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()

    template_name = 'account/register.html'
    context = {'form': form}

    return render(request, template_name=template_name, context=context)
