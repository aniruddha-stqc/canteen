from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML
from .models import Order, Customer  # Import the Order model


# View to display all orders
def order_list(request):
    # Retrieve all orders from the database
    orders = Order.objects.all()

    # Pass orders to the template
    return render(request, 'orders/order_list.html', {'orders': orders})



def generate_pdf(request):
    try:
        # Retrieve all orders from the database
        orders = Order.objects.all()

        # Check if there are orders; otherwise, handle the case appropriately
        if not orders:
            return HttpResponse("No orders found.", status=404)

        # Separate orders into Non-Veg and Veg based on `thali_type`
        orders_nv = orders.filter(thali_type__startswith='NV_')
        orders_vg = orders.filter(thali_type__startswith='VG_')

        # Calculate the difference in lengths of the two lists
        len_nv = len(orders_nv)
        len_vg = len(orders_vg)
        # Calculate counts for Non-Veg Thali and Veg Thali
        non_veg_count = len_nv
        veg_count = len_vg
        # If the lists are not of the same length, add dummy rows
        if len_nv < len_vg:
            # Calculate how many rows to add to orders_nv
            diff = len_vg - len_nv
            dummy_rows = [None] * diff  # Create dummy rows
            orders_nv = list(orders_nv) + dummy_rows  # Append dummy rows to orders_nv
        elif len_nv > len_vg:
            # Calculate how many rows to add to orders_vg
            diff = len_nv - len_vg
            dummy_rows = [None] * diff  # Create dummy rows
            orders_vg = list(orders_vg) + dummy_rows  # Append dummy rows to orders_vg

        # Initialize counters for the extra items
        omelette_count = 0
        rice_count = 0
        sabji_count = 0
        dal_count = 0

        # Iterate through all orders to count the occurrences of extra items
        for order in orders:
            # Check the extra item columns for each order
            extra_items = [
                order.extra_item1, order.extra_item2, order.extra_item3, order.extra_item4
            ]

            # Loop through the extra items and update counts based on their prefixes
            for extra_item in extra_items:
                if extra_item and extra_item.startswith('OML_'):  # Check if the extra_item starts with 'OML_'
                    omelette_count += 1
                elif extra_item and extra_item.startswith('RIC_'):  # Check if the extra_item starts with 'RIC_'
                    rice_count += 1
                elif extra_item and extra_item.startswith('SBJ_'):  # Check if the extra_item starts with 'SBJ_'
                    sabji_count += 1
                elif extra_item and extra_item.startswith('DAL_'):  # Check if the extra_item starts with 'DAL_'
                    dal_count += 1

        # Calculate Total Payment, Via Cash, and Via Wallet
        total_payment = 0
        cash_payment = 0
        wallet_payment = 0

        for order in orders:
            if order.pay_mode == 'CASH':
                cash_payment += order.total_price
            elif order.pay_mode == 'WALL':
                wallet_payment += order.total_price

        total_payment = cash_payment + wallet_payment  # Total Payment is the sum of Cash and Wallet payments

        current_date = timezone.now()  # Get current date and time

        # Render your HTML template to a string with the separated orders context
        html_content = render_to_string('orders/order_pdf.html', {
            'orders_nv': orders_nv,
            'orders_vg': orders_vg,
            'now': current_date,
            'total_payment': total_payment,
            'cash_payment': cash_payment,
            'wallet_payment': wallet_payment,
            'non_veg_count': non_veg_count,  # Pass the Non-Veg Thali count
            'veg_count': veg_count,  # Pass the Veg Thali count
            'omelette_count': omelette_count,  # Pass the count for OMELETTE
            'rice_count': rice_count,  # Pass the count for EXTRA RICE
            'sabji_count': sabji_count,  # Pass the count for EXTRA SABJI
            'dal_count': dal_count  # Pass the count for EXTRA DAL
        })

        # Generate the PDF from the HTML content
        pdf = HTML(string=html_content).write_pdf()

        # Return the PDF as a response with the correct MIME type
        response = HttpResponse(pdf, content_type='application/pdf')

        # Set Content-Disposition to 'inline' to open in the browser instead of downloading
        response['Content-Disposition'] = 'inline; filename="order_report.pdf"'

        return response

    except Exception as e:
        # Handle any errors that occur during PDF generation
        return HttpResponse(f"An error occurred: {e}", status=500)


from django.shortcuts import render
from .models import Customer, Concession, Thali, Extra  # Import your models


def daily_lunch(request):
    # Fetch customer data
    customers = Customer.objects.all().values('name', 'mobile')

    # Fetch concession data from the Concession model
    concessions = Concession.objects.all()  # Adjust based on your model
    # Fetch Thali data from the Concession model
    thali = Thali.objects.all()  # Adjust based on your model
    extras = Extra.objects.all()  # Fetch all extras
    # Pass data to the template
    return render(request, 'orders/daily_lunch.html', {
        'extras': extras,
        'customers': list(customers),
        'concessions': concessions,
        'thalis': thali
    })



def mealrequisition(request):
    # Fetch customer data
    customers = Customer.objects.all().values('name', 'mobile')

    # Fetch concession data from the Concession model
    concessions = Concession.objects.all()  # Adjust based on your model
    # Fetch Thali data from the Concession model
    thali = Thali.objects.all()  # Adjust based on your model
    extras = Extra.objects.all()  # Fetch all extras
    # Pass data to the template
    return render(request, 'orders/Mealrequisition.html', {
        'extras': extras,
        'customers': list(customers),
        'concessions': concessions,
        'thalis': thali
    })


