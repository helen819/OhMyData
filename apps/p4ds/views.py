from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import *
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import BaseUserCreationForm
from django import forms
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'p4ds/index.html')

class CustomUserCreationForm(BaseUserCreationForm):
    # 필수 필드들
    user_id = forms.CharField(required=True, max_length=50, label="로그인 아이디")
    password = forms.CharField(required=True, widget=forms.PasswordInput, label="로그인 비밀번호")
    username = forms.CharField(required=True, max_length=100, label="이름")
    role = forms.ChoiceField(
        required=True, 
        choices=[(1, '학생'), (2, '선생님')],
        label="역할"
    )

    # 선택 필드들
    email = forms.EmailField(required=False, max_length=100, label="이메일")
    phone = forms.CharField(required=False, max_length=20, label="전화번호")
    gender = forms.ChoiceField(
        required=False, 
        choices=[(1, '남성'), (2, '여성')],
        label="성별"
    )
    school_name = forms.CharField(required=False, max_length=100, label="학교명")
    user_grade = forms.CharField(required=False, max_length=20, label="학년")

    class Meta:
        model = Users  # Users 모델을 사용
        fields = [
            'user_id', 'password', 'username', 'role', 
            'email', 'phone', 'gender', 'school_name', 'user_grade'
        ]

@csrf_exempt # api 테스트를 위한 것으로 추후 삭제 예정
@require_POST
def user_register(request):
    try:

        body = request.body.decode('utf-8')
        logger.info("Request body: %s", body)     

        # 1. get input from JSON body
        data = json.loads(request.body)
        
        # 2. check required fields
        required_fields = ["user_id", "password", "username", "role"]
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    "success": False,
                    "message": f"{field} 필수 필드가 누락되었습니다."
                }, status=400)
        
        # 3. retrieve data fields
        user_id = data.get("user_id")
        password = data.get("password")
        username = data.get("username")
        role = data.get("role")
        email = data.get("email", "")  # Optional fields with default empty string
        phone = data.get("phone", "")
        gender = data.get("gender")
        school_name = data.get("school_name", "")
        user_grade = data.get("user_grade", "")

        # 4. check if user_id already exists
        if Users.objects.filter(user_id=user_id).exists():
            return JsonResponse({
                "success": False,
                "message": "이미 가입된 사용자입니다."
            }, status=400)

        # 5. create and save user
        user = Users.objects.create_user(
            user_id=user_id,
            password=password,
            username=username,
            role=role,
            email=email,
            phone=phone,
            gender=gender,
            school_name=school_name,
            user_grade=user_grade
        )

        # 6. prepare success response
        return JsonResponse({
            "success": True
        }, status=200)

    except Exception as e:
        # General error response
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)
    
@csrf_exempt # api 테스트를 위한 것으로 추후 삭제 예정
@require_POST
def user_login(request):
    try:

        body = request.body.decode('utf-8')
        logger.info("Request body: %s", body)
    
        data = json.loads(request.body)

        required_fields = ["user_id", "password"]
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    "success": False,
                    "message": f"{field} 필수 필드가 누락되었습니다."
                }, status=400)
                
        user_id = data.get('user_id')
        password = data.get('password')
        
        if Users.objects.filter(user_id=user_id).exists():
            user = authenticate(request, user_id=user_id, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"success": True}, status=200)
            else :
                return JsonResponse({
                        "success": False,
                        "message": "비밀번호가 틀렸습니다."
                    }, status=400)   
        else :
            return JsonResponse({
                "success": False,
                "message": "존재하지 않는 아이디입니다."
            }, status=400)
    except Exception as e:
        # General error response
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)   

@csrf_exempt # api 테스트를 위한 것으로 추후 삭제 예정
def user_logout(request):    
    logout(request)
    return JsonResponse({"success": True})

@csrf_exempt # api 테스트를 위한 것으로 추후 삭제 예정
@require_POST
def analytics_report(request):
    try:

        body = request.body.decode('utf-8')
        logger.info("Request body: %s", body)     

        # 1. get input from JSON body
        data = json.loads(request.body)
        
        # 2. check required fields
        required_fields = ["user_id"]
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    "success": False,
                    "message": f"{field} 필수 필드가 누락되었습니다."
                }, status=400)
        
        # 3. retrieve data fields
        user_id = data.get("user_id")

        # 4. Check if user exists
        if Users.objects.filter(user_id=user_id).exists():
            user = Users.objects.get(user_id=user_id)
            
            # 5. Prepare user data for response
            user_data = {
                "success": True,
                "user_id": user.user_id,
                "username": user.username,
                "role": "학생" if user.role == 1 else "선생님" if user.role == 2 else "미등록",
                "email": user.email,
                "phone": user.phone,
                "gender": "남성" if user.gender == 1 else "여성" if user.gender == 2 else "미등록",
                "school_name": user.school_name,
                "user_grade": user.user_grade,
                "created_at": user.created_at.strftime("%Y-%m-%d") if user.created_at else None,
            }
            return JsonResponse(user_data, status=200)

        else:
            # If user_id does not exist, return error response
            return JsonResponse({
                "success": False,
                "message": "존재하지 않는 사용자입니다."
            }, status=400)
    except Exception as e:
        # General error response
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)       

@csrf_exempt # api 테스트를 위한 것으로 추후 삭제 예정
@require_POST
def practice_set(request):
    try:
            
        body = request.body.decode('utf-8')
        logger.info("Request body: %s", body)     

        # 1. get input from JSON body
        data = json.loads(request.body)
        
        # 2. check required fields
        required_fields = ["user_id"]
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    "success": False,
                    "message": f"{field} 필수 필드가 누락되었습니다."
                }, status=400)
        
        # 3. retrieve data fields
        user_id = data.get("user_id")

        # 4. Check if user exists
        if Users.objects.filter(user_id=user_id).exists():
            # TODO
            return True
        else:
            # If user_id does not exist, return error response
            return JsonResponse({
                "success": False,
                "message": "존재하지 않는 사용자입니다."
            }, status=400)
    except Exception as e:
        # General error response
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=400)    

@csrf_exempt # api 테스트를 위한 것으로 추후 삭제 예정
@require_POST
def practice_complete(request):
    return True    