from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    description = models.TextField(verbose_name="Tavsif", blank=True)
    image = models.ImageField(upload_to='categories/', verbose_name="Rasm", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name
