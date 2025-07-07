from django.db import models

class WeatherEntry(models.Model):
    city = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.IntegerField()
    icon = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.city} - {self.temperature}°C @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"