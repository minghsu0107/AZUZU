from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from shop import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('products/',views.index, name='index'),
    path('products/<int:id>/',views.detail, name='detail'),
    path('checkout/',views.checkout, name='checkout'),
    path('jet/', include('jet.urls', 'jet')), # for jet
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)