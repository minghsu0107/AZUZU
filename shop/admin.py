from django.contrib import admin
from .models import Product, Order, Contact
from django_admin_json_editor import JSONEditorWidget


admin.site.site_header = 'AZUZU'
admin.site.site_title = 'AZUZU'
admin.site.index_title = 'AZUZU Admin'

class ArrayFieldListFilter(admin.SimpleListFilter):
    """This is a list filter based on the values
    from a model's `keywords` ArrayField. """

    title = 'categories'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        # Very similar to our code above, but this method must return a
        # list of tuples: (lookup_value, human-readable value). These
        # appear in the admin's right sidebar

        categories = Product.objects.values_list("category", flat=True)
        categories = [(kw, kw) for sublist in categories for kw in sublist if kw]

        categories = sorted(set(categories))
        return categories

    def queryset(self, request, queryset):
        # when a user clicks on a filter, this method gets called. The
        # provided queryset with be a queryset of Items, so we need to
        # filter that based on the clicked keyword.

        lookup_value = self.value()  # The clicked keyword. It can be None!
        if lookup_value:
            # the __contains lookup expects a list, so...
            queryset = queryset.filter(category__contains=[lookup_value])
        return queryset

class ProductAdmin(admin.ModelAdmin):

    def cancel_discount(self, request, queryset):
        price = queryset.values_list('price', flat=True)
        queryset.update(discount_price=price[0])
    cancel_discount.short_description = 'Change discount price to original price'

    actions = ('cancel_discount', )

    list_display = ('title', 'price', 'discount_price', 'category', 'image')
    list_editable = ('price', 'discount_price', 'category', 'image')
    list_filter = ('price', ArrayFieldListFilter,)
    search_fields = ('title',)

admin.site.register(Product, ProductAdmin)

class ContactAdmin(admin.ModelAdmin):
    readonly_fields=('created',)
    
admin.site.register(Contact, ContactAdmin)

def dynamic_schema(widget):
	return {}

@admin.register(Order)
class JSONModelAdmin(admin.ModelAdmin):
	readonly_fields=('created',)
	def get_form(self, request, obj=None, **kwargs):
		widget = JSONEditorWidget(dynamic_schema, collapsed=False)
		form = super().get_form(request, obj, widgets={'items': widget}, **kwargs)
		return form