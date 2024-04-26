from rest_framework import status
from rest_framework.views import APIView
from adrf.views import APIView as AsyncAPIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from .models import Blog
from account.custom_auth import AsyncPermission
from channels.db import database_sync_to_async





class BlogView(AsyncAPIView):
    permission_classes = [AsyncPermission]

    async def post(self, request, format=None):
        serializer = BlogSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            await serializer.asave()
            return Response({'msg':'ok'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    async def get(self, request, format=None):
        all_data = await database_sync_to_async(Blog.objects.all)()
        serializer = BlogSerializer(all_data, many=True)
        new_serializer = await serializer.adata
        return Response({'msg':new_serializer}, status=status.HTTP_200_OK)


