from rest_framework.serializers import HyperlinkedModelSerializer

from backend.api.models import Dummy, AfterDummy


class DummySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Dummy
        fields = ["is_dummy"]


class AfterDummySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = AfterDummy
        fields = ["dummy"]
