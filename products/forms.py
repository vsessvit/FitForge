from django import forms
from .models import Product, ProductCategory
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    """Form for adding and editing products"""
    
    class Meta:
        model = Product
        fields = ['category', 'sku', 'name', 'description', 'price', 
                  'stock_quantity', 'rating', 'image_url', 'image']
    
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = ProductCategory.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        
        self.fields['category'].choices = friendly_names
        
        # Add placeholders
        placeholders = {
            'category': 'Product Category',
            'sku': 'SKU (e.g., pp5001340155)',
            'name': 'Product Name',
            'description': 'Product Description',
            'price': 'Price (e.g., 29.99)',
            'stock_quantity': 'Stock Quantity',
            'rating': 'Rating (0-5)',
            'image_url': 'Image URL (optional)',
        }
        
        # Set autofocus on first field
        self.fields['category'].widget.attrs['autofocus'] = True
        
        # Add CSS classes and placeholders to all fields
        for field_name, field in self.fields.items():
            if field_name != 'image':
                if field_name in placeholders:
                    placeholder = placeholders[field_name]
                    field.widget.attrs['placeholder'] = placeholder
                field.widget.attrs['class'] = 'form-control border-dark rounded-0'
