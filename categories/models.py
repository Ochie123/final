from django.db import models
from django.contrib.auth.models import User 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text='Type the title of your product in small letters') 
    meta_keywords = models.CharField("Meta Keywords",max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag') 
    meta_description = models.CharField("Meta Description", max_length=255,help_text='Content for description meta tag') 
    class Meta:
        ordering = ['title'] 
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.title 

class Product(models.Model):
    owner = models.ForeignKey(User, related_name='products_created',on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE) 
    buyers = models.ManyToManyField(User, related_name='products_joined',blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    title = models.CharField(max_length=200, help_text='Title of your product, e.g Sofa')
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    image2 = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    image3 = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    is_active = models.BooleanField(default=True) 
    is_bestseller = models.BooleanField(default=False) 
    is_featured = models.BooleanField(default=False) 
    brand = models.CharField(max_length=50)
    sku = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9,decimal_places=2,help_text='Current price')
    old_price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,default=0.00, help_text='Old price')
    quantity = models.IntegerField()
    slug = models.SlugField(max_length=200, unique=True, help_text='Type the title of your product in small letters, e.g sofa') 
    meta_keywords = models.CharField(max_length=255,help_text='Comma-delimited set of SEO keywords for meta tag') 
    meta_description = models.CharField(max_length=255,help_text='Content for description meta tag') 
    overview = models.TextField(help_text='Describe your product and terms')
    created = models.DateTimeField(auto_now_add=True) 
    class Meta:
        ordering = ['-created'] 
    def __str__(self):
        return self.title 

class Subcategory(models.Model):
    product = models.ForeignKey(Product, related_name='subcategories',on_delete=models.CASCADE) 
    title = models.CharField(max_length=200,help_text='categories to help you, e.g Sitting, Home' )
    description = models.TextField(blank=True) 
    order = OrderField(blank=True, for_fields=['product'])
    class Meta:
        ordering = ['order']
    def __str__(self):
        return f'{self.order}. {self.title}'

class Content(models.Model):
    subcategory = models.ForeignKey(Subcategory,related_name='contents', on_delete=models.CASCADE) 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':( 'text','video', 'image', 'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['subcategory'])

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(User,
    related_name='%(class)s_related', on_delete=models.CASCADE) 
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    
    class Meta:
        abstract = True 
    def __str__(self):
        return self.title 
        
class Text(ItemBase):
    content = models.TextField() 
class File(ItemBase):
    file = models.FileField(upload_to='files') 
class Image(ItemBase):
    file = models.FileField(upload_to='images') 
class Video(ItemBase):
    url = models.URLField()

class ItemBase(models.Model):
    def render(self):
        return render_to_string(f'products/content/{self._meta.model_name}.html', {'item': self})