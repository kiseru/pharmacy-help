import traceback
from uuid import uuid4

import rest_framework
from django import http
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import status, permissions, mixins, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes, action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from recipes import serializers, models
from recipes.exceptions import AlreadyExistsException
from recipes.models import Recipe, MedicineName, MedicineType, Medicine, User
from recipes.permissions import IsDoctor, IsApothecary, IsAdmin
from recipes.serializers import MedicineNameSerializer, MedicineTypeSerializer, \
    MedicineWithPharmaciesSerializer, GoodSerializer
from recipes.services import get_pharmacies_and_medicines


def response_to_api_format(func):
    def new_func(request, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
            if response.__class__ != Response:
                return response
            if status.is_success(response.status_code) or status.is_redirect(response.status_code):
                response.data = get_response(is_success=True, data=response.data)
            elif status.is_client_error(response.status_code):
                response.data = get_response(is_success=False, data=response.data, error='invalid_data')
            return response
        except (rest_framework.exceptions.ValidationError, ValidationError, ObjectDoesNotExist, ValueError):
            traceback.print_exc()
            new_response = get_response(is_success=False, error='invalid_data')
            return Response(data=new_response, status=status.HTTP_400_BAD_REQUEST)
        except http.response.Http404:
            traceback.print_exc()
            new_response = get_response(is_success=False, error='not_found')
            return Response(data=new_response, status=status.HTTP_404_NOT_FOUND)
        except AlreadyExistsException:
            new_response = get_response(is_success=False, error='already_exists')
            return Response(data=new_response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            new_response = get_response(is_success=False, error=str(e))
            return Response(data=new_response, status=status.HTTP_400_BAD_REQUEST)

    return new_func


def get_response(is_success, error=None, data=None):
    return {
        'status': 'success' if is_success else 'fail',
        'error': error,
        'data': data,
    }


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
    queryset = Recipe.objects.none()
    permission_classes = (permissions.IsAuthenticated,
                          IsDoctor)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctor, token=uuid4())

    def get_queryset(self):
        return Recipe.objects.filter(doctor__user=self.request.user)


class SearchMedicineViewSet(ReadOnlyModelViewSet):
    renderer_classes = (JSONRenderer,)

    queryset = MedicineName.objects.all()
    serializer_class = MedicineNameSerializer

    def list(self, request, *args, **kwargs):
        if 'medicine_name' in request.GET:
            self.queryset = self.queryset.filter(medicine_name__icontains=request.GET['medicine_name'])
        return super().list(request, *args, *kwargs)


class SearchMedicineTypesViewSet(ReadOnlyModelViewSet):
    renderer_classes = (JSONRenderer,)

    queryset = MedicineType.objects.all()
    serializer_class = MedicineTypeSerializer

    def list(self, request, *args, **kwargs):
        if 'type_name' in request.GET:
            self.queryset = self.queryset.filter(type_name__icontains=request.GET['type_name'])
        return super().list(request, *args, *kwargs)


class MedicineWithPharmaciesViewSet(ReadOnlyModelViewSet):
    renderer_classes = (JSONRenderer,)

    queryset = None
    serializer_class = MedicineWithPharmaciesSerializer

    def list(self, request, *args, **kwargs):
        if 'id' in request.GET:
            self.queryset = Medicine.objects.filter(medicine_name__pk=request.GET['id'])
        else:
            self.queryset = Medicine.objects.all()
        return super().list(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@authentication_classes((SessionAuthentication,))
@renderer_classes((JSONRenderer,))
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
