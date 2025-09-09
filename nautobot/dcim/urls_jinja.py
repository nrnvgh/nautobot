"""
URLs for Jinja2 template performance comparison POC.

Maps Jinja2 views under the /jinja/dcim/ namespace for A/B testing
against the standard Django template views.
"""

from nautobot.core.views.routers import NautobotUIViewSetRouter

from . import views_jinja

app_name = "dcim_jinja"

# Create router for Jinja2 views
router = NautobotUIViewSetRouter()
router.register("locations", views_jinja.LocationJinjaUIViewSet)

urlpatterns = router.urls
