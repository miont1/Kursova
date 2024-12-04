from rest_framework import serializers
from autos.models import AutosModel, Tag, AutoComment
from users.models import Profile, Advantage


class AutoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoComment
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AutosModelSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = AutosModel
        fields = '__all__'

    def get_comments(self, obj):
        comments = obj.autocomment_set.all()
        serializer = AutoCommentSerializer(comments, many=True)
        return serializer.data
