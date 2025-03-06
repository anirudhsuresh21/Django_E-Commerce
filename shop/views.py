from django.http import JsonResponse

from ecommerceapp.models import Product

def product_api(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        
        # Handle sizes_available conversion
        sizes = []
        if product.sizes_available:
            if isinstance(product.sizes_available, str):
                # If it's a string, split by comma and clean up
                sizes = [size.strip() for size in product.sizes_available.split(',') if size.strip()]
            elif isinstance(product.sizes_available, (list, tuple)):
                # If it's already a list/tuple
                sizes = list(product.sizes_available)
            else:
                # Default sizes if nothing else works
                sizes = ['S', 'M', 'L']

        data = {
            'id': product.id,
            'product_name': product.product_name,
            'price': str(product.price),
            'sale_price': str(product.sale_price) if product.sale_price else None,
            'discount_percentage': product.discount_percentage,
            'description': product.description,
            'main_image': str(product.main_image),
            'image_2': str(product.image_2) if product.image_2 else None,
            'image_3': str(product.image_3) if product.image_3 else None,
            'image_4': str(product.image_4) if product.image_4 else None,
            'fabric': product.fabric,
            'work_type': product.work_type,
            'stock': product.stock,
            'category': product.get_category_display(),
            'style': product.style,
            'occasion_type': product.occasion_type,
            'sizes_available': sizes,
            'custom_sizing_available': product.custom_sizing_available,
            'delivery_time': product.delivery_time,
            'alteration_available': product.alteration_available,
        }
        print("Sizes being sent:", sizes)  # Debug print
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
