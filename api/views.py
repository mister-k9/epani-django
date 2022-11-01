from django.http import HttpResponse, JsonResponse
import json
from django.forms.models import model_to_dict
from epani.models import Card, Order, Machine
from epani.serializers import CardSerializer, OrderSerializer, MachineSerializer
from rest_framework import generics, permissions, authentication

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.views import View

from api.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_home(request, *args, **kwargs):
    if request.method == 'GET':
        instance = Card.objects.all()
        print(instance)
        if instance:
            serializer = CardSerializer(instance, many=True)
            return Response(serializer.data)

  

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_card_detail(request):
    if request.method == 'GET':
        card_num = request.GET['cardno']
        instance = Card.objects.get(card_number=card_num)
        print(instance)
        if instance:
            serializer = CardSerializer(instance, many=True)
            return Response(serializer.data)

    

    


@api_view(["GET", "POST"])
def machine_cards(request, *args, **kwargs):
    if request.method == "GET":
        machine_id = request.GET['machine_id']
        print(machine_id)
        instance = Card.objects.all().filter(machine_id=machine_id)
        if instance:
            data = CardSerializer(instance, many=True)
            print(data.data)

        return Response(data)

    # return HttpResponse("404 Page Not Found")



class CardListCreateAPIView(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    
    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class CardDetailAPIView(generics.RetrieveAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    lookup_field = 'card_number'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CardUpdateAPIView(generics.UpdateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    lookup_field = 'card_number'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


class CardDestroyAPIView(generics.DestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    lookup_field = 'card_number'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'


class OrderUpdateAPIView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'

    def perform_update(self, serializer):
        serializer.save()


class OrderDestroyAPIView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class MachineListCreateAPIView(generics.ListCreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class MachineDetailAPIView(generics.RetrieveAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    lookup_field = 'machine_id'


class MachineUpdateAPIView(generics.UpdateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    lookup_field = 'machine_id'

    def perform_update(self, serializer):
        serializer.save()


class MachineDestroyAPIView(generics.DestroyAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    lookup_field = 'machine_id'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
