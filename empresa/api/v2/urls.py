from rest_framework.routers import SimpleRouter

from .viewsets import CompanyViewSet, ProductViewSet, RegistryViewSet

router = SimpleRouter()
router.register('companys', viewset=CompanyViewSet)
router.register('products', viewset=ProductViewSet)
router.register('registrys', viewset=RegistryViewSet)
urlpatterns = router.urls