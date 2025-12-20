from django.db import models

class Region(models.Model):
    """
    Рівень 1: Автономна Республіка Крим, область, міста зі спец. статусом.
    Категорії: 'O' (Область/АРК), 'K' (Місто спец. статусу - Київ, Севастополь)
    """
    CATEGORY_CHOICES = (
        ('O', 'Область / АРК'),
        ('K', 'Місто спеціального статусу'),
    )

    code = models.CharField(max_length=20, unique=True, verbose_name="Код КАТОТТГ")
    name = models.CharField(max_length=128, verbose_name="Назва")
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, verbose_name="Категорія")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Регіон (Область)"
        verbose_name_plural = "Регіони (Області)"
        ordering = ['name']


class District(models.Model):
    """
    Рівень 2: Райони областей та АРК.
    Категорія: 'P' (Район)
    """
    code = models.CharField(max_length=20, unique=True, verbose_name="Код КАТОТТГ")
    name = models.CharField(max_length=128, verbose_name="Назва")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts', verbose_name="Регіон")

    def __str__(self):
        return f"{self.name}, {self.region.name}"

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Райони"
        ordering = ['name']


class Community(models.Model):
    """
    Рівень 3: Територіальні громади.
    Категорія: 'H' (Громада)
    """
    code = models.CharField(max_length=20, unique=True, verbose_name="Код КАТОТТГ")
    name = models.CharField(max_length=128, verbose_name="Назва")
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='communities', verbose_name="Район")
    
    def __str__(self):
        return f"{self.name}, {self.district.name}"

    class Meta:
        verbose_name = "Громада"
        verbose_name_plural = "Громади"
        ordering = ['name']


class Settlement(models.Model):
    """
    Рівень 4: Населені пункти (міста, селища, села).
    Категорії: 'M' (Місто), 'X' (Селище), 'C' (Село)
    """
    CATEGORY_CHOICES = (
        ('M', 'Місто'),
        ('X', 'Селище'),
        ('C', 'Село'),
    )

    code = models.CharField(max_length=20, unique=True, verbose_name="Код КАТОТТГ")
    name = models.CharField(max_length=128, verbose_name="Назва")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='settlements', verbose_name="Громада")
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, verbose_name="Категорія")

    # Geolocation support
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Довгота")

    def __str__(self):
        return f"{self.name} ({self.get_category_display()}), {self.community.district.region.name} обл., {self.community.district.name} р-н"

    class Meta:
        verbose_name = "Населений пункт"
        verbose_name_plural = "Населені пункти"
        ordering = ['name']


class CityDistrict(models.Model):
    """
    Додатковий рівень: Райони в містах.
    Категорія: 'B' (Район у місті)
    """
    code = models.CharField(max_length=20, unique=True, verbose_name="Код КАТОТТГ")
    name = models.CharField(max_length=128, verbose_name="Назва")
    settlement = models.ForeignKey(Settlement, on_delete=models.CASCADE, related_name='city_districts', verbose_name="Місто")
    
    def __str__(self):
        return f"{self.name}, м. {self.settlement.name}"

    class Meta:
        verbose_name = "Район у місті"
        verbose_name_plural = "Райони у містах"
        ordering = ['name']
