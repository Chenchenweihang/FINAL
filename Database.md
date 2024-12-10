### 1. 数据库概述

我们需要设计一个包含多个表的关系型数据库。
这些表将存储用户信息、角色信息、技能、物品、地图、事件、战斗等数据。

### 2. 数据库表设计

以下是主要的数据库表及其字段设计：

1. **Users（用户表）**
    - `id` (INT, Primary Key, Auto Increment): 用户唯一标识
    - `username` (VARCHAR(80), Unique, Not Null): 用户名
    - `password` (VARCHAR(128), Not Null): 密码（注意：生产环境中请使用哈希加密）
    - `email` (VARCHAR(120), Unique, Not Null): 电子邮件
    - `created_at` (TIMESTAMP, Default CURRENT_TIMESTAMP): 创建时间

2. **Characters（角色表）**
    - `id` (INT, Primary Key, Auto Increment): 角色唯一标识
    - `user_id` (INT, Foreign Key to Users.id, Not Null): 所属用户
    - `name` (VARCHAR(80), Not Null): 角色名称
    - `profession` (ENUM('剑侠', '武者', '医士', '刺客', '道士'), Not Null): 职业
    - `level` (INT, Default 1): 等级
    - `experience` (INT, Default 0): 经验值
    - `health` (INT, Default 100): 生命值
    - `attack` (INT, Default 10): 攻击力
    - `defense` (INT, Default 5): 防御力
    - `mana` (INT, Default 50): 法力值
    - `created_at` (TIMESTAMP, Default CURRENT_TIMESTAMP): 创建时间

3. **Skills（技能表）**
    - `id` (INT, Primary Key, Auto Increment): 技能唯一标识
    - `profession` (ENUM('剑侠', '武者', '医士', '刺客', '道士'), Not Null): 职业
    - `name` (VARCHAR(80), Not Null): 技能名称
    - `description` (TEXT, Not Null): 技能描述
    - `level_required` (INT, Not Null): 解锁所需等级
    - `cooldown` (INT, Not Null): 冷却回合数
    - `mana_cost` (INT, Not Null): 法力消耗
    - `effect` (JSON, Not Null): 技能效果

4. **Items（物品表）**
    - `id` (INT, Primary Key, Auto Increment): 物品唯一标识
    - `name` (VARCHAR(80), Not Null): 物品名称
    - `type` (ENUM('武器', '防具', '饰品', '法宝'), Not Null): 物品类型
    - `base_attribute` (JSON, Not Null): 基础属性
    - `extra_attribute` (JSON, Nullable): 额外属性
    - `set_id` (INT, Foreign Key to Sets.id, Nullable): 所属套装

5. **Sets（套装表）**
    - `id` (INT, Primary Key, Auto Increment): 套装唯一标识
    - `name` (VARCHAR(80), Not Null): 套装名称
    - `bonus` (JSON, Not Null): 套装加成

6. **CharacterItems（角色物品表）**
    - `id` (INT, Primary Key, Auto Increment): 唯一标识
    - `character_id` (INT, Foreign Key to Characters.id, Not Null): 所属角色
    - `item_id` (INT, Foreign Key to Items.id, Not Null): 物品
    - `equipped` (BOOLEAN, Default FALSE): 是否已装备

7. **Maps（地图表）**
    - `id` (INT, Primary Key, Auto Increment): 地图唯一标识
    - `name` (VARCHAR(80), Not Null): 地图名称
    - `description` (TEXT, Not Null): 地图描述
    - `level_required` (INT, Not Null): 进入所需等级

8. **Events（事件表）**
    - `id` (INT, Primary Key, Auto Increment): 事件唯一标识
    - `map_id` (INT, Foreign Key to Maps.id, Not Null): 所属地图
    - `description` (TEXT, Not Null): 事件描述
    - `event_type` (ENUM('战斗', '剧情', '环境'), Not Null): 事件类型
    - `conditions` (JSON, Not Null): 触发条件
    - `outcomes` (JSON, Not Null): 事件结果

9. **Battles（战斗表）**
    - `id` (INT, Primary Key, Auto Increment): 战斗唯一标识
    - `event_id` (INT, Foreign Key to Events.id, Not Null): 所属事件
    - `enemy_id` (INT, Foreign Key to Enemies.id, Not Null): 敌人
    - `battle_data` (JSON, Not Null): 战斗数据

10. **Enemies（敌人表）**
    - `id` (INT, Primary Key, Auto Increment): 敌人唯一标识
    - `name` (VARCHAR(80), Not Null): 敌人名称
    - `health` (INT, Not Null): 生命值
    - `attack` (INT, Not Null): 攻击力
    - `defense` (INT, Not Null): 防御力
    - `skills` (JSON, Not Null): 技能

### 3. 数据库关系图

```plaintext
Users 1---* Characters
Characters *---* CharacterItems *---1 Items
Items *---1 Sets
Maps 1---* Events
Events 1---* Battles
Battles *---1 Enemies
```

### 4. 数据库设计说明

- **Users 表**: 存储用户的基本信息，包括用户名、密码和电子邮件。`username` 和 `email` 字段设置为唯一，以防止重复注册。

- **Characters 表**: 存储用户创建的角色信息。通过 `user_id` 外键与 `Users` 表关联，一个用户可以拥有多个角色。

- **Skills 表**: 存储不同职业的技能信息。通过 `profession` 字段区分不同职业的技能。

- **Sets 表**: 存储套装信息，每个套装有一个名称和对应的加成效果。

- **Items 表**: 存储游戏中的物品信息，包括武器、防具、饰品和法宝。每个物品可以属于一个套装（`set_id`）。

- **CharacterItems 表**: 关联角色与物品，表示一个角色拥有哪些物品以及这些物品是否已装备。

- **Maps 表**: 存储游戏中的地图信息，包括地图名称、描述和进入该地图所需的最低等级。

- **Events 表**: 存储在不同地图中可能触发的事件。每个事件关联一个地图，并包含事件描述、类型、触发条件和事件结果。

- **Enemies 表**: 存储游戏中的敌人信息，包括名称、生命值、攻击力、防御力和技能。

- **Battles 表**: 存储与事件相关的战斗信息，关联具体的事件和敌人，并包含战斗数据。
