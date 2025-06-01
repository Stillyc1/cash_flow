from django.contrib import admin

from cash_flow.models import Status, Type, Category, CashFlow, SubCategory


@admin.register(Status, Type)
class StatusTypeAdmin(admin.ModelAdmin):
    """Объекты models.py: Status, Type; для админ-панели."""

    list_display = ("id", "name",)
    list_filter = ("name",)
    search_fields = ("id", "name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Объекты models.py: Status, Type; для админ-панели."""

    list_display = ("id", "name", "parent_type",)
    list_filter = ("name", "parent_type",)
    search_fields = ("id", "name", "parent_type",)


@admin.register(SubCategory)
class CategoryAdmin(admin.ModelAdmin):
    """Объекты models.py: Status, Type; для админ-панели."""

    list_display = ("id", "name", "parent_category",)
    list_filter = ("name", "parent_category",)
    search_fields = ("id", "name", "parent_category",)


@admin.register(CashFlow)
class SubAdmin(admin.ModelAdmin):
    """Объекты models.py: Status, Type, Category; для админ-панели."""

    list_display = (
        "id",
        "created_at",
        "status",
        "type",
        "category",
        "category_sub",
        "count",
        "comment",
    )
    list_filter = (
        "created_at",
        "status",
    )
    search_fields = ("id", "status",)
