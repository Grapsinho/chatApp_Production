import bleach
from .forms import UsersForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from rest_framework import generics, status, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from .models import User
from rest_framework.views import APIView
from .tokens import create_jwt_for_user


def sanitize_input(user_input):
    cleaned_input = bleach.clean(user_input, tags=['p', 'strong', 'em'], attributes={'*': ['class']})
    return cleaned_input

def registration(request):
    form = UsersForm()

    context = {"form": form}
    return render(request, 'users/registration.html', context)

def loginView(request):
    return render(request, 'users/login.html')

class SignUpView(generics.GenericAPIView):

    """
    View for user registration.
    """

    serializer_class = UserSerializer
    permission_classes = []

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        print(serializer)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    View for user login and JWT token generation.
    """
    def post(self, request: Request):
        email = sanitize_input(request.data.get("email"))
        password = sanitize_input(request.data.get('password')) 

        user = authenticate(request, password=password, email=email)

        if user is not None:
            login(request, user)
            # When the user logs in, create tokens
            tokens = create_jwt_for_user(user)
            response = {
                "message": "User login successful",
                "user": email,
                "tokens": tokens,
            }

            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(
                data={"message": "Email or password is invalid"},
            )

def logoutForm(request):
    logout(request)
    return redirect('login')


from rest_framework import status
from .serializers import UserUpdateSerializer
from .permissions import VendorUpdatePermission
import os

class VendorUpdateView(APIView):
    permission_classes = [VendorUpdatePermission]

    def put(self, request, email):

        """
        mokled vaabdeitebt user profiles chveulebrivad magram tu poto araris mowodebuli mashin ubralod vigebt
        datadan da ase vanaxlet profiles
        """

        try:
            vendor = User.objects.get(email=email)
            
            # Create a copy of the request data
            data = request.data.copy()
            
            # Check if 'avatar' field exists in the data
            if 'avatar' in data:
                avatar_file = request.FILES.get('avatar')
                if avatar_file:
                    # Retrieve the path of the photo associated with the sub-product
                    photo_path = vendor.avatar.url

                    # Delete the photo file from the storage
                    if os.path.exists(f'static{photo_path}'):
                        os.remove(f'static{photo_path}')
                        
                    vendor.avatar = avatar_file
                # If the 'avatar' field is in data but has no file, remove it from data
                else:
                    data.pop('avatar')
            
            # Use the remaining data for the serializer
            serializer = UserUpdateSerializer(vendor, data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                response = {"message": "Vendor Updated", "data": serializer.data}
                return Response(data=response, status=status.HTTP_200_OK)
            
            # If serializer is not valid
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response(data={"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print(f"Error updating user: {e}")
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
def update_user(request, email):
    user = User.objects.get(email=email)
    return render(request, 'users/update-user.html', {'vend': user})