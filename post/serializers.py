from rest_framework import serializers
from .models import *


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ('image',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Post
        fields = ('id', 'description', 'author', 'total_likes')

    def create(self, validated_data):
        request = self.context.get('request')
        pictures_files = request.FILES
        post = Post.objects.create(
            author=request.user,
            **validated_data
        )
        for picture in pictures_files.getlist('image'):
            Picture.objects.create(
                image=picture,
                post=post
            )
        return post

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.pictures.all().delete()
        for image in images_data.getlist('pictures'):
            Picture.objects.create(
                image=image,
                post=instance
            )
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['pictures'] = PictureSerializer(instance.pictures.all(), many=True).data
        return representation