from nautobot.dcim.models import Location


class ProxyLocation(Location):
    class Meta:
        app_label = "dcim"
        proxy = True
