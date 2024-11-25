# test_api.py

import requests

# 配置 Flask 应用的基本 URL
BASE_URL = 'http://localhost:5000/api'


# 用户注册
def register_user(username, password, email):
    url = "http://localhost:5000/api/register"
    payload = {
        "username": username,
        "password": password,
        "email": email
    }
    try:
        response = requests.post(url, json=payload)
        print("响应状态码:", response.status_code)
        print("响应内容:", response.text)  # 打印原始响应内容
        return response.json()  # 如果是合法的 JSON，则继续解析
    except requests.exceptions.JSONDecodeError as e:
        print("JSON 解码失败:", e)
        return None
    except requests.exceptions.RequestException as e:
        print("请求失败:", e)
        return None


# 用户登录
def login_user(username, password):
    url = f'{BASE_URL}/login'
    payload = {
        'username': username,
        'password': password
    }
    response = requests.post(url, json=payload)
    print('登录用户响应:', response.status_code, response.json())
    if response.status_code == 200:
        return response.json().get('access_token')
    return None


# 创建角色
def create_character(token, name, profession):
    url = f'{BASE_URL}/characters'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'name': name,
        'profession': profession
    }
    response = requests.post(url, json=payload, headers=headers)
    print('创建角色响应:', response.status_code, response.json())
    return response


# 获取角色列表
def get_characters(token):
    url = f'{BASE_URL}/characters'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    print('获取角色列表响应:', response.status_code, response.json())
    return response


# 获取地图信息
def get_maps():
    url = f'{BASE_URL}/maps'
    response = requests.get(url)
    print('获取地图信息响应:', response.status_code, response.json())
    return response


# 示例测试流程
if __name__ == '__main__':
    # 定义测试用户信息
    test_username = 'game_user'
    test_password = '123456'
    test_email = 'player1@example.com'

    # 注册用户
    register_response = register_user(test_username, test_password, test_email)

    # 如果注册成功或用户已存在，尝试登录
    if register_response.status_code in [200, 201, 409]:
        token = login_user(test_username, test_password)

        if token:
            # 创建角色
            create_character(token, '李青', 'Swordmaster')

            # 获取角色列表
            get_characters(token)
        else:
            print('登录失败，无法获取 JWT 令牌。')
    else:
        print('用户注册失败。')

    # 获取地图信息（无需认证）
    get_maps()
