from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from backend.api.models import Dummy, AfterDummy
from backend.api.serializers.dummy import DummySerializer, AfterDummySerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def public_dummy(request):
    return JsonResponse({'message': 'You are a public dummy!'})


@api_view(['GET'])
def private_dummy(request):
    username = request.user.username

    return JsonResponse({'message': 'You are a dummy, but only in private.', 'username': username})


class DummyDetail(generics.RetrieveAPIView):
    lookup_field = "id"
    queryset = Dummy.objects.all()
    serializer_class = DummySerializer


class AfterDummyView(generics.ListAPIView):
    queryset = AfterDummy.objects.all()
    serializer_class = AfterDummySerializer
