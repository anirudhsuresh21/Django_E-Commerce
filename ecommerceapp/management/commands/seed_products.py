from django.core.management.base import BaseCommand
from ecommerceapp.models import Product
from django.core.files import File
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Seed the Product model with wedding-related products'

    def handle(self, *args, **options):
        self.stdout.write('Creating wedding-related products...')

        products_data = [
            {
                'product_name': 'Royal Wedding Lehenga',
                'category': 'BRIDE',
                'subcategory': 'LEHENGA',
                'price': 75000.00,
                'sale_price': 67500.00,
                'description': 'Stunning bridal lehenga with intricate zardozi work and crystal embellishments. Perfect for the modern bride who wants to make a statement.',
                'fabric': 'Raw Silk, Net',
                'sizes_available': 'XS,S,M,L,XL',
                'stock': 5,
                'custom_sizing_available': True,
                'alteration_available': True,
                'occasion_type': 'Wedding',
                'style': 'Traditional',
                'work_type': 'Zardozi, Crystal Work',
                'is_featured': True,
                'rating': 4.8,
                'reviews_count': 24,
            },
            {
                'product_name': 'Classic Wedding Sherwani',
                'category': 'GROOM',
                'subcategory': 'SHERWANI',
                'price': 45000.00,
                'description': 'Royal blue sherwani with golden threadwork and pearl embellishments. Includes matching stole and churidar.',
                'fabric': 'Silk Blend',
                'sizes_available': 'M,L,XL,XXL',
                'stock': 8,
                'custom_sizing_available': True,
                'alteration_available': True,
                'occasion_type': 'Wedding',
                'style': 'Modern Traditional',
                'work_type': 'Thread Work, Pearl Work',
                'is_featured': True,
                'rating': 4.7,
                'reviews_count': 18,
            },
            {
                'product_name': 'Bridal Kundan Set',
                'category': 'JEWELRY',
                'subcategory': 'NECKLACE',
                'price': 125000.00,
                'sale_price': 112500.00,
                'description': 'Complete bridal set including necklace, earrings, and maang tika. Features kundan work with pearl drops.',
                'stock': 3,
                'occasion_type': 'Wedding',
                'style': 'Traditional',
                'is_featured': True,
                'rating': 4.9,
                'reviews_count': 15,
            },
            {
                'product_name': 'Designer Wedding Saree',
                'category': 'BRIDE',
                'subcategory': 'SAREE',
                'price': 85000.00,
                'description': 'Heavy embroidered silk saree with zari work border and designer blouse piece.',
                'fabric': 'Pure Silk',
                'sizes_available': 'Free Size',
                'stock': 4,
                'custom_sizing_available': True,
                'alteration_available': True,
                'occasion_type': 'Wedding, Reception',
                'style': 'Designer',
                'work_type': 'Zari Work, Embroidery',
                'rating': 4.6,
                'reviews_count': 12,
            },
            {
                'product_name': 'Crystal Wedding Clutch',
                'category': 'ACCESSORIES',
                'subcategory': 'CLUTCH',
                'price': 12000.00,
                'sale_price': 10800.00,
                'description': 'Crystal-embellished bridal clutch with chain strap. Perfect for wedding ceremonies.',
                'stock': 10,
                'occasion_type': 'Wedding, Reception',
                'style': 'Luxury',
                'rating': 4.5,
                'reviews_count': 8,
            }
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                product_name=product_data['product_name'],
                defaults=product_data
            )

            # Add sample images (you'll need to add actual images to your media directory)
            if created:
                # Example of how to add images (uncomment and modify paths as needed)
                """
                image_path = os.path.join(settings.MEDIA_ROOT, 'sample_images', f'{product_data["category"].lower()}.jpg')
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        product.main_image.save(
                            f'{product_data["category"].lower()}.jpg',
                            File(img_file),
                            save=True
                        )
                """
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.product_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product.product_name}')
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded wedding-related products'))
