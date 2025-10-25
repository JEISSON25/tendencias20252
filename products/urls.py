from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
=======
from products.front.views.ProductsFrontView import ProductsFrontView
>>>>>>> repo2/main
from products.views import ProductView

router = DefaultRouter()
router.register(r'products', ProductView, "products")
<<<<<<< HEAD
=======
router.register('front/products', ProductsFrontView, basename='products_front')
>>>>>>> repo2/main

urlpatterns = router.urls