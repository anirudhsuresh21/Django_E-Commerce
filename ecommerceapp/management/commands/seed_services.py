from django.core.management.base import BaseCommand
from ecommerceapp.models import Services

class Command(BaseCommand):
    help = 'Seed the Services model with marriage-related services'

    def handle(self, *args, **options):
        self.stdout.write('Creating marriage-related services...')
        
        services_data = [
            {
                'provider_name': 'Perfect Match Matrimony',
                'email': 'contact@perfectmatch.com',
                'phone_no': '+91 98765 43210',
                'address': 'Crystal Tower, MG Road, Bangalore 560001',
                'service_name': 'Elite Matchmaking Service',
                'service_category': 'Matchmaking',
                'description': 'Premium matchmaking service with personalized consultations and verified profiles',
                'price_range': '₹25,000 - ₹1,00,000',
                'experience_years': 15,
                'website': 'https://perfectmatch.com',
                'rating': 4.8,
                'reviews_count': 520,
                'social_links': {'instagram': '@perfectmatch', 'facebook': 'perfectmatchofficial'},
                'available_days': 'Monday-Saturday',
                'working_hours': '10 AM - 7 PM',
                'verified': True
            },
            {
                'provider_name': 'Royal Wedding Planners',
                'email': 'info@royalweddings.com',
                'phone_no': '+91 99999 88888',
                'address': 'The Business Hub, Whitefield, Bangalore 560066',
                'service_name': 'Complete Wedding Planning',
                'service_category': 'Wedding Planning',
                'description': 'End-to-end wedding planning services including venue, decor, catering, and coordination',
                'price_range': '₹5,00,000 - ₹25,00,000',
                'experience_years': 10,
                'website': 'https://royalweddings.com',
                'rating': 4.9,
                'reviews_count': 310,
                'social_links': {'instagram': '@royalweddings', 'pinterest': 'royalweddingsind'},
                'available_days': 'All Days',
                'working_hours': '9 AM - 8 PM',
                'verified': True
            },
            {
                'provider_name': 'Memorable Moments Photography',
                'email': 'shoot@memorablemoments.com',
                'phone_no': '+91 98989 89898',
                'address': 'Creative Space, Indiranagar, Bangalore 560038',
                'service_name': 'Wedding Photography & Videography',
                'service_category': 'Photography',
                'description': 'Cinematic wedding films and artistic photography packages',
                'price_range': '₹1,50,000 - ₹5,00,000',
                'experience_years': 8,
                'website': 'https://memorablemoments.com',
                'rating': 4.7,
                'reviews_count': 245,
                'social_links': {'instagram': '@memorablemoments', 'youtube': 'memorablemomentsofficial'},
                'available_days': 'All Days',
                'working_hours': 'Flexible Hours',
                'verified': True
            },
            {
                'provider_name': 'Divine Caterers',
                'email': 'bookings@divinecaterers.com',
                'phone_no': '+91 77777 66666',
                'address': 'Food Street, Malleshwaram, Bangalore 560003',
                'service_name': 'Wedding Catering Services',
                'service_category': 'Catering',
                'description': 'Multi-cuisine catering specializing in traditional and modern wedding feasts',
                'price_range': '₹750 - ₹2,000 per plate',
                'experience_years': 20,
                'website': 'https://divinecaterers.com',
                'rating': 4.6,
                'reviews_count': 680,
                'social_links': {'instagram': '@divinecaterers', 'facebook': 'divinecaterersofficial'},
                'available_days': 'All Days',
                'working_hours': '7 AM - 11 PM',
                'verified': True
            },
            {
                'provider_name': 'Bridal Beauty Studio',
                'email': 'appointment@bridalbeauty.com',
                'phone_no': '+91 88888 77777',
                'address': 'Beauty Plaza, Koramangala, Bangalore 560034',
                'service_name': 'Bridal Makeup & Styling',
                'service_category': 'Makeup & Styling',
                'description': 'Professional bridal makeup, hairstyling, and draping services',
                'price_range': '₹25,000 - ₹75,000',
                'experience_years': 12,
                'website': 'https://bridalbeauty.com',
                'rating': 4.9,
                'reviews_count': 430,
                'social_links': {'instagram': '@bridalbeautystudio', 'facebook': 'bridalbeautystudio'},
                'available_days': 'Tuesday-Sunday',
                'working_hours': '8 AM - 8 PM',
                'verified': True
            }
        ]

        for service_data in services_data:
            service, created = Services.objects.get_or_create(
                email=service_data['email'],
                defaults=service_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created service: {service.service_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Service already exists: {service.service_name}')
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded marriage-related services'))
