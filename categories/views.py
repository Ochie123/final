from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.forms.models import modelform_factory 
from django.apps import apps
from .models import Subcategory, Content


from django.db.models import Count
from .models import Category

from django.views.generic.base import TemplateResponseMixin, View 
from .forms import SubcategoryFormSet
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Product

#Reordering modules and their contents

# Create your views here.
class CarouselView(TemplateView):
    template_name = 'other/carousel.html'

class ManageProductListView(ListView):
    model = Product
    template_name = 'courses/manage/course/list.html' 
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
class OwnerEditMixin(object): 
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form) 
        
class OwnerProductMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Product
    fields = ['category', 'title', 'slug', 'overview', 'price', 'old_price', 'brand', 'sku', 'quantity', 'meta_keywords', 'meta_description'] 
    success_url = reverse_lazy('manage_product_list')

class OwnerProductEditMixin(OwnerProductMixin, OwnerEditMixin): 
    template_name = 'courses/manage/course/form.html'
class ManageProductListView(OwnerProductMixin, ListView): 
    template_name = 'courses/manage/course/list.html'
    permission_required = 'products.view_product'

class ProductCreateView(OwnerProductEditMixin, CreateView): 
    permission_required = 'products.add_product'
    
class ProductUpdateView(OwnerProductEditMixin, UpdateView): 
    permission_required = 'products.change_product'
class ProductDeleteView(OwnerProductMixin, DeleteView): 
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'products.delete_product'

class ProductSubcategoryUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html' 
    product = None
    def get_formset(self, data=None):
        return SubcategoryFormSet(instance=self.product, data=data)
    def dispatch(self, request, pk): 
        self.product = get_object_or_404(Product,id=pk,owner=request.user) 
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'product': self.product,'formset': formset}) 
    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST) 
        if formset.is_valid():
            formset.save()
            return redirect('manage_product_list')
        return self.render_to_response({'product': self.product,'formset': formset})

class ContentCreateUpdateView(TemplateResponseMixin, View): 
    subcategory = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html' 
    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']: 
            return apps.get_model(app_label='categories',model_name=model_name)
        return None
    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order','created', 'updated'])
        return Form(*args, **kwargs)
    def dispatch(self, request, subcategory_id, model_name, id=None):
        self.subcategory = get_object_or_404(Subcategory, id=subcategory_id,
        product__owner=request.user) 
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,id=id,owner=request.user)
        return super().dispatch(request, subcategory_id, model_name, id)

    def get(self, request, subcategory_id, model_name, id=None): 
        form = self.get_form(self.model, instance=self.obj) 
        return self.render_to_response({'form': form,'object': self.obj}) 

    def post(self, request, subcategory_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj,
        data=request.POST, files=request.FILES)
        
        if form.is_valid():
            obj = form.save(commit=False) 
            obj.owner = request.user 
            obj.save()
        if not id:
            # new content 
            Content.objects.create(subcategory=self.subcategory,item=obj)
            return redirect('subcategory_content_list', self.subcategory.id)
        return self.render_to_response({'form': form, 'object': self.obj})

class SubcategoryContentListView(TemplateResponseMixin, View): 
    template_name = 'courses/manage/module/content_list.html' 
    def get(self, request, subcategory_id):
        subcategory = get_object_or_404(Subcategory, id=subcategory_id,product__owner=request.user) 
        
        return self.render_to_response({'subcategory': subcategory})
#This is the ModuleOrderView view.


class ProductListView(TemplateResponseMixin, View):
    model = Product
    products = Product.objects.all()
    template_name = 'courses/course/list.html' 
    paginate_by = 4
    def get(self, request, category=None):
        categories = Category.objects.annotate( total_products=Count('products'))
        products = Product.objects.annotate( total_subcategories=Count('subcategories'))
        if category:
            category = get_object_or_404(Category, slug=category) 
            products = products.filter(category=category)
        return self.render_to_response({'categories': categories, 'category': category,'products': products})

class ProductDetailView(DetailView):
    model = Product
    template_name = 'courses/course/detail.html'

class ProductDetailView(DetailView): 
    model = Product
    template_name = 'courses/course/detail.html' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = ProductEnrollForm( initial={'product':self.object})
        return context

