from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from.models import User
import jwt, datetime

# Create your views here.

# registro de usuarios

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# endpoint para login no sistema e autenticando usuario com jwt

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('Usuario não encontrado!')

        elif not user.check_password(password):
            raise AuthenticationFailed('Senha Incorreta!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


