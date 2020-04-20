from django.shortcuts import render
from .models import Product, Order, Contact
from .forms import ContactForm, OrderForm
from django.core.paginator import Paginator
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse

class HomeView(View):
    
    template_name="shop/home.html"

    def post(self, request, *args, **kwargs):
        context = {}
        context['product_objects'] = Product.objects.all()[:3]
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_email = form.cleaned_data['contact_email']
            Contact.objects.create(contact_email=contact_email)
            context['success_contact'] = True
        
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        context = {}
        context['product_objects'] = Product.objects.all()[:3]
        
        item_name = request.GET.get('item_name')
        if item_name != '' and item_name is not None:
            return HttpResponseRedirect(reverse('index') + f'?item_name={item_name}')
        
        success_order = request.GET.get('success_order')
        if success_order != '' and success_order is not None:
            context['success_order'] = success_order

        return render(request, self.template_name, context)

def index(request):
    #search code
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects_by_title = Product.objects.filter(title__icontains=item_name)
        product_objects_by_category = Product.objects.filter(category__contains=[item_name])
        product_objects = product_objects_by_title | product_objects_by_category
    else:
        product_objects = Product.objects.all()


    #paginator code
    paginator = Paginator(product_objects, 6)
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)
    
    return render(request,'shop/index.html', {'product_objects':product_objects})

def detail(request, id):
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        return HttpResponseRedirect(reverse('index') + f'?item_name={item_name}')

    try:
        product_object = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return render(request,'shop/index.html', {'product_objects': None})

    return render(request,'shop/detail.html', {'product_object': product_object})
    
def checkout(request):
    shipping = 60
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        # print(form.errors)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home') + '?success_order=1')
 
    return render(request,'shop/checkout.html', {'shipping': shipping, 'form': form})
