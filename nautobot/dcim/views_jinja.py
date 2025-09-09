"""
Views for Jinja2 template performance comparison POC.

These views inherit from the existing DCIM views but use Jinja2 templates instead of Django templates.
"""

import time

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.template import engines
from django.urls import NoReverseMatch, reverse

from nautobot.core.utils import lookup
from nautobot.core.utils.lookup import get_created_and_last_updated_usernames_for_model

from .views import LocationUIViewSet


class LocationJinjaUIViewSet(LocationUIViewSet):
    """
    Location viewset that uses Jinja2 templates for performance comparison.

    Inherits all functionality from LocationUIViewSet but overrides template selection
    to use Jinja2 templates from templates_jinja directories.
    """

    def _build_permissions_context(self, user):
        """
        Build a permissions context that mimics Django's perms template variable.

        Django templates expect perms.app_label.permission_name syntax.
        """

        class PermissionProxy:
            def __init__(self, user):
                self.user = user

            def __getattr__(self, app_label):
                return AppPermissionProxy(self.user, app_label)

        class AppPermissionProxy:
            def __init__(self, user, app_label):
                self.user = user
                self.app_label = app_label

            def __getattr__(self, permission_name):
                full_perm = f"{self.app_label}.{permission_name}"
                return self.user.has_perm(full_perm)

        return PermissionProxy(user)

    def _url_helper(self, viewname, *args, **kwargs):
        """
        URL helper that handles Django URL reversal for Jinja2 templates.

        Converts template calls like url('name', key=value) to reverse('name', kwargs={'key': 'value'})
        """
        try:
            if args:
                return reverse(viewname, args=args)
            elif kwargs:
                return reverse(viewname, kwargs=kwargs)
            else:
                return reverse(viewname)
        except NoReverseMatch:
            return f"#URL-ERROR:{viewname}"

    def _get_validated_viewname(self, instance, action):
        """
        Replicate the validated_viewname filter functionality.
        Returns viewname if valid, None if invalid.
        """

        try:
            viewname_str = lookup.get_route_for_model(instance, action)
            # Validate the view name
            reverse(viewname_str)
            return viewname_str
        except (NoReverseMatch, AttributeError):
            return None

    def _get_user_info(self, instance, field_type):
        """
        Get user information for created/updated fields using Nautobot's helper function.
        """

        created_by, last_updated_by = get_created_and_last_updated_usernames_for_model(instance)

        if field_type == "created":
            return created_by
        else:
            return last_updated_by

    def get_template_name(self):
        """
        Override template selection to use Jinja2 templates.

        Converts standard Django template paths to Jinja2 equivalents
        and forces the use of the "jinja" template engine.
        """
        # Get the standard template name from parent
        django_template_name = super().get_template_name()

        # Convert Django template path to Jinja2 path
        # e.g., "dcim/location_retrieve.html" -> "dcim/location_retrieve.html"
        # (since our Jinja2 templates are in templates_jinja/dcim/ directories)
        jinja_template_name = django_template_name

        return jinja_template_name

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to use Jinja2 template engine.

        We need to override at this level because the NautobotHTMLRenderer
        handles template resolution before render_to_response gets called.
        """
        print("Retrieve called")
        try:
            # Get the object and build basic context
            instance = self.get_object()

            # Build a comprehensive context for Jinja2 to match Django templates

            context = {
                "object": instance,
                "request": request,
                "user": request.user,
                "settings": settings,
                # Add permissions context like Django does
                "perms": self._build_permissions_context(request.user),
                # Add messages
                "messages": messages.get_messages(request),
                # Add URL function for Jinja2 that handles kwargs properly
                "url": self._url_helper,
                # Add Django context processor data (safely access _meta)
                "verbose_name": getattr(instance._meta, "verbose_name", "Object"),
                "verbose_name_plural": getattr(instance._meta, "verbose_name_plural", "Objects"),
                # Add list_url for proper breadcrumbs
                "list_url": self._get_validated_viewname(instance, "list"),
                # Add created/updated user info for advanced panel
                "created_by": self._get_user_info(instance, "created"),
                "last_updated_by": self._get_user_info(instance, "updated"),
                # Phase 2: Pre-compute ALL method calls (basic + advanced)
                "custom_fields_basic": instance.get_custom_field_groupings_basic(),
                "computed_fields_basic": instance.get_computed_fields_grouping_basic(),
                "relationships_basic": instance.get_relationships_data_basic_fields(),
                "custom_fields_advanced": instance.get_custom_field_groupings_advanced(),
                "computed_fields_advanced": instance.get_computed_fields_grouping_advanced(),
                "relationships_advanced": instance.get_relationships_data_advanced_fields(),
            }

            # Add our custom context
            extra_context = self.get_extra_context(request, instance)
            context.update(extra_context)

            # Get template name
            template_name = self.get_template_name()
            print(f"Template name: {template_name}")
            # Use direct Jinja2 approach with proper engine
            try:
                jinja_engine = engines["jinja"]  # Use jinja engine with all filters registered
                start_time = time.time()
                jinja_template = jinja_engine.env.get_template(template_name)
                template_load_time = time.time()
                render_start = time.time()

                print(f"Loaded template in {template_load_time - render_start:.3f}s")

                content = jinja_template.render(context)
                render_time = time.time()
                print(f"Rendered template in {render_time - template_load_time:.3f}s")
                print(f"Total time: {render_time - start_time:.3f}s")
                print(f"Engine class: {jinja_engine.env.__class__.__name__}")

                content = f"<!-- RENDERED WITH JINJA2 UNSANDBOXED (WITH FILTERS) -->\n{content}"
                return HttpResponse(content)

            except Exception as jinja_e:
                print(f"Jinja2 template error: {jinja_e}")
                # Fallback to Django template
                return super().retrieve(request, *args, **kwargs)

        except Exception as e:
            # Fallback to Django template for any unexpected errors
            print(f"Error: {e}")
            return super().retrieve(request, *args, **kwargs)
