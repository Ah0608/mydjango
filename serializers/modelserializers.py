from rest_framework import serializers

from article.models import Article
from dispatchplatform.models import DisPlatform
from proxypool.models import ProxyPool
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProxySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxyPool
        fields = ['ip','type','validation_time']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title','author','intro','category','created_at']


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisPlatform
        fields = '__all__'