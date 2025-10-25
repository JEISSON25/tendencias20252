from rest_framework.routers import DefaultRouter

from auth import views
<<<<<<< HEAD

router = DefaultRouter()
router.register(r'auth', views.AuthView, basename='auth')
=======
from auth.front.views.AuthFrontView import AuthFrontView

router = DefaultRouter()
router.register(r'auth', views.AuthView, basename='auth')
router.register('front/auth', AuthFrontView, basename='auth_front')
>>>>>>> repo2/main

urlpatterns = router.urls