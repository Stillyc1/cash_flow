from cash_flow.forms import StatusForm, TypeForm, CategoryForm, SubCategoryForm
from cash_flow.models import Status, Type, Category, SubCategory


def get_model_and_form_class(model_name):
    """Вынесена функция в сервисный слой, для динамического определения Model и form_class для views."""
    if model_name == 'status':
        return Status, StatusForm
    elif model_name == 'type':
        return Type, TypeForm
    elif model_name == 'category':
        return Category, CategoryForm
    elif model_name == 'sub_category':
        return SubCategory, SubCategoryForm
    else:
        raise ValueError("Неправильное название модели.")
