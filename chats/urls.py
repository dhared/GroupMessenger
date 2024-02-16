from rest_framework.routers import DefaultRouter

from chats.views import ChatViewSet

router = DefaultRouter()
router.register('chat', ChatViewSet)

urlpatterns = router.urls
