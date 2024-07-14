# serializers.py
from rest_framework import serializers
from .models import Product, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
    
    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        tags_data = validated_data.pop('tags')
        product = Product.objects.create(**validated_data)
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            product.categories.add(category)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            product.tags.add(tag)
        return product

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories')
        tags_data = validated_data.pop('tags')

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.price = validated_data.get('price', instance.price)
        instance.color = validated_data.get('color', instance.color)
        instance.save()

        instance.categories.clear()
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            instance.categories.add(category)

        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            instance.tags.add(tag)

        return instance
