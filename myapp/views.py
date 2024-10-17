from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project
from .serializers import UserRegistrationSerializer, ClientSerializer, ClientDetailSerializer, ProjectCreateSerializer, ProjectSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# User Registration view
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# USer Login and Generate token
class UserLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'user logged-in',
                'token': str(token),
            })
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# Handle create client and get list of client
class ClientListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            client = serializer.save()
            return Response(ClientSerializer(client).data, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Handle Client detial
class ClientDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        projects = client.projects.all()
        client_data = ClientDetailSerializer(client).data
        client_data['projects'] = ProjectSerializer(projects, many=True).data
        return Response(client_data)

    def put(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientDetailSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, client_id):
        try:
            client = get_object_or_404(Client, id=client_id)
        except Client.DoesNotExist:
            return Response({'detail':'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        
        request_data = request.data.copy()
        request_data['client'] = client.id

        serializer = ProjectCreateSerializer(data=request.data, context={'request': request, 'client': client})
        
        if serializer.is_valid():
            project = serializer.save()
            output_serializer = ProjectCreateSerializer(project)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user_projects = Project.objects.all() # List of Project
        serializer = ProjectSerializer(user_projects, many=True)
        return Response(serializer.data)
