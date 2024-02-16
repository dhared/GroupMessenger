from django.contrib.auth import get_user_model
from rest_framework import serializers
from groups.models import Group


User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ('created_by', )
        extra_kwargs = {"members": {"required": False}}

    def create(self, validated_data):
        created_by = self.context['request'].user
        validated_data['created_by'] = created_by
        group = super().create(validated_data)
        group.members.add(created_by)
        return group


class UserIdSerializer(serializers.Serializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
