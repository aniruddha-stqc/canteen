from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML

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


from .models import Customer, Thali, Extra  # Import your models

from .models import Category  # Import the Category model

def daily_lunch(request):
    # Fetch customer data
    customers = Customer.objects.all().values('name', 'mobile')

    # Fetch category data
    categories = Category.objects.all().values('category_name')  # Adjust fields as needed for Category model

    # Fetch Thali data
    thali = Thali.objects.all().values('category')  # Adjust fields as needed for Thali model

    # Fetch Extra data
    extras = Extra.objects.all().values('short_name', 'long_name', 'price')  # Correct field names

    # Pass data to the template
    return render(request, 'orders/daily_lunch.html', {
        'customers': list(customers),
        'categories': list(categories),  # Use categories instead of concessions
        'thalis': list(thali),
        'extras': list(extras),
    })

from .models import Customer, Category, Thali, Extra  # Import Category instead of Concession

def mealrequisition(request):
    # Fetch customer data
    customers = Customer.objects.all().values('name', 'mobile')

    # Fetch category data (instead of concession)
    categories = Category.objects.all()  # Fetch categories instead of concessions

    # Fetch Thali data
    thali = Thali.objects.all()  # Fetch Thali data

    # Fetch Extra data
    extras = Extra.objects.all()  # Fetch all extras

    # Pass data to the template
    return render(request, 'orders/Mealrequisition.html', {
        'extras': extras,
        'customers': list(customers),
        'categories': categories,  # Pass categories instead of concessions
        'thalis': thali
    })


from django.shortcuts import redirect
from .models import Wallet
from .forms import WalletTopUpForm

def wallet_top_up(request):
    success_message = ""
    error_message = ""

    if request.method == "POST":
        form = WalletTopUpForm(request.POST)
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile']
            credit_amount = form.cleaned_data['credit']

            if credit_amount <= 0:
                error_message = "Top-up amount must be greater than zero."
            else:
                try:
                    last_wallet = Wallet.objects.filter(mobile=mobile_number).order_by('-transaction_time').first()
                    new_balance = last_wallet.balance + credit_amount if last_wallet else credit_amount

                    Wallet.objects.create(
                        mobile=mobile_number,
                        transaction="Top-Up",
                        credit=credit_amount,
                        balance=new_balance
                    )

                    success_message = f"Top-up successful! New balance: ₹{new_balance}"

                except Exception as e:
                    error_message = f"An error occurred while processing your top-up: {str(e)}"

    else:
        form = WalletTopUpForm()

    return render(request, "wallet_topup.html", {
        "form": form,
        "success_message": success_message,
        "error_message": error_message,
    })



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomerForm


def add_customer(request):

    if request.method == 'POST':
        # Instantiate the form with POST data
        form = CustomerForm(request.POST)

        # Check if it's a confirmation action
        if 'confirm' in request.POST:
            print("Form data:", request.POST)  # Log submitted form data
            if form.is_valid():

                # Check if all required fields are present and valid
                mobile = form.cleaned_data.get('mobile')
                name = form.cleaned_data.get('name')
                category = form.cleaned_data.get('category')
                email = form.cleaned_data.get('email')

                # Ensure that mobile, name, and category are not empty
                if not mobile or not name or not category:
                    messages.error(request, "All required fields (mobile, name, category) must be filled out.")
                    return render(request, 'add_customer.html', {
                        'form': form,
                        'mobile': mobile,
                        'name': name,
                        'category': category,
                        'email': email,
                        'confirmation': True
                    })


                try:
                    # Save the form data to create a new customer
                    form.save()

                    # Add a success message for the user
                    messages.success(request, "Customer added successfully!")

                    # Redirect to the same page or another success page
                    return redirect('add_customer')  # Replace with your redirect URL
                except Exception as e:
                    # Handle any exceptions that occur during saving
                    messages.error(request, f"An error occurred while adding the customer: {str(e)}")
            else:
                # If the form is not valid, send error messages for the form fields
                for field in form.errors:
                    messages.error(request, f"Error in {field}: {form.errors[field]}")
        # Check if it's a cancel action
        elif 'cancel' in request.POST:
            # Redirect back to the previous page (no changes are saved)
            return redirect('add_customer')  # Replace with your previous view

        # If form is valid and not a confirmation or cancel, display the confirmation card
        if form.is_valid() and not ('confirm' in request.POST or 'cancel' in request.POST):
            return render(request, 'add_customer.html', {
                'form': form,
                'mobile': form.cleaned_data['mobile'],
                'name': form.cleaned_data['name'],
                'category': form.cleaned_data['category'],
                'email': form.cleaned_data['email'],
                'confirmation': True
            })
    else:
        # If it's a GET request, just display the empty form
        form = CustomerForm()

    # Render the template with the form and any messages
    return render(request, 'add_customer.html', {'form': form, 'confirmation': False})


from django.shortcuts import render, redirect
from .forms import CategoryForm

from django.shortcuts import render, redirect
from .forms import CategoryForm

def add_category(request):


    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Save the category with the manually entered category_id
            form.save()
            return render(request, 'add_category.html', {'form': form, 'success_message': 'Category added successfully!'})
        else:
            return render(request, 'add_category.html', {'form': form, 'error_message': 'There was an error in your form. Please check your inputs.'})
    else:
        form = CategoryForm()
        return render(request, 'add_category.html', {'form': form})

