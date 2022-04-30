import json
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from django.contrib.auth.hashers import check_password
from .models import *
from django.template.loader import get_template
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class AdminRegistrationApi(generics.GenericAPIView):
    serializer_class = AdminRegistrationSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            Email = request.data.get('Email')

            otp = generateOTP()
            created_at = datetime.datetime.now()
            user1 = OtpModel(AdminId=user.id, otp=otp).save()
            htmly = get_template('adminregistration_otp.html')
            d = {'otp': otp, 'created_at': created_at}
            subject, from_email, to = 'Confirmation mail for Registration', settings.FROM_EMAIL, Email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, settings.FROM_EMAIL, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return Response({
                'message': 'Successful',
                'Result': AdminRegistrationSerializer(user).data,
                'HasError': False,
                'status': 200
            })
        except Exception as e:
            return Response({
                'message': 'Fail',
                'Result': [],
                'HasError': True,
                'status': 400
            })


class AdminLoginApi(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer

    def post(self, request, format=None):
        Email = request.data.get('Email')
        MobileNumber = request.data.get('MobileNumber')

        password = request.data.get('Password')

        if AdminRegisterModel.objects.filter(Email=Email).first():
            user = AdminRegisterModel.objects.filter(Email=Email).first()
            if check_password(password, user.Password):
                user.save()
                s = AdminLoginSerializer(user, partial=True)
                s.is_valid(raise_exception=True)
                s.save()
                serializer_class = AdminRegistrationSerializer(user).data
                return Response({
                    'message': 'Successful',
                    'Result': serializer_class,
                    'HasError': False,
                    'status': 200
                })
            else:
                return Response({
                    'message': 'Fail',
                    'Result': [],
                    'HasError': True,
                    'status': 400
                })
        elif AdminRegisterModel.objects.filter(MobileNumber=Email).first():
            user = AdminRegisterModel.objects.filter(MobileNumber=Email).first()
            if check_password(password, user.Password):

                user.save()

                s = AdminLoginSerializer(user, partial=True)
                s.is_valid(raise_exception=True)
                s.save()
                serializer_class = AdminRegistrationSerializer(user).data
                return Response({
                    'message': 'Sucessfull',
                    'Result': serializer_class,
                    'HasError': False,
                    'status': 200
                })
            else:
                return Response({
                    'message': 'UserNOTFound',
                    'Result': [],
                    'HasError': True,
                    'status': 400
                })
        return Response({
            'message': 'PleaseEnterValidDetails',
            'Result': [],
            'HasError': True,
            'status': 400
        })


class GetAllCustomers(APIView):
    serializer_class = AdminRegistrationSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            queryset = AdminRegisterModel.objects.all()
            serializer_class = AdminRegistrationSerializer(queryset, many=True)
            return Response({'Message': 'Successful',
                             'Result': serializer_class.data,
                             'HasError': False,
                             'Status': 200})
        except Exception as e:
            return Response({
                'message': 'Fail',
                'Result': [],
                'HasError': True,
                'status': 400
            })


class MoviesPostApi(generics.GenericAPIView):
    serializer_class = MoviesPostSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response({
                'message': 'Successful',
                'Result': MoviesPostSerializer(user).data,
                'HasError': False,
                'status': 200
            })
        except Exception as e:
            return Response({
                'message': 'Fail',
                'Result': [],
                'HasError': True,
                'status': 400
            })


class GetAllMovies(APIView):
    serializer_class = MoviesPostSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            queryset = MovieListModel.objects.all()
            serializer_class = MoviesPostSerializer(queryset, many=True)
            return Response({'Message': 'Successful',
                             'Result': serializer_class.data,
                             'HasError': False,
                             'Status': 200})
        except Exception as e:
            return Response({
                'message': 'Fail',
                'Result': [],
                'HasError': True,
                'status': 400
            })


class GetAllMoviesInDescendingOrder(APIView):
    serializer_class = MoviesPostSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            queryset = MovieListModel.objects.all().order_by('-Rating')
            serializer_class = MoviesPostSerializer(queryset, many=True)
            return Response({'Message': 'Successful',
                             'Result': serializer_class.data,
                             'HasError': False,
                             'Status': 200})
        except Exception as e:
            return Response({
                'message': 'Fail',
                'Result': [],
                'HasError': True,
                'status': 400
            })


class GetAllMoviesInAssendingOrder(APIView):
    serializer_class = MoviesPostSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            queryset = MovieListModel.objects.all().order_by('Rating')
            serializer_class = MoviesPostSerializer(queryset, many=True)
            return Response({'Message': 'Successful',
                             'Result': serializer_class.data,
                             'HasError': False,
                             'Status': 200})
        except Exception as e:
            return Response({
                'message': 'Fail',
                'Result': [],
                'HasError': True,
                'status': 400
            })


class GetMovieByDay(APIView):
    serializer_class = MoviesPostSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
            queryset = MovieListModel.objects.filter(date__startswith=datetime.date.today())
            serializer_class = MoviesPostSerializer(queryset, many=True)
            return Response({'Message': 'Successful',
                             'Result': serializer_class.data,
                             'HasError': False,
                             'Status': 200})
        except Exception as e:
            return Response({
                'message': 'Fail',
                'Result': [],
                'HasError': True,
                'status': 400
                })


class MovieNotificationApi(generics.GenericAPIView):
    serializer_class = AdminRegistrationSerializer

    def post(self, request, *args, **kwargs):
        try:
            ReleaseDate=request.data.get('ReleaseDate')
            CloseDate=request.data.get('CloseDate')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            Email = request.data.get('Email')

            otp = generateOTP()
            created_at = datetime.datetime.now()
            user1 = OtpModel(AdminId=user.id, otp=otp).save()
            htmly = get_template('adminregistration_otp.html')
            d = {'otp': otp, 'created_at': created_at,'ReleaseDate':ReleaseDate,'CloseDate':CloseDate}
            subject, from_email, to = 'Confirmation mail for Registration', settings.FROM_EMAIL, Email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, settings.FROM_EMAIL, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return Response({
                'message': 'Successful',
                'Result': AdminRegistrationSerializer(user).data,
                'HasError': False,
                'status': 200
            })
        except Exception as e:
            return Response({
                'message': 'Fail',
                'Result': [],
                'HasError': True,
                'status': 400
            })