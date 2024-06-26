# Generated by Django 3.2.25 on 2024-05-03 14:57

import uuid

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion

import nautobot.core.models.fields
import nautobot.core.models.ordering
import nautobot.core.models.query_functions
import nautobot.extras.models.mixins
import nautobot.extras.models.roles
import nautobot.extras.models.statuses


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0109_staticgroup_staticgroupassociation"),
        ("tenancy", "0009_update_all_charfields_max_length_to_255"),
        ("dcim", "0060_alter_cable_status_alter_consoleport__path_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("serial", models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ("asset_tag", models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="ModuleBay",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("position", models.CharField(blank=True, max_length=255)),
                ("name", models.CharField(max_length=255, db_index=True)),
                (
                    "_name",
                    nautobot.core.models.fields.NaturalOrderingField(
                        "name",
                        blank=True,
                        db_index=True,
                        max_length=255,
                        naturalize_function=nautobot.core.models.ordering.naturalize,
                    ),
                ),
                ("label", models.CharField(blank=True, max_length=255)),
                ("description", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "abstract": False,
            },
            bases=(
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
                models.Model,
            ),
        ),
        migrations.CreateModel(
            name="ModuleBayTemplate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("position", models.CharField(blank=True, max_length=255)),
                ("name", models.CharField(max_length=255)),
                (
                    "_name",
                    nautobot.core.models.fields.NaturalOrderingField(
                        "name",
                        blank=True,
                        max_length=255,
                        naturalize_function=nautobot.core.models.ordering.naturalize,
                    ),
                ),
                ("label", models.CharField(blank=True, max_length=255)),
                ("description", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ModuleType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("model", models.CharField(max_length=255)),
                ("part_number", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "ordering": ("manufacturer", "model"),
            },
            bases=(
                nautobot.extras.models.mixins.DynamicGroupMixin,
                nautobot.extras.models.mixins.NotesMixin,
                models.Model,
            ),
        ),
        migrations.AddField(
            model_name="moduletype",
            name="manufacturer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="module_types", to="dcim.manufacturer"
            ),
        ),
        migrations.AddField(
            model_name="moduletype",
            name="tags",
            field=nautobot.core.models.fields.TagsField(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AddField(
            model_name="modulebaytemplate",
            name="device_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="dcim.devicetype"
            ),
        ),
        migrations.AddField(
            model_name="modulebaytemplate",
            name="module_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="dcim.moduletype"
            ),
        ),
        migrations.AddField(
            model_name="modulebay",
            name="parent_device",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="module_bays",
                to="dcim.device",
            ),
        ),
        migrations.AddField(
            model_name="modulebay",
            name="parent_module",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="module_bays",
                to="dcim.module",
            ),
        ),
        migrations.AddField(
            model_name="modulebay",
            name="tags",
            field=nautobot.core.models.fields.TagsField(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AddField(
            model_name="module",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="modules",
                to="dcim.location",
            ),
        ),
        migrations.AddField(
            model_name="module",
            name="module_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="modules", to="dcim.moduletype"
            ),
        ),
        migrations.AddField(
            model_name="module",
            name="parent_module_bay",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="installed_module",
                to="dcim.modulebay",
            ),
        ),
        migrations.AddField(
            model_name="module",
            name="role",
            field=nautobot.extras.models.roles.RoleField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="extras.role",
            ),
        ),
        migrations.AddField(
            model_name="module",
            name="status",
            field=nautobot.extras.models.statuses.StatusField(
                on_delete=django.db.models.deletion.PROTECT, to="extras.status"
            ),
        ),
        migrations.AddField(
            model_name="module",
            name="tags",
            field=nautobot.core.models.fields.TagsField(through="extras.TaggedItem", to="extras.Tag"),
        ),
        migrations.AddField(
            model_name="module",
            name="tenant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="modules",
                to="tenancy.tenant",
            ),
        ),
        migrations.AddField(
            model_name="consoleport",
            name="module",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.module",
            ),
        ),
        migrations.AddField(
            model_name="consoleporttemplate",
            name="module_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.moduletype",
            ),
        ),
        migrations.AddField(
            model_name="consoleserverport",
            name="module",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.module",
            ),
        ),
        migrations.AddField(
            model_name="consoleserverporttemplate",
            name="module_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.moduletype",
            ),
        ),
        migrations.AddField(
            model_name="frontport",
            name="module",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.module",
            ),
        ),
        migrations.AddField(
            model_name="frontporttemplate",
            name="module_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.moduletype",
            ),
        ),
        migrations.AddField(
            model_name="interface",
            name="module",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.module",
            ),
        ),
        migrations.AddField(
            model_name="interfacetemplate",
            name="module_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.moduletype",
            ),
        ),
        migrations.AddField(
            model_name="poweroutlet",
            name="module",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.module",
            ),
        ),
        migrations.AddField(
            model_name="poweroutlettemplate",
            name="module_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.moduletype",
            ),
        ),
        migrations.AddField(
            model_name="powerport",
            name="module",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.module",
            ),
        ),
        migrations.AddField(
            model_name="powerporttemplate",
            name="module_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.moduletype",
            ),
        ),
        migrations.AddField(
            model_name="rearport",
            name="module",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.module",
            ),
        ),
        migrations.AddField(
            model_name="rearporttemplate",
            name="module_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.moduletype",
            ),
        ),
        migrations.AlterModelOptions(
            name="consoleporttemplate",
            options={"ordering": ("device_type", "module_type", "_name")},
        ),
        migrations.AlterModelOptions(
            name="consoleserverporttemplate",
            options={"ordering": ("device_type", "module_type", "_name")},
        ),
        migrations.AlterModelOptions(
            name="frontporttemplate",
            options={"ordering": ("device_type", "module_type", "_name")},
        ),
        migrations.AlterModelOptions(
            name="interfacetemplate",
            options={"ordering": ("device_type", "module_type", "_name")},
        ),
        migrations.AlterModelOptions(
            name="poweroutlettemplate",
            options={"ordering": ("device_type", "module_type", "_name")},
        ),
        migrations.AlterModelOptions(
            name="powerporttemplate",
            options={"ordering": ("device_type", "module_type", "_name")},
        ),
        migrations.AlterModelOptions(
            name="rearporttemplate",
            options={"ordering": ("device_type", "module_type", "_name")},
        ),
        migrations.AlterModelOptions(
            name="consoleport",
            options={"ordering": ("device", "module", "_name")},
        ),
        migrations.AlterModelOptions(
            name="consoleserverport",
            options={"ordering": ("device", "module", "_name")},
        ),
        migrations.AlterModelOptions(
            name="frontport",
            options={"ordering": ("device", "module", "_name")},
        ),
        migrations.AlterModelOptions(
            name="poweroutlet",
            options={"ordering": ("device", "module", "_name")},
        ),
        migrations.AlterModelOptions(
            name="powerport",
            options={"ordering": ("device", "module", "_name")},
        ),
        migrations.AlterModelOptions(
            name="rearport",
            options={"ordering": ("device", "module", "_name")},
        ),
        migrations.AlterModelOptions(
            name="interface",
            options={"ordering": ("device", "module", nautobot.core.models.query_functions.CollateAsChar("_name"))},
        ),
        migrations.AlterField(
            model_name="consoleport",
            name="device",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.device",
            ),
        ),
        migrations.AlterField(
            model_name="consoleporttemplate",
            name="device_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.devicetype",
            ),
        ),
        migrations.AlterField(
            model_name="consoleserverport",
            name="device",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.device",
            ),
        ),
        migrations.AlterField(
            model_name="consoleserverporttemplate",
            name="device_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.devicetype",
            ),
        ),
        migrations.AlterField(
            model_name="frontport",
            name="device",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.device",
            ),
        ),
        migrations.AlterField(
            model_name="frontporttemplate",
            name="device_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.devicetype",
            ),
        ),
        migrations.AlterField(
            model_name="interface",
            name="device",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.device",
            ),
        ),
        migrations.AlterField(
            model_name="interfacetemplate",
            name="device_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.devicetype",
            ),
        ),
        migrations.AlterField(
            model_name="poweroutlet",
            name="device",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.device",
            ),
        ),
        migrations.AlterField(
            model_name="poweroutlettemplate",
            name="device_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.devicetype",
            ),
        ),
        migrations.AlterField(
            model_name="powerport",
            name="device",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.device",
            ),
        ),
        migrations.AlterField(
            model_name="powerporttemplate",
            name="device_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.devicetype",
            ),
        ),
        migrations.AlterField(
            model_name="rearport",
            name="device",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.device",
            ),
        ),
        migrations.AlterField(
            model_name="rearporttemplate",
            name="device_type",
            field=nautobot.core.models.fields.ForeignKeyWithAutoRelatedName(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dcim.devicetype",
            ),
        ),
        migrations.AddConstraint(
            model_name="consoleporttemplate",
            constraint=models.UniqueConstraint(
                fields=("device_type", "name"), name="dcim_consoleporttemplate_device_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="consoleporttemplate",
            constraint=models.UniqueConstraint(
                fields=("module_type", "name"), name="dcim_consoleporttemplate_module_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="consoleserverporttemplate",
            constraint=models.UniqueConstraint(
                fields=("device_type", "name"), name="dcim_consoleserverporttemplate_device_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="consoleserverporttemplate",
            constraint=models.UniqueConstraint(
                fields=("module_type", "name"), name="dcim_consoleserverporttemplate_module_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="frontporttemplate",
            constraint=models.UniqueConstraint(
                fields=("device_type", "name"), name="dcim_frontporttemplate_device_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="frontporttemplate",
            constraint=models.UniqueConstraint(
                fields=("module_type", "name"), name="dcim_frontporttemplate_module_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="frontporttemplate",
            constraint=models.UniqueConstraint(
                fields=("rear_port_template", "rear_port_position"),
                name="dcim_frontporttemplate_rear_port_template_position_unique",
            ),
        ),
        migrations.AddConstraint(
            model_name="interfacetemplate",
            constraint=models.UniqueConstraint(
                fields=("device_type", "name"), name="dcim_interfacetemplate_device_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="interfacetemplate",
            constraint=models.UniqueConstraint(
                fields=("module_type", "name"), name="dcim_interfacetemplate_module_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="poweroutlettemplate",
            constraint=models.UniqueConstraint(
                fields=("device_type", "name"), name="dcim_poweroutlettemplate_device_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="poweroutlettemplate",
            constraint=models.UniqueConstraint(
                fields=("module_type", "name"), name="dcim_poweroutlettemplate_module_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="powerporttemplate",
            constraint=models.UniqueConstraint(
                fields=("device_type", "name"), name="dcim_powerporttemplate_device_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="powerporttemplate",
            constraint=models.UniqueConstraint(
                fields=("module_type", "name"), name="dcim_powerporttemplate_module_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="rearporttemplate",
            constraint=models.UniqueConstraint(
                fields=("device_type", "name"), name="dcim_rearporttemplate_device_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="rearporttemplate",
            constraint=models.UniqueConstraint(
                fields=("module_type", "name"), name="dcim_rearporttemplate_module_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="consoleport",
            constraint=models.UniqueConstraint(fields=("device", "name"), name="dcim_consoleport_device_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="consoleport",
            constraint=models.UniqueConstraint(fields=("module", "name"), name="dcim_consoleport_module_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="consoleserverport",
            constraint=models.UniqueConstraint(
                fields=("device", "name"), name="dcim_consoleserverport_device_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="consoleserverport",
            constraint=models.UniqueConstraint(
                fields=("module", "name"), name="dcim_consoleserverport_module_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="frontport",
            constraint=models.UniqueConstraint(fields=("device", "name"), name="dcim_frontport_device_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="frontport",
            constraint=models.UniqueConstraint(fields=("module", "name"), name="dcim_frontport_module_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="frontport",
            constraint=models.UniqueConstraint(
                fields=("rear_port", "rear_port_position"), name="dcim_frontport_rear_port_position_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="interface",
            constraint=models.UniqueConstraint(fields=("device", "name"), name="dcim_interface_device_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="interface",
            constraint=models.UniqueConstraint(fields=("module", "name"), name="dcim_interface_module_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="poweroutlet",
            constraint=models.UniqueConstraint(fields=("device", "name"), name="dcim_poweroutlet_device_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="poweroutlet",
            constraint=models.UniqueConstraint(fields=("module", "name"), name="dcim_poweroutlet_module_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="powerport",
            constraint=models.UniqueConstraint(fields=("device", "name"), name="dcim_powerport_device_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="powerport",
            constraint=models.UniqueConstraint(fields=("module", "name"), name="dcim_powerport_module_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="rearport",
            constraint=models.UniqueConstraint(fields=("device", "name"), name="dcim_rearport_device_name_unique"),
        ),
        migrations.AddConstraint(
            model_name="rearport",
            constraint=models.UniqueConstraint(fields=("module", "name"), name="dcim_rearport_module_name_unique"),
        ),
        migrations.AlterUniqueTogether(
            name="moduletype",
            unique_together={("manufacturer", "model")},
        ),
        migrations.AlterModelOptions(
            name="module",
            options={"ordering": ("parent_module_bay", "location", "module_type", "asset_tag", "serial")},
        ),
        migrations.AlterModelOptions(
            name="modulebay",
            options={"ordering": ("parent_device", "parent_module__id", "_name")},
        ),
        migrations.AlterModelOptions(
            name="modulebaytemplate",
            options={"ordering": ("device_type", "module_type", "_name")},
        ),
        migrations.AddConstraint(
            model_name="module",
            constraint=models.UniqueConstraint(
                fields=("module_type", "serial"), name="dcim_module_module_type_serial_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="modulebay",
            constraint=models.UniqueConstraint(
                fields=("parent_device", "name"), name="dcim_modulebay_parent_device_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="modulebay",
            constraint=models.UniqueConstraint(
                fields=("parent_module", "name"), name="dcim_modulebay_parent_module_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="modulebaytemplate",
            constraint=models.UniqueConstraint(
                fields=("device_type", "name"), name="dcim_modulebaytemplate_device_type_name_unique"
            ),
        ),
        migrations.AddConstraint(
            model_name="modulebaytemplate",
            constraint=models.UniqueConstraint(
                fields=("module_type", "name"), name="dcim_modulebaytemplate_module_type_name_unique"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="consoleporttemplate",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="consoleserverporttemplate",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="frontporttemplate",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="interfacetemplate",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="poweroutlettemplate",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="powerporttemplate",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="rearporttemplate",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="consoleport",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="consoleserverport",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="frontport",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="interface",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="poweroutlet",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="powerport",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="rearport",
            unique_together=set(),
        ),
    ]
