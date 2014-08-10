from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext


def register(request, template_name="registration/register.html"):
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = UserCreationForm(post_data)
        if form.is_valid():
            form.save()
            username = post_data.get('username', '')
            password = post_data.get('password1', '')
            new_user = authenticate(username=username, password=password)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = urlresolvers.reverse('my_account')
                return HttpResponseRedirect(url)
    else:
        form = UserCreationForm()
    page_title = 'User Registration'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
