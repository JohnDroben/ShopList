from .models import Category

def categories(request):
    return {'all_categories': Category.objects.all()}