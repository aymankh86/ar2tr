from django.db import models
import pyarabic.araby as araby

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Phrase(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category') 
    tr_text = models.CharField(max_length=255)
    ar_text = models.CharField(max_length=255)
    ar_text_no_harakat = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.ar_text_no_harakat = araby.strip_harakat(self.ar_text)
        super(Phrase, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.ar_text} (ar) -> {self.tr_text} (tr)'


class Suggestions(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='suggestion_category', null=True, blank=True) 
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE, related_name='suggestion_phrase', null=True, blank=True) 
    tr_text = models.CharField(max_length=255)
    ar_text = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50)


    def __str__(self):
        return f'{self.job_type}: {self.ar_text} (ar) -> {self.tr_text} (tr)'