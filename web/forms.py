from django import forms
from .models import Wallet

from django import forms
from .models import Wallet, Customer
from datetime import datetime


class WalletTopUpForm(forms.ModelForm):
    mobile = forms.CharField(max_length=10)  # Take mobile as a string input

    class Meta:
        model = Wallet
        fields = ['mobile', 'credit']  # Include the necessary fields for the form

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')

        # Ensure mobile is exactly 10 digits and contains only numbers
        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")

        # Ensure mobile is exactly 10 digits
        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number must be 10 digits.")

        # Check if the mobile number exists in the Customer table
        try:
            customer = Customer.objects.get(mobile=mobile)
        except Customer.DoesNotExist:
            raise forms.ValidationError("No customer found with this mobile number.")

        # If customer exists, return the customer instance instead of just the mobile string
        #print(f"clean_mobile: Mobile number is valid: {mobile}")
        return customer  # Returning the Customer instance

    def clean_credit(self):
        credit = self.cleaned_data['credit']
        # Ensure that credit is a positive integer
        if credit <= 0:
            raise forms.ValidationError("Credit amount must be a positive number.")
        return credit

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Convert mobile string into a Customer instance
        customer = Customer.objects.get(mobile=self.cleaned_data['mobile'])
        # Retrieve the customer instance by mobile
        # Assign the Customer instance to the Wallet instance
        instance.mobile = customer

        # Set initial balance equal to the credit amount
        instance.balance = instance.credit

        # Ensure a unique transaction_time for each top-up
        instance.transaction_time = datetime.now().strftime('%Y%m%d%H%M%S')

        if commit:
            instance.save()

        return instance



from django import forms
from .models import Customer, Category


class CustomerForm(forms.ModelForm):


    class Meta:
        model = Customer
        fields = ['mobile', 'name', 'email', 'category']  # Fields to include in the form

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Ensure name contains only alphabetic characters and spaces
        if not name.replace(" ", "").isalpha():
            raise forms.ValidationError("Name must contain only letters.")

        return name

    # Additional validations can be added if needed
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        # Ensure mobile is exactly 10 digits and contains only numbers
        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")

        # Ensure mobile is exactly 10 digits
        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number must be 10 digits.")

        # Optionally: You could add more validations for the mobile number format

        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Optional: Validate if email is not empty if provided
        if email and len(email) < 5:
            raise forms.ValidationError("Please enter a valid email address.")

        return email

    def clean_category(self):
        category = self.cleaned_data.get('category')

        # Optional: Ensure category is selected, if any additional validation is needed
        if not category:
            raise forms.ValidationError("Category must be selected.")

        return category


from django import forms
from .models import Category
from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']  # Include category_id and category_name

    category_id = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category ID'})
    )

    category_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category Name'})
    )

