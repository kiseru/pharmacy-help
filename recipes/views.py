import traceback
from uuid import uuid4

from rest_framework import status, permissions, mixins, viewsets, filters
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes import serializers, models
from recipes.models import Recipe, User
from recipes.permissions import IsDoctor, IsApothecary, IsAdmin
from recipes.serializers import MedicineWithPharmaciesSerializer, GoodSerializer
from recipes.services import get_pharmacies_and_medicines


class LoginViewSet(viewsets.GenericViewSet):
    queryset = models.User.objects.none()
    serializer_class = serializers.LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data['email']).first()
        if user is None or not user.check_password(serializer.validated_data['password']):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user_id=user.id)
        return Response({'token': token.key, 'role': user.role})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsApothecary | IsDoctor,
                          IsAdmin)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        return Response(self.serializer_class(request.user).data)


class RecipesViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticated,
                          IsDoctor)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor, token=uuid4())

    def get_queryset(self):
        return self.queryset.filter(doctor__user=self.request.user)


class MedicineWithPharmaciesViewSet(mixins.ListModelMixin,
                                    viewsets.GenericViewSet):
    queryset = models.Medicine.objects.filter(good__count__gt=0)
    serializer_class = MedicineWithPharmaciesSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [filters.SearchFilter]
    search_field = ('medicine_name__medicine_name',
                    'medicine_type__type_name')


def find_pharmacies(request):
    try:
        data = {
            'medicines': request.GET.getlist('medicines'),
            'city_name': request.GET['city_name'],
            'coordinates': (float(request.GET['latitude']), float(request.GET['longitude'])) if ('latitude'
                                                                                                 and 'longitude'
                                                                                                 in request.GET) else None,
        }
        result = get_pharmacies_and_medicines(data)
        return Response(result)
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ApothecaryViewSet(viewsets.ModelViewSet):
    queryset = models.Apothecary.objects.all()
    serializer_class = serializers.ApothecarySerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsApothecary,
                          IsAdmin)

    def get_queryset(self):
        return self.queryset.filter(pharmacy=self.request.user.apothecary.pharmacy)

    def perform_create(self, serializer):
        serializer.save(pharmacy=self.request.user.apothecary.pharmacy)


class GoodsViewSet(viewsets.ModelViewSet):
    queryset = models.Good.objects.all()
    serializer_class = GoodSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsApothecary)

    def get_queryset(self):
        return self.queryset.filter(pharmacy=self.request.user.apothecary.pharmacy)

    def perform_create(self, serializer):
        serializer.save(pharmacy=self.request.user.apothecary.pharmacy)


class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Medicine.objects.all()
    serializer_class = serializers.MedicineSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsDoctor)
    filter_backends = [filters.SearchFilter]
    search_fields = ('medicine_name__medicine_name',
                     'medicine_type__type_name')
