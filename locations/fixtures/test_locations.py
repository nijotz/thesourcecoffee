from locations.models import Location

Location.objects.all().delete()
Location.objects.create(address='555 NW Main St. Portland, OR 97214')
Location.objects.create(address='123 Main St. New York, NY 10460')
