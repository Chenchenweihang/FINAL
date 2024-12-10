# API 文档

## 目录

1. [用户认证](#用户认证)
   - [注册用户](#注册用户)
   - [登录用户](#登录用户)
2. [角色管理](#角色管理)
   - [创建角色](#创建角色)
   - [获取角色列表](#获取角色列表)
   - [获取角色详情](#获取角色详情)
   - [更新角色信息](#更新角色信息)
   - [删除角色](#删除角色)
3. [技能管理](#技能管理)
   - [获取职业技能列表](#获取职业技能列表)
   - [学习技能](#学习技能)
   - [升级技能](#升级技能)
   - [获取角色技能列表](#获取角色技能列表)
4. [地图管理](#地图管理)
   - [获取地图列表](#获取地图列表)
   - [获取地图详情](#获取地图详情)
5. [任务系统](#任务系统)
   - [创建任务](#创建任务)
   - [获取任务详情](#获取任务详情)
   - [分配任务](#分配任务)
   - [获取角色任务列表](#获取角色任务列表)
   - [更新角色任务状态](#更新角色任务状态)
6. [背包管理](#背包管理)
   - [添加物品到背包](#添加物品到背包)
   - [移除物品从背包](#移除物品从背包)
   - [使用物品](#使用物品)
   - [获取角色背包](#获取角色背包)
   - [装备/卸下物品](#装备卸下物品)
7. [物品管理](#物品管理)
   - [获取所有物品](#获取所有物品)
   - [获取物品详情](#获取物品详情)
   - [创建物品](#创建物品)
   - [更新物品信息](#更新物品信息)
   - [删除物品](#删除物品)
8. [战斗管理](#战斗管理)
   - [获取战斗详情](#获取战斗详情)
   - [执行战斗动作](#执行战斗动作)
   - [获取战斗状态效果](#获取战斗状态效果)
9. [事件管理](#事件管理)
   - [获取事件详情](#获取事件详情)
   - [触发事件](#触发事件)

---

## 用户认证

### 注册用户

- **URL**: `/auth/register`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "username": "testuser",
      "password": "testpass",
      "email": "testuser@example.com"
  }
  ```

- **成功响应**:
  - **状态码**: `201 Created`
  - **内容**:

    ```json
    {
        "message": "注册成功"
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

    或

    ```json
    {
        "message": "用户名已存在"
    }
    ```

    或

    ```json
    {
        "message": "电子邮件已存在"
    }
    ```

### 登录用户

- **URL**: `/auth/login`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "username": "testuser",
      "password": "testpass"
  }
  ```

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "message": "登录成功",
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "testuser@example.com",
            "created_at": "2024-04-27T12:34:56"
        }
    }
    ```

- **错误响应**:
  - **状态码**: `401 Unauthorized`
  - **内容**:

    ```json
    {
        "message": "用户名或密码错误"
    }
    ```

    或

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

---

## 角色管理

### 创建角色

- **URL**: `/characters/`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "user_id": 1,
      "name": "李剑",
      "profession": "剑侠"
  }
  ```

- **成功响应**:
  - **状态码**: `201 Created`
  - **内容**:

    ```json
    {
        "message": "角色创建成功",
        "character_id": 1
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

    或

    ```json
    {
        "message": "无效的职业"
    }
    ```

    或

    ```json
    {
        "message": "用户不存在"
    }
    ```

### 获取角色列表

- **URL**: `/characters/?user_id=1`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "characters": [
            {
                "id": 1,
                "name": "李剑",
                "profession": "剑侠",
                "level": 1,
                "experience": 0,
                "health": 100,
                "attack": 10,
                "defense": 5,
                "mana": 50,
                "inventory_capacity": 20,
                "created_at": "2024-04-27T12:34:56"
            }
        ]
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "缺少 user_id 参数"
    }
    ```

    或

    ```json
    {
        "message": "未找到角色"
    }
    ```

### 获取角色详情

- **URL**: `/characters/<int:character_id>`
  - **示例**: `/characters/1`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "character": {
            "id": 1,
            "user_id": 1,
            "name": "李剑",
            "profession": "剑侠",
            "level": 1,
            "experience": 0,
            "health": 100,
            "attack": 10,
            "defense": 5,
            "mana": 50,
            "inventory_capacity": 20,
            "created_at": "2024-04-27T12:34:56"
        }
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "角色不存在"
    }
    ```

### 更新角色信息

- **URL**: `/characters/<int:character_id>`
  - **示例**: `/characters/1`
- **方法**: `PUT`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "name": "李剑改",
      "profession": "武者"
  }
  ```

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "message": "角色信息已更新"
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "无效的职业"
    }
    ```

    或

    ```json
    {
        "message": "角色不存在"
    }
    ```

### 删除角色

- **URL**: `/characters/<int:character_id>`
  - **示例**: `/characters/1`
- **方法**: `DELETE`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "message": "角色已删除"
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "角色不存在"
    }
    ```

---

## 技能管理

### 获取职业技能列表

- **URL**: `/skills/<profession>`
  - **示例**: `/skills/剑侠`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "skills": [
            {
                "id": 1,
                "name": "剑气斩",
                "description": "使用剑气远程攻击敌人，对单体目标造成物理伤害，并有概率眩晕1回合。",
                "level_required": 4,
                "cooldown": 2,
                "mana_cost": 30,
                "effect": {
                    "damage_type": "physical",
                    "target": "single",
                    "stun_chance": 0.3,
                    "stun_duration": 1
                }
            }
        ]
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "无效的职业"
    }
    ```

### 学习技能

- **URL**: `/skills/learn`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "character_id": 1,
      "skill_id": 1
  }
  ```

- **成功响应**:
  - **状态码**: `201 Created`
  - **内容**:

    ```json
    {
        "message": "技能学习成功",
        "character_skill_id": 1
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "角色等级不足以学习该技能"
    }
    ```

    或

    ```json
    {
        "message": "角色已学习该技能"
    }
    ```

    或

    ```json
    {
        "message": "技能职业不匹配"
    }
    ```

    或

    ```json
    {
        "message": "角色不存在"
    }
    ```

    或

    ```json
    {
        "message": "技能不存在"
    }
    ```

### 升级技能

- **URL**: `/skills/upgrade`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "character_id": 1,
      "skill_id": 1
  }
  ```

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "message": "技能升级成功",
        "new_level": 2
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "角色等级不足以升级该技能"
    }
    ```

    或

    ```json
    {
        "message": "角色未学习该技能"
    }
    ```

    或

    ```json
    {
        "message": "技能不存在"
    }
    ```

### 获取角色技能列表

- **URL**: `/skills/character/<int:character_id>`
  - **示例**: `/skills/character/1`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "character_skills": [
            {
                "character_skill_id": 1,
                "skill_id": 1,
                "name": "剑气斩",
                "description": "使用剑气远程攻击敌人，对单体目标造成物理伤害，并有概率眩晕1回合。",
                "level_required": 4,
                "cooldown": 2,
                "mana_cost": 30,
                "effect": {
                    "damage_type": "physical",
                    "target": "single",
                    "stun_chance": 0.3,
                    "stun_duration": 1
                },
                "level": 1
            }
        ]
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "角色不存在"
    }
    ```

---

## 地图管理

### 获取地图列表

- **URL**: `/maps/`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`
- **查询参数**:
  - `parent_map`（可选）：过滤某个上属地图的二级地图。

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "maps": [
            {
                "id": 1,
                "name": "安茂集会",
                "description": "都城最繁华的区域，各种奇珍异宝可在此交易。",
                "level_required": 1,
                "parent_map": "天都城"
            }
        ]
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "未找到地图"
    }
    ```

### 获取地图详情

- **URL**: `/maps/<int:map_id>`
  - **示例**: `/maps/1`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "map": {
            "id": 1,
            "name": "安茂集会",
            "description": "都城最繁华的区域，各种奇珍异宝可在此交易。",
            "level_required": 1,
            "parent_map": "天都城"
        }
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "地图不存在"
    }
    ```

---

## 任务系统

### 创建任务

- **URL**: `/tasks/`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "name": "主线任务1",
      "description": "完成天都城的某个事件。",
      "task_type": "主线",
      "requirements": {
          "level": 5
      },
      "rewards": {
          "experience": 500,
          "item_id": 3
      }
  }
  ```

- **成功响应**:
  - **状态码**: `201 Created`
  - **内容**:

    ```json
    {
        "message": "任务创建成功",
        "task_id": 1
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

    或

    ```json
    {
        "message": "无效的任务类型"
    }
    ```

### 获取任务详情

- **URL**: `/tasks/<int:task_id>`
  - **示例**: `/tasks/1`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "task": {
            "id": 1,
            "name": "主线任务1",
            "description": "完成天都城的某个事件。",
            "task_type": "主线",
            "requirements": {
                "level": 5
            },
            "rewards": {
                "experience": 500,
                "item_id": 3
            },
            "created_at": "2024-04-27T12:34:56"
        }
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "任务不存在"
    }
    ```

### 分配任务

- **URL**: `/tasks/assign`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "character_id": 1,
      "task_id": 1
  }
  ```

- **成功响应**:
  - **状态码**: `201 Created`
  - **内容**:

    ```json
    {
        "message": "任务已分配",
        "character_task_id": 1
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "任务已分配给该角色"
    }
    ```

    或

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

    或

    ```json
    {
        "message": "角色不存在"
    }
    ```

    或

    ```json
    {
        "message": "任务不存在"
    }
    ```

### 获取角色任务列表

- **URL**: `/tasks/character/<int:character_id>`
  - **示例**: `/tasks/character/1`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "character_tasks": [
            {
                "character_task_id": 1,
                "task_id": 1,
                "name": "主线任务1",
                "description": "完成天都城的某个事件。",
                "task_type": "主线",
                "status": "未开始",
                "progress": {}
            }
        ]
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "未找到角色任务"
    }
    ```

    或

    ```json
    {
        "message": "角色不存在"
    }
    ```

### 更新角色任务状态

- **URL**: `/tasks/update/<int:character_task_id>`
  - **示例**: `/tasks/update/1`
- **方法**: `PUT`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "status": "进行中",
      "progress": {
          "event_completed": true
      }
  }
  ```

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "message": "任务状态已更新"
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "无效的状态"
    }
    ```

    或

    ```json
    {
        "message": "缺少状态参数"
    }
    ```

    或

    ```json
    {
        "message": "角色任务不存在"
    }
    ```

---

## 背包管理

### 添加物品到背包

- **URL**: `/inventory/add`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "character_id": 1,
      "item_id": 2
  }
  ```

- **成功响应**:
  - **状态码**: `201 Created`
  - **内容**:

    ```json
    {
        "message": "物品已添加到背包"
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "背包已满"
    }
    ```

    或

    ```json
    {
        "message": "角色已拥有该物品"
    }
    ```

    或

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

    或

    ```json
    {
        "message": "角色不存在"
    }
    ```

    或

    ```json
    {
        "message": "物品不存在"
    }
    ```

### 移除物品从背包

- **URL**: `/inventory/remove`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "character_id": 1,
      "item_id": 2
  }
  ```

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "message": "物品已从背包中移除"
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "物品不在角色背包中"
    }
    ```

    或

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

### 使用物品

- **URL**: `/inventory/use`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "character_id": 1,
      "item_id": 3
  }
  ```

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "message": "使用龙鳞项链，恢复了50生命值"
    }
    ```

    或

    ```json
    {
        "message": "使用玄铁护甲，攻击力增加了20"
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "该物品无法使用"
    }
    ```

    或

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

    或

    ```json
    {
        "message": "物品不在角色背包中"
    }
    ```

### 获取角色背包

- **URL**: `/inventory/<int:character_id>`
  - **示例**: `/inventory/1`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "inventory": [
            {
                "item_id": 2,
                "name": "玄铁护甲",
                "type": "防具",
                "base_attribute": {"defense": 20},
                "extra_attribute": null,
                "equipped": false
            }
        ]
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "角色不存在"
    }
    ```

### 装备/卸下物品

- **URL**: `/inventory/equip`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "character_id": 1,
      "item_id": 2
  }
  ```

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "message": "物品装备状态已更新",
        "equipped": true
    }
    ```

    或

    ```json
    {
        "message": "物品装备状态已更新",
        "equipped": false
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

    或

    ```json
    {
        "message": "角色不存在"
    }
    ```

    或

    ```json
    {
        "message": "物品不存在"
    }
    ```

    或

    ```json
    {
        "message": "物品不在角色背包中"
    }
    ```

---

## 物品管理

### 获取所有物品

- **URL**: `/items/`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "items": [
            {
                "id": 1,
                "name": "青龙剑",
                "type": "武器",
                "base_attribute": {"attack": 15},
                "extra_attribute": {"critical_chance": 10},
                "set_id": 1
            }
        ]
    }
    ```

### 获取物品详情

- **URL**: `/items/<int:item_id>`
  - **示例**: `/items/1`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "item": {
            "id": 1,
            "name": "青龙剑",
            "type": "武器",
            "base_attribute": {"attack": 15},
            "extra_attribute": {"critical_chance": 10},
            "set_id": 1
        }
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "物品不存在"
    }
    ```

### 创建物品

- **URL**: `/items/create`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "name": "玄铁护甲",
      "type": "防具",
      "base_attribute": {"defense": 20},
      "extra_attribute": null,
      "set_id": 1
  }
  ```

- **成功响应**:
  - **状态码**: `201 Created`
  - **内容**:

    ```json
    {
        "message": "物品创建成功",
        "item_id": 2
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

    或

    ```json
    {
        "message": "无效的物品类型"
    }
    ```

    或

    ```json
    {
        "message": "套装不存在"
    }
    ```

### 更新物品信息

- **URL**: `/items/<int:item_id>`
  - **示例**: `/items/1`
- **方法**: `PUT`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "name": "玄铁护甲升级版",
      "type": "防具",
      "base_attribute": {"defense": 25},
      "extra_attribute": {"health_bonus": 50},
      "set_id": 1
  }
  ```

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "message": "物品信息已更新"
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "无效的物品类型"
    }
    ```

    或

    ```json
    {
        "message": "套装不存在"
    }
    ```

    或

    ```json
    {
        "message": "物品不存在"
    }
    ```

### 删除物品

- **URL**: `/items/<int:item_id>`
  - **示例**: `/items/1`
- **方法**: `DELETE`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "message": "物品已删除"
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "物品不存在"
    }
    ```

---

## 战斗管理

### 获取战斗详情

- **URL**: `/battles/<int:battle_id>`
  - **示例**: `/battles/1`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "battle": {
            "id": 1,
            "event_id": 2,
            "enemy": {
                "id": 1,
                "name": "黑风帮头目",
                "health": 150,
                "attack": 20,
                "defense": 10,
                "skills": {
                    "skill1": "猛攻",
                    "skill2": "防御"
                }
            },
            "battle_data": {
                "enemy_skills": ["猛攻", "防御"],
                "loot": {
                    "experience": 100,
                    "item_id": 2
                },
                "enemy_health": 150,
                "player_health": 100
            },
            "status_effects": []
        }
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "战斗不存在"
    }
    ```

### 执行战斗动作

- **URL**: `/battles/<int:battle_id>/action`
  - **示例**: `/battles/1/action`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:

  ```json
  {
      "action": "attack",
      "character_id": 1
  }
  ```

  或者使用技能：

  ```json
  {
      "action": "skill",
      "character_id": 1,
      "skill_id": 2
  }
  ```

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**（攻击示例）:

    ```json
    {
        "result": "ongoing",
        "player_health": 95,
        "enemy_health": 140
    }
    ```

    或（使用技能示例）:

    ```json
    {
        "result": "ongoing",
        "player_health": 90,
        "enemy_health": 130,
        "damage_dealt": 20,
        "damage_received": 10
    }
    ```

    或（战斗胜利）:

    ```json
    {
        "result": "victory",
        "experience_gained": 100
    }
    ```

    或（战斗失败）:

    ```json
    {
        "result": "defeat"
    }
    ```

- **错误响应**:
  - **状态码**: `400 Bad Request`
  - **内容**:

    ```json
    {
        "message": "使用技能时需要提供 skill_id"
    }
    ```

    或

    ```json
    {
        "message": "法力值不足"
    }
    ```

    或

    ```json
    {
        "message": "角色未学习该技能"
    }
    ```

    或

    ```json
    {
        "message": "缺少必要参数"
    }
    ```

    或

    ```json
    {
        "message": "技能不存在"
    }
    ```

### 获取战斗状态效果

- **URL**: `/battles/<int:battle_id>/status`
  - **示例**: `/battles/1/status`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "status_effects": [
            {
                "id": 1,
                "target": "enemy",
                "effect_type": "stun",
                "duration": 1,
                "parameters": {}
            },
            {
                "id": 2,
                "target": "enemy",
                "effect_type": "bleed",
                "duration": 3,
                "parameters": {"damage_percent_hp": 0.05}
            }
        ]
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "战斗不存在"
    }
    ```

---

## 事件管理

### 获取事件详情

- **URL**: `/events/<int:event_id>`
  - **示例**: `/events/1`
- **方法**: `GET`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **状态码**: `200 OK`
  - **内容**:

    ```json
    {
        "event": {
            "id": 1,
            "map_id": 1,
            "description": "你在天都城的锦绣坊发现了一件奇珍异宝。",
            "event_type": "剧情",
            "conditions": {
                "level": 1
            },
            "outcomes": {
                "reward": {
                    "item_id": 1
                }
            }
        }
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "事件不存在"
    }
    ```

### 触发事件

- **URL**: `/events/trigger/<int:event_id>`
  - **示例**: `/events/1`
- **方法**: `POST`
- **Headers**: `Content-Type: application/json`

- **成功响应**:
  - **对于战斗事件**:
  
    ```json
    {
        "battle": {
            "battle_id": 1,
            "enemy": {
                "id": 1,
                "name": "黑风帮头目",
                "health": 150,
                "attack": 20,
                "defense": 10,
                "skills": {
                    "skill1": "猛攻",
                    "skill2": "防御"
                }
            },
            "battle_data": {
                "enemy_skills": ["猛攻", "防御"],
                "loot": {
                    "experience": 100,
                    "item_id": 2
                }
            }
        }
    }
    ```

  - **对于剧情和环境事件**:
  
    ```json
    {
        "outcome": {
            "reward": {
                "item_id": 1
            }
        }
    }
    ```

- **错误响应**:
  - **状态码**: `404 Not Found`
  - **内容**:

    ```json
    {
        "message": "事件不存在"
    }
    ```


### 已实现功能

1. **用户管理**：注册和登录。
2. **角色管理**：创建、获取、更新和删除角色。
3. **技能管理**：获取职业技能列表、学习技能、升级技能、获取角色技能列表。
4. **地图管理**：获取地图列表和详情。
5. **任务系统**：创建任务、获取任务详情、分配任务、获取角色任务列表、更新任务状态。
6. **背包管理**：添加物品到背包、移除物品、使用物品、获取背包内容、装备/卸下物品。
7. **物品管理**：获取所有物品、获取物品详情、创建物品、更新物品信息、删除物品。
8. **战斗管理**：获取战斗详情、执行战斗动作、获取战斗状态效果。
9. **事件管理**：获取事件详情、触发事件。
