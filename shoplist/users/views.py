from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from cart.models import Order

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})


@login_required
def profile(request):
    total_spent = sum(order.total_amount for order in request.user.order_set.all())
    return render(request, 'users/profile.html', {'total_spent': total_spent})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/order_history.html', {'orders': orders})