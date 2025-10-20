import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import logging

# 获取logger
logger = logging.getLogger(__name__)

@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = list(User.objects.values())
        return JsonResponse(users, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create(**data)
        return JsonResponse({'id': str(user.id), 'message': 'User created successfully'})

@csrf_exempt
def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': str(user.id),
            'username': user.username,
            'name': user.name,
            'password': user.password,
            'age': user.age,
            'gender': user.gender,
        })

    elif request.method == 'PUT':
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return JsonResponse({'message': 'User updated successfully'})

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})


@csrf_exempt
def login(request):
    """Login API"""
    print("=" * 50)
    print("🔍 LOGIN API 被调用了")
    print(f"请求方法: {request.method}")
    print("=" * 50)
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        print(f"📝 收到的username: {username}")
        print(f"📝 收到的password: {password}")
        
        # 验证必要字段
        if not username or not password:
            return JsonResponse({
                'status': 'failed',
                'message': 'Username and password are required'
            }, status=400)
        
        # 查询用户
        print(f"🔎 开始查询用户: {username}")
        user = User.objects.filter(username=username).first()
        
        if user:
            print(f"✅ 找到用户: {user.username}")
            print(f"📊 数据库中的密码: {user.password}")
            print(f"📊 接收到的密码: {password}")
            print(f"🔐 密码匹配: {user.password == password}")
        else:
            print(f"❌ 未找到用户: {username}")
        
        # 用户不存在或密码错误
        if not user or user.password != password:
            print("❌ 登录失败")
            return JsonResponse({
                'status': 'failed',
                'message': 'Username or password incorrect'
            }, status=401)
        
        # 登录成功，返回用户信息
        print("✅ 登录成功")
        return JsonResponse({
            'status': 'success',
            'user': {
                'id': str(user.id),
                'username': user.username,
                'name': user.name,
                'age': user.age,
                'gender': user.gender,
            }
        })
    
    except json.JSONDecodeError:
        print("❌ JSON解析错误")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)