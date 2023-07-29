from rest_framework import serializers

from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = News
        fields = '__all__'
