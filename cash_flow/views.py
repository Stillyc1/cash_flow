from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from cash_flow.forms import CashFlowForm
from cash_flow.models import CashFlow, Category, Status, SubCategory, Type
from cash_flow.services import get_model_and_form_class


class MainListView(ListView):
    """Главная страница со всеми записями ДДС, с возможностью фильтрации."""

    model = CashFlow
    template_name = "cash_flow/main.html"
    context_object_name = "cash_flows"

    def get_context_data(self, *, object_list=None, **kwargs):
        """Передаем в форму объекты для фильтрации."""
        context = super().get_context_data(**kwargs)

        context["status"] = Status.objects.all()
        context["type"] = Type.objects.all()
        context["categories"] = Category.objects.all()
        context["sub_categories"] = SubCategory.objects.all()

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по дате
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        if start_date and end_date:
            queryset = queryset.filter(created_at__range=[start_date, end_date])

        # Фильтрация по статусу
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status__name=status)

        # Фильтрация по типу
        type_ = self.request.GET.get("type")
        if type_:
            queryset = queryset.filter(type__name=type_)

        # Фильтрация по категории
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category__name=category)

        # Фильтрация по подкатегории
        subcategory = self.request.GET.get("subcategory")
        if subcategory:
            queryset = queryset.filter(category_sub__name=subcategory)

        return sorted(
            queryset, key=lambda x: x.created_at, reverse=True
        )  # Сортируем объекты по дате


class CashFlowCreateView(CreateView):
    form_class = CashFlowForm
    template_name = "cash_flow/create_cash_flow.html"
    success_url = reverse_lazy("cash_flow:main")


class CashFlowUpdateView(UpdateView):
    model = CashFlow
    form_class = CashFlowForm
    template_name = "cash_flow/create_cash_flow.html"
    success_url = reverse_lazy("cash_flow:main")


class CashFlowDeleteView(DeleteView):
    model = CashFlow
    template_name = "cash_flow/delete_cash_flow.html"
    success_url = reverse_lazy("cash_flow:main")


class ReferenceBooksListView(ListView):
    """Представление всех справочников (Статусы, Типы, Категории, Подкатегории)."""

    model = Status
    template_name = "cash_flow/reference_books.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context["all_status"] = Status.objects.all()
        context["all_type"] = Type.objects.all()
        context["all_category"] = Category.objects.all()
        context["all_sub_category"] = SubCategory.objects.all()

        return context


class ReferenceBooksCreateView(CreateView):
    """
    Создание объектов справочника,
    model и form_class динамически подставляется
    для каждого объекта справочника.
    """

    template_name = "cash_flow/reference_books_cud.html"
    model = None
    form_class = None
    success_url = reverse_lazy("cash_flow:reference_books")

    def get(self, request, *args, **kwargs):
        self.model, _ = get_model_and_form_class(f"{kwargs.get('model')}")
        return super().get(request, *args, **kwargs)

    def get_form_class(self):
        _, form_class = get_model_and_form_class(self.kwargs.get("model"))
        return form_class


class ReferenceBooksUpdateView(UpdateView):
    """
    Изменение объектов справочника,
    model и form_class динамически подставляется
    для каждого объекта справочника.
    """

    template_name = "cash_flow/reference_books_cud.html"
    model = None
    form_class = None
    success_url = reverse_lazy("cash_flow:reference_books")

    def get(self, request, *args, **kwargs):
        self.model, _ = get_model_and_form_class(f"{kwargs.get('model')}")
        return super().get(request, *args, **kwargs)

    def get_form_class(self):
        _, form_class = get_model_and_form_class(self.kwargs.get("model"))
        return form_class

    def get_queryset(self):
        model, _ = get_model_and_form_class(self.kwargs.get("model"))
        return model.objects.all()


class ReferenceBooksDeleteView(DeleteView):
    """
    Удаление объектов справочника,
    model и form_class динамически подставляется
    для каждого объекта справочника.
    """

    model = None
    template_name = "cash_flow/reference_books_delete.html"
    success_url = reverse_lazy("cash_flow:reference_books")

    def get(self, request, *args, **kwargs):
        self.model, _ = get_model_and_form_class(f"{kwargs.get('model')}")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        model, _ = get_model_and_form_class(self.kwargs.get("model"))
        return model.objects.all()
