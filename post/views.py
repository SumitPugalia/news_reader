from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from .models import Post, Tag  
from .serializers import PostSerializer, TagSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class PostView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        posts = Post.objects.all()
        tag_id = self.request.query_params.get('tag_id')
        if tag_id:
            posts = posts.filter(tags__id=tag_id)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        user=request.user 
        if serializer.is_valid(): 
            serializer.save(user=user)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 

    def put(self, request, pk, action, format=None):
        post = get_object_or_404(Post.objects.all(), pk=pk)
        likes = post.likes
        dislikes = post.dislikes
        viewed = post.viewed

        if action == 'like':
            likes = likes + 1
        
        if action == 'dislike':
            dislikes = dislikes + 1

        if action == 'viewed':
            viewed = viewed + 1

        serializer = PostSerializer(instance=post, data={'likes': likes, 'dislikes': dislikes, 'viewed': viewed}, partial=True)
        if serializer.is_valid(raise_exception=True):
            post = serializer.save()

        return Response({"success": "Post '{}' updated successfully".format(post.id)}) 

class TagView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 

