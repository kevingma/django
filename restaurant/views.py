from django.shortcuts import render, redirect
import random
from datetime import datetime, timedelta

# Create your views here.
def main(request):
    return render(request, 'voter_analytics/main.html')

def order(request):
    specials = ['SPECIAL: Canned Soup', 'SPECIAL: Lunchables',
        'SPECIAL: White Rice', 'SPECIAL: Toast',]
    daily_special = random.choice(specials)
    context = {'daily_special': daily_special}
    return render(request, 'voter_analytics/order.html', context)


def confirmation(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '')
        customer_phone = request.POST.get('customer_phone', '')
        customer_email = request.POST.get('customer_email', '')
        special_instructions = request.POST.get('special_instructions', '')

        menu_items = [
            {'name': 'Cheeseburger', 'price': 8}, {'name': 'Big Mac', 'price': 11}, {'name': 'Burrito', 'price': 14},
            {'name': 'Chopped Cheese', 'price': 17}, {'name': 'Grabba Sandwich', 'price': 12},]
        ordered_items = []
        total_price = 0

        for item in menu_items:
            if request.POST.get(item['name']):
                ordered_items.append(item)
                total_price += item['price']

        if request.POST.get('Cheeseburger'):
            toppings = request.POST.getlist('toppings')
            if toppings:
                toppings_str = ', '.join(toppings)
                ordered_items.append({'name': 'Toppings for Cheeseburger: ' + toppings_str, 'price': len(toppings)})
                total_price += len(toppings)

        daily_special_name = request.POST.get('ds')
        daily_special_price = request.POST.get('ds_price')
        if request.POST.get('Daily Special'):
            daily_special = {
                'name': daily_special_name,
                'price': float(daily_special_price)
            }
            ordered_items.append(daily_special)
            total_price += daily_special['price']

        minutes_to_add = random.randint(30, 60)
        ready_time = datetime.now() + timedelta(minutes=minutes_to_add)
        ready_time_fixed = ready_time.strftime('%I:%M %p')

        context = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'total_price': total_price,
            'ready_time': ready_time_fixed,
        }
        return render(request, 'voter_analytics/confirmation.html', context)
    else:
        return redirect('order')
