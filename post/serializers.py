from rest_framework import serializers 
from .models import Post, Tag, Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Subscription
        fields = ['subscriber', 'tag', 'user']
        extra_kwargs = {
            'tag': {'required': False},
            'user': {'required': False},
        }

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Post
        fields = ['title', 'text', 'user', 'tags', 'likes', 'dislikes', 'viewed']

        extra_kwargs = {
            'likes': {'required': False},
            'dislikes': {'required': False},
            'viewed': {'required': False}
        }

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        post = Post.objects.create(**validated_data)

        tag_objects = []
        for tag_data in tags_data:
            tag_object = Tag.objects.create(**tag_data)
            tag_objects.append(tag_object)

        post.tags.set(tag_objects)
        return post

    def update(self, instance, validated_data):
        instance.likes = validated_data.get('likes', instance.likes)
        instance.dislikes = validated_data.get('dislikes', instance.dislikes)
        instance.viewed = validated_data.get('viewed', instance.viewed)

        instance.save()
        return instance

    