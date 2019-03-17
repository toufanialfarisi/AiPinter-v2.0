from aipinter import ma
from aipinter.models import BlogPost, ImageFile, OCR

class UserPostSchema(ma.ModelSchema):
    class Meta:
        model = BlogPost

class ImageFileSchema(ma.ModelSchema):
    class Meta:
        model = ImageFile

class OCRSchema(ma.ModelSchema):
    class Meta:
        model = OCR




