from rest_framework import serializers
from .models import Blog
from adrf.serializers import ModelSerializer



class BlogSerializer(ModelSerializer):
    # name = serializers.CharField()
    class Meta:
        model = Blog
        exclude = ['sender']

    
    def validate(self, attrs):
        data = super().validate(attrs)
        country_list = ['india', 'usa', 'japan','rusia', 'uk']
        if data['country'].lower() not in country_list:
            raise serializers.ValidationError(f"{data['country']}  this country blog you can not post here ..")
        data['country'] = data['country'].lower()
        return data
    
    async def acreate(self, validated_data):
        user = self.context.get('request').user
        validated_data['sender'] = user
        return await super().acreate(validated_data)
