from rest_framework.routers import DefaultRouter
from .views import ItemView

router = DefaultRouter()
router.register(r'itens',ItemView, basename='item')

urlpatterns = router.urls