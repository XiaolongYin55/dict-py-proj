import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User

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

