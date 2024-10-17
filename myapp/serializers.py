from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username','email', 'password', 'password_confirm']

    # Handle validation of data
    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data["username"]).exists():
                raise serializers.ValidationError("username is Taken")
            
        if data['email']:
            if User.objects.filter(email = data["email"]).exists():
                raise serializers.ValidationError("email is Taken")
        
            
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove password_confirm from validated_data
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField() # custom field for the username

    class Meta:
        model = Client
        fields = ['id','client_name', 'created_at', 'created_by']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        # Automatically assign the 'created_by' field to the logged-in user's username
        validated_data['created_by'] = self.context['request'].user# Assign the username
        print(validated_data['created_by'])
        # Create and return the new Client instance
        return Client.objects.create(**validated_data)
    
    def get_created_by(self, obj):
        return obj.created_by.username 


class ProjectCreateSerializer(serializers.ModelSerializer):
    users = serializers.ListField(write_only = True) # List of user with(id and name)
    client = serializers.CharField(source = 'client.client_name', read_only = True)
    created_by = serializers.CharField(source = 'created_by.uername', read_only=True)

    class Meta:
        model = Project
        fields = ['id','project_name','client' ,'users', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by', 'client']

    def create(self, validated_data):
        users_data = validated_data.pop('users', [])

        client = self.context['client']
        request = self.context['request']
        project = Project.objects.create(**validated_data, client = client ,created_by= request.user)

        for user_data in users_data:
            user_id = user_data.get('id')
            try:
                user = User.objects.get(id = user_id)
                project.users.add(user)
            except User.DoesNotExist:
                raise serializers.ValidationError(f"User with id {user_id}")
        return project

    # Handle the Output of user field
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['users'] = [{'id': user.id, 'name': user.username} for user in instance.users.all()]
        return representation


class ProjectSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source = 'created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at', 'created_by']
        read_only_field = ['created_at', 'created_by']
     

class ClientDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()  # Custom field for the username
    projects = ProjectCreateSerializer(many=True, read_only=True)  # Nested serializer for projects

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']  # Include updated_at for detail
        read_only_fields = ['created_by', 'projects']  # Set read-only fields

    def get_created_by(self, obj):
        return obj.created_by.username 