from django.shortcuts import render
from django.http.response import JsonResponse
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, generics, status,views
from django.contrib.auth import login
from . models import *
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.response import Response
from knox.models import AuthToken

# Create your views here.



#Register View
class RegisterApi(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status":True,
                "message": "User Created Successfully.",
                "data": serializer.data,
                "token": AuthToken.objects.create(user)[1]
            })
        return Response({
                "status":False,
                "message": "Some thing Went Wrong",                
                "error": serializer.errors,
            })
#for register get
class registerget(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRegisterSerializer
    def get(self,request,id,*args, **kwargs):
        try: 
            prod = User.objects.get(id=id) 
        except User.DoesNotExist: 
            return JsonResponse({'message': 'User does not exist',"status": False} )

        if request.method == 'GET':
            prodSerializer = UserRegisterSerializer(prod)
            
             
            # return JsonResponse(tutorial_serializer.data) 

            result = {
                "status": True,
                "data": prodSerializer.data,
                "message": " Detials Fetched Successfully",
                
                }
            return JsonResponse(result,safe=False)


##Login View    
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            alldetails=User.objects.all().filter(email=request.data["email"]).values('id','name','is_admin','is_customer')
            # print(type(alldetails))    
            login(request, user)
            return Response({
                "status":True,
                "data": alldetails,
                "message": "Login Successfully.",
                "token": AuthToken.objects.create(user)[1],
            })
        return Response({
                "status":False,
                "error": serializer.errors,
                "message": "Some thing Went Wrong",                
            })
        
class logout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self ,request):
         print(request.user)
         return Response({'sucess' : "Hurray you are authenticated"})

##user Details Post
class UserDeatilsPost(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerializer
    def post(self, request, *args, **kwargs):
        serializer = UserDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "User Details saved Successfully.",
                "status":True,
            })
        return Response({
                "error": serializer.errors,
                "message": "Some thing Went Wrong",
                "status":False
            })

##user Details Put Api
class UserDeatilsPut(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerializer   
    def put(self,request,id,format=None):
        if request.method=='PUT':
            queryset = userDetails.objects.get(id=id)
            queryset_serialzer = UserDetailsSerializer(queryset,data=request.data,partial=True)
            if queryset_serialzer.is_valid():
                queryset_serialzer.save()
                success={
                    "message" :" Detials Updated Successfully",
                    "status" : True,
                    "data" : queryset_serialzer.data,
                }
                return Response(success)
            error={
                "message": queryset_serialzer.errors,
                "status": False,
            }
            return Response(error)

##Category Details Get Api
class UserDeatilsGet(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerializer
    def get(self,request):
        try:
            queryset = userDetails.objects.all().order_by('-id')
            serializer = UserDetailsSerializer(queryset , many = True)
            return JsonResponse({'status': True,'message': 'Details Successfully Fethced' ,'data' :serializer.data})
        except userDetails.DoesNotExist: 
            return Response({'status': False,'message': 'Details Not Available!'}) 