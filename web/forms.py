from django import forms
from .models import Wallet


from django import forms
from .models import Wallet, Customer

class WalletTopUpForm(forms.ModelForm):
    # Add a mobile field to allow user input for mobile number
    mobile = forms.CharField(max_length=10)

    class Meta:
        model = Wallet
        fields = ['mobile', 'credit']  # Include the necessary fields for the form

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        try:
            customer = Customer.objects.get(mobile=mobile)  # Validate the mobile number
        except Customer.DoesNotExist:
            raise forms.ValidationError("This mobile number is not associated with any customer.")
        return mobile

    def save(self, commit=True):
        # Override the save method to assign the customer ForeignKey
        instance = super().save(commit=False)
        customer = Customer.objects.get(mobile=self.cleaned_data['mobile'])
        instance.customer = customer  # Assign the customer to the wallet instance

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

