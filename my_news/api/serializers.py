from rest_framework import serializers

from news.models import Comment, News


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'created_at')


class NewsSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    last_comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_last_comments(self, obj):
        COMMENTS_COUNT = 10

        return CommentSerializer(
            obj.comments.order_by('-created_at')[:COMMENTS_COUNT],
            many=True
        ).data

    class Meta:
        model = News
        fields = ('id', 'author', 'title', 'text', 'comments_count', 'likes_count', 'last_comments',)
