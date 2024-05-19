from django.shortcuts import render

def show_dashboard(request):
    name = request.COOKIES.get('nama', 'Guest')
    email = request.COOKIES.get('email')
    role = request.COOKIES.get('non premium', 'premium')
    kota_asal = request.COOKIES.get('kota_asal')
    gender = request.COOKIES.get('gender')
    tanggal_lahir = request.COOKIES.get('tanggal_lahir')

    context = {
        'name': name,
        'email': email,
        'role': role,
        'kota_asal': kota_asal,
        'gender': gender,
        'tanggal_lahir': tanggal_lahir,
    }
    return render(request, 'show_dashboard.html', context)
