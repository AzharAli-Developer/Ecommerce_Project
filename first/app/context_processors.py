# core/context_processors.py

from .models import Cart

def cart_length(request):
    if request.user.is_authenticated:
        user = request.user
        length = Cart.objects.filter(user=user).count()
    else:
        length = 0
    return {'cart_length': length}
