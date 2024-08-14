from django.shortcuts import render

# Create your views here.

from django.views.generic import TemplateView
from django.shortcuts import render # here by default 
from django.views import View 
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here. 

class homePageView(TemplateView): 
    template_name = "pages/home.html"


class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
 
     
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Your Name", 
        }) 
    
        return context
    

class ContactPageView(TemplateView): 
    template_name = 'pages/contact.html' 
 
     
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "email": "helloworld@gmail.com", 
            "adress": "carrera 23a - 65", 
            "phone": "582-242-413", 
        }) 
    
        return context
    

 
class Product: 
    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV", "Price":396}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "Price":300}, 
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "Price":50}, 
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "Price":25} 
    ] 
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id) - 1]
            viewData["title"] = product["name"] + " - Online Store"
            viewData["subtitle"] = product["name"] + " - Product information"
            viewData["product"] = product
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse('home'))

        return render(request, self.template_name, viewData)
    


from django import forms 
from django.shortcuts import render, redirect 
 
class ProductForm(forms.Form): 
    name = forms.CharField(required=True) 
    price = forms.FloatField(required=True,min_value=0) 
 
 
class ProductCreateView(View): 
    template_name = 'products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
             
            return redirect("exito.html")  
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 
            return render(request, self.template_name, viewData)
        

def exito(request):
    return render(request,"products/exito.html")