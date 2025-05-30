from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'created_at', 'updated_at', 'is_approved']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'is_published', 'created_at', 'updated_at']



class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'is_published', 'created_at', 'updated_at', 'comments']
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(
            instance.comments.filter(is_approved=True), 
            many=True
        ).data
        return representation
    

# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Post, Comment


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']


# class CommentSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)
#     post = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'post', 'author', 'body', 'created_at', 'updated_at', 'is_approved']
#         read_only_fields = ['id', 'post', 'created_at', 'updated_at', 'is_approved']


# class CommentDetailSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)
#     post = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'post', 'author', 'body', 'created_at', 'updated_at', 'is_approved']
#         read_only_fields = ['id', 'post', 'created_at', 'updated_at']


# class CommentUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['body']


# class PostListSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)

#     class Meta:
#         model = Post
#         fields = ['id', 'author', 'title', 'created_at', 'updated_at', 'is_published']


# class PostDetailSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)
#     comments = serializers.SerializerMethodField()

#     class Meta:
#         model = Post
#         fields = ['id', 'author', 'title', 'body', 'created_at', 'updated_at', 'is_published', 'comments']
#         read_only_fields = ['id', 'created_at', 'updated_at']

#     def get_comments(self, obj):
#         approved_comments = obj.comments.filter(is_approved=True)
#         return CommentSerializer(approved_comments, many=True).data


# class PostCreateUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['title', 'body', 'is_published']

#     def create(self, validated_data):
#         validated_data['author'] = self.context['request'].user
#         return super().create(validated_data)


# class CommentCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['body']

#     def create(self, validated_data):
#         validated_data['author'] = self.context['request'].user
#         validated_data['post'] = self.context['post']
#         return super().create(validated_data)