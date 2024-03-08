from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Center
from .serializers import UserSerializer, CenterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.hashers import make_password
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login


# from .permissions import CustomPermission


class LoginAPIView(APIView):
    def post(self, request):
        # username = request.data.get('username')
        email = request.data.get('email')
        print(email)
        password = request.data.get('password')
        print(password)

        user = None

        if email:
            user = authenticate(request, email=email, password=password)
            print(user)

        if user is None:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid email or password', 'data':{ }}, status=status.HTTP_400_BAD_REQUEST)

        # if not check_password(password, user.password):
        #     return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        refresh = RefreshToken.for_user(user)

        # Save token in database
        user.token = str(refresh.access_token)
        user.save()

        serializer = UserSerializer(user)
        user_data = {
            'status': status.HTTP_200_OK,
            'message': 'Login successful',
            'data': serializer.data
        }
        return Response(user_data, status=status.HTTP_200_OK)

# class UpdatePasswordView(APIView):
#     def post(self, request):
#         user = request.user  # Assuming the user is authenticated
#         data = request.data
#
#         new_password = data.get('new_password')
#
#
#         if user.last_login is NULL:
#             user.password = make_password(new_password)
#         else:
#           return Response({'message':'This functionality is only for users who are first time logging in})
#
#         user.save()
#
#         return Response({'message': 'Password and/or username updated successfully'}, status=status.HTTP_200_OK)

class UserAPIViewList(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        role = request.data.get('role', None)
        if role not in [2, 3]:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Invalid role', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)

        request.data['role'] = role
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if role in [2]:
                return Response({'status': status.HTTP_201_CREATED,'message': 'Trainer created successfully'}, status=status.HTTP_201_CREATED)
            elif role in [3]:
                return Response({'status': status.HTTP_201_CREATED, 'message': 'Trainee created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Failed to create user. Please check your input data.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        role = request.data.get('role', None)
        if role not in ['2', '3']:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid role', 'data': [{}]}, status=status.HTTP_400_BAD_REQUEST)

        users = CustomUser.objects.filter(role__id=role)
        user_data = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.role_type,
            'photo': user.photo.url if user.photo else None,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'contact': user.contact,
            'address': user.address,
            'center': user.center.center_name if user.center else None,
            'created_at': user.created_at,
            'modified_at': user.modified_at,
            'year_of_experience': user.year_of_experience,
            'training_type': user.training_type,
            'discount': str(user.discount),  # Convert DecimalField to string
            'fees_paid': user.fees_paid
        } for user in users]

        return Response({'status': status.HTTP_200_OK, 'message': 'retrieval successfull', 'data': user_data}, status=status.HTTP_200_OK)
        # serializer = UserSerializer(users, many=True)
        # user_data = {
        #     'status': status.HTTP_200_OK,
        #     'message': 'retrieval successfull',
        #     'data': serializer.data
        # }
        # return Response(user_data)

class UserAPIViewDetail(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
        # except CustomUser.DoesNotExist:
        #     return Response({'error':'User not found'}, status=status.HTTP_404_NOT_FOUND)
            role_id = user.role_id
            if role_id not in [2, 3]:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid Role'}, status=status.HTTP_400_BAD_REQUEST)
            request.data['role'] = role_id

            user_detail = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.role_type,
                'photo': user.photo.url if user.photo else None,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender,
                'contact': user.contact,
                'address': user.address,
                'center': user.center.center_name if user.center else None,
                'created_at': user.created_at,
                'modified_at': user.modified_at,
                'year_of_experience': user.year_of_experience,
                'training_type': user.training_type,
                'discount': str(user.discount),  # Convert DecimalField to string
                'fees_paid': user.fees_paid
            }
            return Response( {'status':status.HTTP_200_OK,'data':user_detail}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'status':status.HTTP_200_OK, 'message': 'User not found', 'data':[{}]}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({'status':status.HTTP_404_NOT_FOUND, 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        role_id = user.role_id
        if role_id not in [2, 3]:
            return Response({'status':status.HTTP_400_BAD_REQUEST, 'message': 'Invalid Role'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['role'] = role_id
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if role_id in [2]:
                return Response({'status': status.HTTP_200_OK, 'message': 'Trainer updated successfully'}, status=status.HTTP_200_OK)
            elif role_id in [3]:
                return Response({'status': status.HTTP_200_OK, 'message': 'Trainee updated successfully'}, status=status.HTTP_200_OK)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND,'message': 'User not found', 'data': {}}, status=status.HTTP_404_NOT_FOUND)

        role_id = user.role_id
        if role_id not in [2, 3]:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Invalid role', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        request.data['role'] = role_id
        delete = user.delete()
        if delete:
            return Response({'status': status.HTTP_204_NO_CONTENT,'message': 'Deleted successfully', 'data': {}}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Deleted successfully', 'data': {}}, status=status.HTTP_400_BAD_REQUEST)


class CenterAPIViewList(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CenterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Center created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Failed to create center. Please check you input data'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        centers = Center.objects.all()
        data = [{
            'id': center.id,
            'center_name': center.center_name,
            'address':center.address
        } for center in centers]
        # serializer = CenterSerializer(centers, many=True)
        return Response(data, status=status.HTTP_200_OK)

class CenterAPIViewDetail(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            center = Center.objects.get(id=id)
            center_detail = {
                'id': center.id,
                'center_name': center.center_name,
                'address': center.address
            }
            return Response(center_detail, status=status.HTTP_200_OK)
        except Center.DoesNotExist:
            return Response({'error': 'Center not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            center = Center.objects.get(id=id)
        except Center.DoesNotExist:
            return Response({'error': 'Center not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CenterSerializer(center, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Center update successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        # try:
        #     center = Center.objects.get(center_id=center_id)
        # except Center.DoesNotExist:
        #     return Response({'error': 'Center not found'}, status=status.HTTP_404_NOT_FOUND)
        #
        # center.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

        try:
            center = Center.objects.get(id=id)
            center.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Center.DoesNotExist:
            return Response({'error': 'Center not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
