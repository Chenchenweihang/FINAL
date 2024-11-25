# 完整的关系图示意

以下是各模型之间关系的简要示意图：

CopyInsert
User
│
├── Character
│   ├── Inventory 
│   │   └── Item 
│   ├── Equipment 
│   │   └── Item 
│   ├── Battle 
│   │   └── Event 
│   └── Quest 
│       └── Event 
Map 
│ 
└── Event 
    ├── Battle 
    └── Quest

## 关系说明

- **User ↔ Character**: 一对多关系，一个用户可以拥有多个角色。
- **Character ↔ Inventory ↔ Item**: 多对多关系，通过 Inventory 表实现，一个角色可以拥有多个物品，一个物品可以属于多个角色的库存。
- **Character ↔ Equipment ↔ Item**: 多对多关系，通过 Equipment 表实现，一个角色可以装备多个物品，一个物品可以被多个角色装备。
- **Character ↔ Battle ↔ Event**: 多对多关系，通过 Battle 表实现，一个角色可以参与多个战斗，一个战斗关联一个事件。
- **Character ↔ Quest ↔ Event**: 多对多关系，通过 Quest 表实现，一个角色可以有多个任务，一个任务关联一个事件。
- **Map ↔ Event**: 一对多关系，一个地图可以包含多个事件。
- **Event ↔ Battle / Quest**: 一对多关系，一个事件可以关联多个战斗和任务。
