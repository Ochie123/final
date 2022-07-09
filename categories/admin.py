from django.contrib import admin
from .models import Category, Product, Subcategory 
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)} 

class SubcategoryInline(admin.StackedInline):
    model = Subcategory
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created'] 
    list_filter = ['created', 'category'] 
    search_fields = ['title', 'overview'] 
    prepopulated_fields = {'slug': ('title',)} 
    inlines = [SubcategoryInline]
