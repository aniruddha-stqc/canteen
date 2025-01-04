from django.shortcuts import render
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string

# Create your views here.
from .models import Order  # Import the Order model

# View to display all orders
def order_list(request):
    # Retrieve all orders from the database
    orders = Order.objects.all()

    # Pass orders to the template
    return render(request, 'orders/order_list.html', {'orders': orders})


from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from .models import Order  # Ensure your Order model is correctly imported

def generate_pdf(request):
    try:
        # Retrieve all orders from the database
        orders = Order.objects.all()

        # Check if there are orders; otherwise, handle the case appropriately
        if not orders:
            return HttpResponse("No orders found.", status=404)

        # Render your HTML template to a string with the orders context
        html_content = render_to_string('orders/order_pdf.html', {'orders': orders})

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

