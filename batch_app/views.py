# from django.shortcuts import render
import json        
from batch_app.models import Batch, Code
from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from scripts.generic_helper import create_data
from batch_app.form import MainForm, SearchKeyword
from scripts.generic_helper import get_paginated_response
# Create your views here.
def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')
		context = {}
		return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def Home(request):
	if not request.user.is_authenticated:
		return redirect('login')
	query = list()
	username = request.user.username
	page_number = request.GET.get('page') or 1

	if request.method == 'POST':
		form = MainForm(request.POST)
		if form.is_valid():
			batch_name = form.cleaned_data.get('batch_name')
			number_of_codes = form.cleaned_data.get('number_of_codes')
			_, is_created = create_data(request.user._wrapped, batch_name, number_of_codes)

			if is_created:
				messages.success(request, f'Batch submission successful for {batch_name} with {number_of_codes} number of codes')
	
	elif request.method == 'GET':
		form = SearchKeyword(request.GET)
		
		search_string = form.data.get('search_keyword')
		
		qs = Code.objects.filter(batch__in = Batch.objects.filter(batch_user = request.user._wrapped))
		if search_string:
			query = qs.filter(batch_code__icontains = search_string)
			query = get_paginated_response(request,query, page_number)
			query['search_keyword'] = search_string

	post_form = MainForm()
	get_form = SearchKeyword()
	
	return render(request, 'home.html', {'username':username.upper(), 'post_form':post_form,"get_form":get_form, "query_list":query})