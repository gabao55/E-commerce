def price_format(value):
    return f'$ {value:.2f}'

def cart_total_amount(cart):
    return sum([item['amount'] for item in cart.values()])

def cart_totals(cart):
    return sum(
        [
            item.get('quantitative_promotional_price')
            if item.get('quantitative_promotional_price')
            else item.get('quantitative_price')
            for item 
            in cart.values()
        ]
    )