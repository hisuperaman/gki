from .models import NewUpdate

def new_updates_processor(request):
    new_updates = NewUpdate.objects.all().order_by('-date')
    return {
        'base_new_updates': new_updates
    }