from rest_framework import permissions
from drf_yasg.views import get_schema_view
from knox import views as knox_views
from .views import *
from django.urls import path, include, re_path

from drf_yasg import openapi
#for images
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required




schema_view = get_schema_view(
   openapi.Info(
      title="Grocery APi",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('register', RegisterApi.as_view(), name='register'),
    path('register-get/<int:id>', registerget.as_view(), name='register'),
    # path('register-get', register_get_all.as_view(), name='register'),

    path('signin', LoginAPI.as_view()),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),

    path('user-details' , UserDeatilsPost.as_view() ),#for products get
    path('user-details-put/<int:id>' , UserDeatilsPut.as_view() ),#for products get for guest
    path('UserDeatilsGet-details-post', UserDeatilsGet.as_view()),#for product post

       #for swagger
    path('swagger', (schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
