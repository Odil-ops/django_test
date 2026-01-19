# config/urls.py (loyiha fayli)

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse

# 1. Oddiy view yaratamiz
def home_view(request):
    return HttpResponse("Bosh sahifa - Django ishlayapti!")

# 2. To'g'ri URL konfiguratsiyasi:
urlpatterns = [
    # Til o'zgartirish uchun (i18n)
    path('i18n/', include('django.conf.urls.i18n')),
]

# 3. i18n_patterns ichida faqat kerakli yo'llarni qo'shamiz
urlpatterns += i18n_patterns(
    # Admin paneli (faqat bir marta)
    path('admin/', admin.site.urls),
    
    # Bosh sahifa
    path('', home_view, name='home'),
    
    # Quiz app (agar mavjud bo'lsa)
    # path('quiz/', include('quiz.urls')),
)