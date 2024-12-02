from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

# Vista protegida para el perfil de usuario
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Requiere autenticación

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


# Personalización del token para incluir más campos del usuario
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Vista para registrar usuarios
class RegisterView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generar tokens para el usuario recién registrado
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "Usuario registrado exitosamente",
                "user_id": user.id,
                "username": user.username,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista de conjunto de usuarios (CRUD)
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]  # Protege las vistas con autenticación


# Vista para cambiar la contraseña del usuario
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"error": "Contraseña actual incorrecta"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Contraseña actualizada correctamente"})


# Vista para obtener el usuario actual
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

