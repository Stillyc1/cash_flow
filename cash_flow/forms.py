from django import forms
from django.utils import timezone

from cash_flow.models import CashFlow, Category, SubCategory, Type, Status


class CashFlowForm(forms.ModelForm):
    """Форма создания записи ДДС, со стилизацией полей."""

    created_at = forms.DateField(
        label="Дата создания записи",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=timezone.now().date()
    )  # Вывод календаря в форме для возможности выбора даты

    def __init__(self, *args, **kwargs):
        super(CashFlowForm, self).__init__(*args, **kwargs)

        self.fields["status"].widget.attrs.update(
            {"class": "form-select", "placeholder": "Статус"}
        )
        self.fields["type"].widget.attrs.update(
            {"class": "form-select",
             "required": True}  # Валидация полей на стороне клиента
        )
        self.fields["category"].widget.attrs.update(
            {"class": "form-select",
             "onchange": "this.form.submit()",
             # Выбор категории отправляет GET Запрос и тем самым мы фильтруем подкатегории
             "name": "category",
             "required": True}
        )
        self.fields["category_sub"].widget.attrs.update(
            {"class": "form-select",
             "required": True}
        )
        self.fields["count"].widget.attrs.update(
            {"class": "form-control",
             "placeholder": "Введите сумму",
             "required": True}
        )
        self.fields["comment"].widget.attrs.update(
            {"class": "form-control",
             "placeholder": "Дополнительная информация..."}
        )

    class Meta:
        model = CashFlow
        fields = "__all__"

    def clean(self):
        """Валидация данных"""
        cleaned_data = super().clean()
        type_ = cleaned_data.get("type")
        category = cleaned_data.get("category")

        # Производим валидацию подкатегорий, пользователь сможет выбрать только связанные с Категорией.
        if category:
            self.fields["category_sub"].queryset = SubCategory.objects.filter(parent_category__name=category)

        if type_ and category:
            instance_type = Type.objects.filter(name=type_).first()
            instance_category = Category.objects.filter(name=category).first()
            if instance_category.parent_type != instance_type:
                self.add_error("category", f"Данная категория не относится к выбранному типу '{type_}'")


class StatusForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Название"}
        )

    class Meta:
        model = Status
        fields = "__all__"


class TypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TypeForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Название"}
        )

    class Meta:
        model = Type
        fields = "__all__"


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Название"}
        )
        self.fields["parent_type"].widget.attrs.update(
            {"class": "form-select"}
        )

    class Meta:
        model = Category
        fields = "__all__"


class SubCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Название"}
        )
        self.fields["parent_category"].widget.attrs.update(
            {"class": "form-select"}
        )

    class Meta:
        model = SubCategory
        fields = "__all__"
