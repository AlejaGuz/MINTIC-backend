from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from sportClubApp.models.reserva import Reserva
from sportClubApp.serializers.reservaSerializer import ReservaSerializer

class ReservaDetailView(generics.RetrieveAPIView):
  queryset = Reserva.objects.all()
  serializer_class = ReservaSerializer
  permission_classes = (IsAuthenticated,)
 
  def get(self, request, *args, **kwargs):
    id_user_body = request.data.pop("id_user")

    token = request.META.get('HTTP_AUTHORIZATION')[7:]
    tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
    valid_data = tokenBackend.decode(token,verify=False)
    if valid_data['user_id'] != id_user_body:
      stringResponse = {'detail':'Unauthorized Request'}
      return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
    
    reserva= Reserva.objects.filter(id=kwargs['pk']).first()
    serializer = ReservaSerializer(reserva)
    return Response(serializer.data)