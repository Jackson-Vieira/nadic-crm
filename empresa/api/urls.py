from rest_framework.routers import SimpleRouter

from .views import CompanyViewSet, ProductViewSet, RegistryViewSet, InventoryViewSet


router = SimpleRouter()
router.register(r'companys', CompanyViewSet)
router.register(r'products', ProductViewSet)
router.register(r'registrys', RegistryViewSet)
router.register(r'inventory', InventoryViewSet)

urlpatterns = router.urls