import matplotlib.pyplot as plt
import networkx as nx

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体字体
plt.rcParams['axes.unicode_minus'] = False

# 创建无向图
G = nx.Graph()

# 按层次分组节点
group1 = ['锦绣坊', '御龙殿', '琉璃宫']
group2 = ['安茂集会', '观星阁']
group3 = ['黑风寨', '叹息康河']
group4 = ['风云山脉', '雨落狂流之地', '中庭黑市']
group5 = ['涧谷入口', '葬神灵峰', '落日茂林', '万兽山林', '雨歌海林']
group6 = ['迷雾沼泽', '藏龙洞天', '涧龙神国', '血雨焚林', '八荒石林']

nodes = group1 + group2 + group3 + group4 + group5 + group6
G.add_nodes_from(nodes)

# 指定节点位置
pos = {}
# 层次1: y=5
for i, node in enumerate(group1):
    pos[node] = (i + 1, 5)
# 层次2: y=4
for i, node in enumerate(group2):
    pos[node] = (i + 1, 4)
# 层次3: y=3
for i, node in enumerate(group3):
    pos[node] = (i + 1, 3)
# 层次4: y=2
for i, node in enumerate(group4):
    pos[node] = (i + 1, 2)
# 层次5: y=1
for i, node in enumerate(group5):
    pos[node] = (i + 1, 1)
# 层次6: y=0
for i, node in enumerate(group6):
    pos[node] = (i + 1, 0)

# 添加边
edges = [
    ('锦绣坊', '御龙殿'),
    ('御龙殿', '琉璃宫'),
    ('御龙殿', '观星阁'),
    ('琉璃宫', '观星阁'),
    ('锦绣坊', '安茂集会'),
    ('黑风寨', '安茂集会'),
    ('黑风寨', '雨落狂流之地'),
    ('叹息康河', '雨落狂流之地'),
    ('中庭黑市', '雨落狂流之地'),
    ('风云山脉', '雨落狂流之地'),
    ('风云山脉', '涧谷入口'),
    ('涧谷入口', '葬神灵峰'),
    ('涧谷入口', '迷雾沼泽'),
    ('葬神灵峰', '藏龙洞天'),
    ('迷雾沼泽', '藏龙洞天'),
    ('藏龙洞天', '涧龙神国'),
    ('涧龙神国', '落日茂林'),
    ('落日茂林', '雨歌海林'),
    ('雨歌海林', '八荒石林'),
    ('八荒石林', '血雨焚林'),
    ('血雨焚林', '万兽山林'),
    ('万兽山林', '落日茂林'),
    ('万兽山林', '八荒石林'),
    ('八荒石林', '血雨焚林')
]

G.add_edges_from(edges)

# 定义节点分组和对应颜色
node_groups = {
    '组1': ['锦绣坊', '御龙殿', '琉璃宫', '安茂集会', '观星阁'],
    '组2': ['黑风寨', '叹息康河', '雨落狂流之地', '中庭黑市', '风云山脉'],
    '组3': ['涧谷入口', '葬神灵峰', '迷雾沼泽', '藏龙洞天', '涧龙神国'],
    '组4': ['万兽山林', '血雨焚林', '落日茂林', '雨歌海林', '八荒石林']
}

group_colors = {
    '组1': 'lightblue',
    '组2': 'lightgreen',
    '组3': 'orange',
    '组4': 'pink'
}

# 生成节点颜色
colors = []
for node in G.nodes():
    for group, nodes in node_groups.items():
        if node in nodes:
            colors.append(group_colors[group])

# 绘制图形
plt.figure(figsize=(12, 8))  # 设置图形大小
nx.draw(G, pos, with_labels=True, node_shape='s', node_size=5000, font_size=14, edge_color='gray', node_color=colors)

# 添加标题
plt.title('天道大陆地图先览', fontsize=16)

# 显示图形
plt.show()
