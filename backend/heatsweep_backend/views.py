from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)

from rest_framework.response import Response
from rest_framework.views import APIView
class BoardView(APIView):
    def get(self, request):
        return Response([1, 2, 3])