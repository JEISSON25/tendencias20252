from rest_framework.routers import DefaultRouter
<<<<<<< HEAD

=======
from clients.front.views.ClientsFrontView import ClientsFrontView
>>>>>>> repo2/main
from clients.views import ClientView

router = DefaultRouter()

router.register(r'clients', ClientView, basename='clients')
<<<<<<< HEAD
=======
router.register('front/clients', ClientsFrontView, basename='clients_front')
>>>>>>> repo2/main

urlpatterns = router.urls