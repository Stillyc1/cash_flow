from django.db import models


class SubField(models.Model):
    """Вынесен в родительский класс, атрибут 'name' и '__str__' для моделей (Status, Type, Category)."""

    name = models.CharField(max_length=150, unique=True, verbose_name="Название")

    def __str__(self):
        return f"{self.name}"


class Status(SubField):
    """Поле 'статус' в модели CashFlow."""

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Type(SubField):
    """Поле 'Тип' в модели CashFlow."""

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Category(SubField):
    """Поле 'Категория' в модели CashFlow."""

    parent_type = models.ForeignKey(
        Type, on_delete=models.CASCADE, related_name="categories", verbose_name="Тип"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(SubField):
    """Поле 'Подкатегория' в модели CashFlow."""

    parent_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="sub_categories",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class CashFlow(models.Model):
    """Создание модели: 'Запись о движении денежных средств (ДДС)'."""

    created_at = models.DateField(verbose_name="Дата создания записи", blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name="cash_flows",
        verbose_name="Статус",
        blank=True,
        null=True,
    )
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, related_name="cash_flows", verbose_name="Тип"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="cash_flows",
        verbose_name="Категория",
    )
    category_sub = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="cash_flows",
        verbose_name="Подкатегория",
    )
    count = models.PositiveIntegerField(verbose_name="Сумма")
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"

    def __str__(self):
        return f"Запись ДДС: №{self.pk}"
