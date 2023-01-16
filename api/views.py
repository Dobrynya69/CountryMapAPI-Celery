from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import *
from .serializers import *
from .permitions import *
import urllib.request, json 
from rest_framework.viewsets import ModelViewSet
from . import tasks
import random
import requests

class ContriesReloadView(APIView):
    permission_classes = [IsAdminUser, ]
    model_class = Country
    serializer_class = CountrySerializer


    def post(self, request):
        with urllib.request.urlopen("https://restcountries.com/v3.1/all") as url:
            counries_data = json.load(url)

        self.model_class.objects.all().delete()

        for country in counries_data:
            serializer = self.serializer_class(data={'name': country['name']['common'], 'population': country['population']})
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'error': 'Country error!'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Countries reload success!'}, status=status.HTTP_201_CREATED)


class ContriesFindView(APIView):
    permission_classes = [IsAuthenticated, ]
    model_class = Country
    serializer_class = CountrySerializer


    def post(self, request):
        search_str = request.POST['name']
        return Response({'countries': self.serializer_class(self.model_class.objects.filter(name__contains=search_str), many=True).data})
        

class CountryViewSet(ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated, ])
    def list(self, request):
        return Response(self.serializer_class(self.get_queryset(), many=True).data, status=status.HTTP_202_ACCEPTED)


class CountryImageView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CountrySerializer
    model_class = Country


    def get_random_src(self, json):
        lenght = len(json['photos'])
        rand_int = random.randint(0, lenght - 1)
        return json['photos'][rand_int]['src']['large']


    def get(self, request, *args, **kwargs):
        try:
            country = self.model_class.objects.get(pk=kwargs['pk'])
        except self.model_class.DoesNotExist:
            return Response({'error': 'Country does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_src = self.get_random_src(requests.get(url=f"https://api.pexels.com/v1/search?query={country.name}", headers={'Authorization': '563492ad6f91700001000001018f97a09de4429093e75a2b70f8cc60'}).json())
        return Response({'image': image_src}, status=status.HTTP_202_ACCEPTED)
            

class ReviewViewSet(ModelViewSet):
    permission_classes = [isAuthorOrReadOnly, IsAuthenticated]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


    @action(methods=['post'], detail=False)
    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            tasks.create_review.delay(data, request.user.pk)
            return Response({'message': 'Review is creating... You can leave'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Data is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        


