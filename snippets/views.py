from typing import List, Optional

from django.http import Http404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetList(APIView):
    def get(self, request: Request, format: Optional[List[str]] = None) -> Response:
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format: Optional[List[str]] = None) -> Response:
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    def get_object(self, pk: int) -> Snippet:
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(
        self, request: Request, pk: int, format: Optional[List[str]] = None
    ) -> Response:
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(
        self, request: Request, pk: int, format: Optional[List[str]] = None
    ) -> Response:
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self, request: Request, pk: int, format: Optional[List[str]] = None
    ) -> Response:
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=204)
