# Create your views here.

from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect, get_object_or_404  # here by default
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product

# Create your views here.


class homePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "title": "About us - Online Store",
                "subtitle": "About us",
                "description": "This is an about page ...",
                "author": "Developed by: Your Name",
            }
        )

        return context


class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "email": "helloworld@gmail.com",
                "adress": "carrera 23a - 65",
                "phone": "582-242-413",
            }
        )

        return context


from .models import Product


class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()

        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        viewData = {}

        # Check if product id is valid
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            # If the product id is not valid, redirect to the home page
            return HttpResponseRedirect(reverse("home"))

        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = (
        "products"  # This will allow you to loop through 'products' in your template
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products - Online Store"
        context["subtitle"] = "List of products"
        return context


from django import forms


class ProductForm(forms.Form):
    class Meta:
        model = Product
        fields = ["name", "price"]


class ProductCreateView(View):
    template_name = "products/create.html"

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("exito.html")
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)


def exito(request):
    return render(request, "products/exito.html")


class CartView(View): 
    template_name = 'cart/index.html' 
     
    def get(self, request): 
        # Simulated database for products 
        products = {} 
        products[121] = {'name': 'Tv samsung', 'price': '1000'} 
        products[11] = {'name': 'Iphone', 'price': '2000'} 
 
        # Get cart products from session 
        cart_products = {} 
        cart_product_data = request.session.get('cart_product_data', {}) 
 
        for key, product in products.items(): 
            if str(key) in cart_product_data.keys(): 
                cart_products[key] = product 
 
        # Prepare data for the view 
        view_data = { 
            'title': 'Cart - Online Store', 
            'subtitle': 'Shopping Cart', 
            'products': products, 
            'cart_products': cart_products 
        } 
 
        return render(request, self.template_name, view_data)
    def post(self, request, product_id): 
        # Get cart products from session and add the new product 
        cart_product_data = request.session.get('cart_product_data', {}) 
        cart_product_data[product_id] = product_id 
        request.session['cart_product_data'] = cart_product_data 
    
        return redirect('cart_index') 
 
 
class CartRemoveAllView(View): 
    def post(self, request): 
        # Remove all products from cart in session 
        if 'cart_product_data' in request.session: 
            del request.session['cart_product_data'] 
 
        return redirect('cart_index')