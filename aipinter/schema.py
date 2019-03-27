from aipinter import ma
from aipinter.models import BlogPost, ImageFile, OCR, Forecasting

class UserPostSchema(ma.ModelSchema):
    class Meta:
        model = BlogPost

class ImageFileSchema(ma.ModelSchema):
    class Meta:
        model = ImageFile

class OCRSchema(ma.ModelSchema):
    class Meta:
        model = OCR

class ForecastingSchema(ma.ModelSchema):
    class Meta:
        model = Forecasting




