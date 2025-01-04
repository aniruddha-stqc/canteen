from django.shortcuts import render
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from .models import Order  # Import the Order model

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

          # Render your HTML template to a string with the separated orders context
        html_content = render_to_string('orders/order_pdf.html', {
            'orders_nv': orders_nv,
            'orders_vg': orders_vg
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


