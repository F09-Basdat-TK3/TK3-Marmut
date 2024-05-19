from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .queries import login

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = login(email, password)

        for element in user:
            print(element)
            
        if not user[0]:  # Check if the user data list is empty
            context = {'login_error': 'Invalid login credentials'}
            return render(request, 'login.html', context)   
        
        user_data = user[0][0]  # Access the first tuple in the user data list
        premium_data = user[1] if len(user) > 1 and user[1] else None

        response = HttpResponseRedirect(reverse("dashboard:show_dashboard"))
        response.set_cookie('email', user_data[0])
        response.set_cookie('nama', user_data[2])
        response.set_cookie('role', 'non premium' if premium_data is None else 'premium')
        response.set_cookie('kota_asal', user_data[4])
        response.set_cookie('gender', user_data[3])
        response.set_cookie('tanggal_lahir', user_data[5])
        response.set_cookie('kota_asal', user_data[7])

        
        return response  # Add this return to complete the redirect
    
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    response = HttpResponseRedirect(reverse('authentication:login_user'))
    response.delete_cookie('email')
    response.delete_cookie('role')
    response.delete_cookie('nama')
    response.delete_cookie('kota_asal')
    response.delete_cookie('gender')
    response.delete_cookie('tanggal_lahir')

    return response

def register_user(request):
    # TODO: BUAT FUNGSI REGISTER
    return
