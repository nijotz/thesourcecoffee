from locations.models import Area, Location

Area.objects.all().delete()
Location.objects.all().delete()

ny = Area.objects.create(name='New York')
pdx = Area.objects.create(name='Portland/Vancouver')

Location.objects.create(area=pdx, address='555 NW Main St. Portland, OR 97214')
Location.objects.create(area=pdx, address='123 SE Place St. Portland, OR 97222')
Location.objects.create(area=ny, address='123 Main St. New York, NY 10460')
Location.objects.create(area=ny, address='999 Big St. New York, NY 10471')
