from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Book, Sale, SaleItem
from djmoney.money import Money

# Create your views here.

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f"{book.title} ajouté au panier.")
    return redirect('sales:view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('book').all()
    total = sum(item.book.price * item.quantity for item in items)
    return render(request, 'sales/cart.html', {'cart': cart, 'items': items, 'total': total})

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
            messages.success(request, "Quantité mise à jour.")
        else:
            item.delete()
            messages.success(request, "Article supprimé du panier.")
    return redirect('sales:view_cart')

@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Article supprimé du panier.")
    return redirect('sales:view_cart')

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('book').all()
    if not items:
        messages.warning(request, "Votre panier est vide.")
        return redirect('sales:view_cart')
    # Calcul du total
    total = sum(item.book.price * item.quantity for item in items)
    # Création de la vente
    sale = Sale.objects.create(user=request.user, total=total, status='completed')
    for item in items:
        SaleItem.objects.create(sale=sale, book=item.book, quantity=item.quantity, unit_price=item.book.price)
        # Optionnel : décrémenter le stock
        item.book.stock = max(0, item.book.stock - item.quantity)
        item.book.save()
    # Vider le panier
    items.delete()
    messages.success(request, "Votre commande a été validée avec succès.")
    return redirect('sales:order_history')

@login_required
def order_history(request):
    orders = Sale.objects.filter(user=request.user).order_by('-date')
    return render(request, 'sales/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Sale, pk=order_id, user=request.user)
    items = order.items.select_related('book').all()
    return render(request, 'sales/order_detail.html', {'order': order, 'items': items})
