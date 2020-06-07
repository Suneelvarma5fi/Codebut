from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm,UpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from blog.models import BlogPosts
# Create your views here.

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f"{ username }'s account has been created!")
			return redirect('users-login')
	else:
		form = UserRegisterForm()

	return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f"Profile has been updated!")
			return redirect('users-profile')
	else:
		u_form = UpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		post_list = BlogPosts.objects.filter(author = request.user.profile)

	updateforms = {
		'u_form' : u_form,
		'p_form' : p_form,
		'post_list' : post_list,
	}
	return render(request,'users/profile.html',updateforms)

