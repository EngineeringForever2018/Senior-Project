from django.contrib.auth.models import Group
from rest_framework import serializers


# Quick reference: https://www.django-rest-framework.org/api-guide/serializers/


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


