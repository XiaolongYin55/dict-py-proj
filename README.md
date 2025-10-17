# Intro

## Install PyMySQL

```HTML
laurence@Mac-mini ~ % pip install PyMySQL
```

```HTML
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple/
Collecting PyMySQL
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/7c/4c/ad33b92b9864cbde84f259d5df035a6447f91891f5be77788e2a3892bce3/pymysql-1.1.2-py3-none-any.whl (45 kB)
Installing collected packages: PyMySQL
Successfully installed PyMySQL-1.1.2

[notice] A new release of pip is available: 24.2 -> 25.2
[notice] To update, run: pip install --upgrade pip
```

## Create a new file

```HTML
/Users/laurence/Desktop/python.proj/myDict
```

## Install django

```HTML
laurence@Mac-mini myDict % pip3 install django
```

```HTML
ooking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple/
Collecting django
  Using cached https://pypi.tuna.tsinghua.edu.cn/packages/8f/ef/81f3372b5dd35d8d354321155d1a38894b2b766f576d0abffac4d8ae78d9/django-5.2.7-py3-none-any.whl (8.3 MB)
Collecting asgiref>=3.8.1 (from django)
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/17/9c/fc2331f538fbf7eedba64b2052e99ccf9ba9d6888e2f41441ee28847004b/asgiref-3.10.0-py3-none-any.whl (24 kB)
Collecting sqlparse>=0.3.1 (from django)
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/a9/5c/bfd6bd0bf979426d405cc6e71eceb8701b148b16c21d2dc3c261efc61c7b/sqlparse-0.5.3-py3-none-any.whl (44 kB)
Installing collected packages: sqlparse, asgiref, django
Successfully installed asgiref-3.10.0 django-5.2.7 sqlparse-0.5.3

[notice] A new release of pip is available: 24.2 -> 25.2
[notice] To update, run: pip install --upgrade pip
```

## Check version

```HTML
laurence@Mac-mini myDict % python3 -m django --version

5.2.7
laurence@Mac-mini myDict % 
```

## Initial Proj File

```HTML
laurence@Mac-mini myDict % python3 -m django startproject myDict .
```

# Samle CRUD - Users

## Add users file

```HTML
python3 manage.py startapp users
```

## Install DRF

```HTML
laurence@Mac-mini ~ % pip3 install djangorestframework

[notice] A new release of pip is available: 24.2 -> 25.2
[notice] To update, run: pip install --upgrade pip

```



## Register App

```HTML
//open settings.py
//find `INSTALLED_APPS`，then add 'users'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',   # ← 新加的 app
]

```

## Define Modals

```HTML
//paste into models.py

import uuid
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])

    def __str__(self):
        return f"{self.username} ({self.name})"

```

## Create Serializer

```HTML
//create file 'serializers' in /users 
//paste into serilizers.py

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

```

## Create ViewSet for Sample CRUD

```HTML

//paste into users/views.py

from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

```

## Create urls.py

``` 
//create 'urls.py' in /users
//pasted into users/urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```

## Create myDict in DB

```HTML
laurence@Mac-mini ~ % mysql -u root -p;
mysql> create database myDict;

```

## Config DB

```HTML
//paste it into myDict/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myDict',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

```

## Let Djanggo using pymysql

```HTML
//open /myDict/__init__.py
//pate it into there

import pymysql
pymysql.install_as_MySQLdb()

```

## Test connection of DB

```HTML
laurence@Mac-mini myDict % python3 manage.py migrate
laurence@Mac-mini myDict % python3 manage.py runserver

//then open the url: http://127.0.0.1:8000/
```



## Migrate DB

```HTML
laurence@Mac-mini myDict % python3 manage.py makemigrations


laurence@Mac-mini myDict % python3 manage.py migrate


```

## Create CRUD Views

```HTML
//open users/views.py

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

```

## Config users/urls.py

```HTML
//paste into users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/<uuid:user_id>/', views.user_detail, name='user_detail'),
]

```

## Config Main urls

```HTML
//paste into myDict/urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  # 👈 新增
]

```

## Restart Proj

```HTML
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

System check identified no issues (0 silenced).
October 15, 2025 - 14:05:27
Django version 5.2.7, using settings 'myDict.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Project Tree

```HTML
mysite/
│
├── manage.py
├── mysite/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py       👈 主路由文件
│   └── ...
│
└── users/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── urls.py       👈 你刚刚贴的这段
    ├── views.py
    └── migrations/

```

 
# 自动化部署测试 - Fri Oct 17 22:39:51 +08 2025
 
# 🚀 自动化部署测试成功 - Fri Oct 17 22:47:19 +08 2025
 
# 🚀 自动化部署测试成功:) - Fri Oct 17 22:48:02 +08 2025
