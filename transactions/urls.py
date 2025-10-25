from rest_framework import routers

from transactions import views
<<<<<<< HEAD

router = routers.DefaultRouter()
router.register(r'transactions', views.TransactionViewSet, basename='transactions')
=======
from transactions.front.views.TransactionsFrontView import TransactionsFrontView

router = routers.DefaultRouter()
router.register(r'transactions', views.TransactionViewSet, basename='transactions')
router.register('front/transactions', TransactionsFrontView, basename='transactions_front')
>>>>>>> repo2/main

urlpatterns = router.urls