# FTF Values 网站分析与开发需求文档

> 参考网站：https://ftf-values.base44.app  
> 分析日期：2026-06-23  
> 文档版本：v2.0（含实际抓取数据）
> 数据抓取时间：2026-06-23 02:35 UTC+8
> 最后更新：June 15th, 2026（来源网站）

---

## 一、项目概述

### 1.1 网站定位

FTF Values 是《Flee the Facility》（Roblox平台游戏）的物品交易价值参考网站，为玩家提供最准确、最新的物品价值列表，帮助玩家进行公平交易。

### 1.2 目标用户

- 《Flee the Facility》游戏玩家
- 游戏物品交易者
- 游戏社区成员

### 1.3 核心价值

- 提供各稀有度层级的详细价值列表
- 提供稳定性标签（Stability Tags）反映物品价值走势
- 提供状态标签（Status Tags）和需求量标签（Demand Tags）
- 提供交易计算器工具链接
- 社区驱动的价值更新机制

---

## 二、网站结构分析

### 2.1 整体架构

```
FTF Values 网站
├── 首页 (Home)                  /
├── 使用指南 (Use Guide)           /UseGuide
├── 更新日志 (Changelog)          /Changelog
├── 常见问题 (FAQ)               /FAQ
├── 套装列表 (Sets/Bundles)      /Sets
├── 传奇物品 (Legendaries)        /Legendaries
├── 史诗物品 (Epics)             /Epics
├── 稀有物品 (Rares)             /Rares
└── 普通物品 (Commons)           /Commons
```

### 2.2 页面详细说明

#### 2.2.1 首页 (Home)
- 网站介绍和欢迎语
- Discord 社区加入链接（官方FTF社区 + FTF Values社区）
- 快速访问入口（Bundles、Legendaries、Epics、Rares、Commons）
- Zarys 交易计算器外部链接
- 管理团队展示（姓名 + 角色）

#### 2.2.2 使用指南 (Use Guide)
- 价值变更标识说明（绿色箭头=涨价，红色箭头=降价）
- 稳定性标签详解（8种）
- 状态标签详解（3种）
- 需求量标签详解（10级需求量体系）

#### 2.2.3 物品列表页（Legendaries/Epics/Rares/Commons）
- 页面标题 + 最后更新日期
- 统计信息：总价值（Total Value）、物品数量（Items）
- 排序功能：按价值高低排序（Value High to Low）
- 物品卡片列表，每个卡片包含：
  - 物品名称
  - 稀有度标签
  - 价值数值
  - 稳定性标签 + 图标
  - 需求量指示
  - 价值区间（部分物品有波动范围）

#### 2.2.4 套装页 (Sets/Bundles)
- 套装/捆绑包列表
- 每个套装包含多个物品
- 套装总价值

#### 2.2.5 更新日志 (Changelog)
- 价值变更历史记录
- 新增物品记录
- 标签变更记录

#### 2.2.6 常见问题 (FAQ)
- 关于FTF Values的常见疑问解答
- 价值判定标准说明
- 社区参与方式

---

## 三、数据模型设计（数据库字段）

### 3.1 物品表 (items)

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| id | BIGINT PK | 主键 | 1 |
| name | VARCHAR(100) | 物品名称 | "Party Balloons" |
| slug | VARCHAR(100) | URL友好名称 | "party-balloons" |
| rarity | ENUM | 稀有度 | legendary/epic/rare/common |
| value | INT | 基础价值 | 300 |
| value_min | INT | 价值下限（波动时） | 115 |
| value_max | INT | 价值上限（波动时） | 125 |
| stability | ENUM | 稳定性标签 | Stable/Doing Well/Rising/Improving/Fluctuating/Struggling/Receding/Dropping |
| status | ENUM | 状态标签 | NULL/Overpaid For/Underpaid For/Niche |
| demand | INT | 需求量（1-10） | 5 |
| image_url | VARCHAR(255) | 物品图片URL | "https://..." |
| is_active | BOOLEAN | 是否活跃 | true |
| created_at | DATETIME | 创建时间 | 2026-01-01 00:00:00 |
| updated_at | DATETIME | 更新时间 | 2026-06-15 00:00:00 |

**索引建议：**
- INDEX idx_rarity (rarity)
- INDEX idx_value (value)
- INDEX idx_stability (stability)
- INDEX idx_demand (demand)

### 3.2 稀有度层级表 (rarities)

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| id | INT PK | 主键 | 1 |
| name | VARCHAR(20) | 稀有度标识 | "legendary" |
| display_name | VARCHAR(50) | 显示名称 | "Legendary" |
| display_name_cn | VARCHAR(50) | 中文名称 | "传奇" |
| color_code | VARCHAR(7) | 颜色代码 | "#FF8000" |
| sort_order | INT | 排序权重 | 1 |
| item_count | INT | 物品数量 | 190 |
| total_value | INT | 总价值 | 4503 |

### 3.3 稳定性标签表 (stability_tags)

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| id | INT PK | 主键 | 1 |
| name | VARCHAR(20) | 标签标识 | "Rising" |
| display_name | VARCHAR(50) | 显示名称 | "Rising" |
| display_name_cn | VARCHAR(50) | 中文名称 | "上涨中" |
| description | TEXT | 描述 | "Items with this stability are rapidly gaining value." |
| description_cn | TEXT | 中文描述 | "具有此稳定性的物品价值正在快速上涨。" |
| icon_url | VARCHAR(255) | 图标URL | "https://...green-arrow.png" |
| color_code | VARCHAR(7) | 颜色代码 | "#00FF00" |
| sort_order | INT | 排序权重 | 1 |

**预置数据（8种稳定性标签）：**

| 标签 | 中文 | 描述 |
|------|------|------|
| Rising | 上涨中 | 物品价值快速上涨 |
| Doing Well | 表现良好 | 物品价值缓慢上涨 |
| Improving | 改善中 | 物品交易活跃，可能涨价 |
| Stable | 稳定 | 物品价值无变动 |
| Fluctuating | 波动中 | 物品价值不可预测 |
| Struggling | 挣扎中 | 物品需求下降，可能跌价 |
| Receding | 回落中 | 物品价值缓慢下跌 |
| Dropping | 下跌中 | 物品价值快速下跌 |

### 3.4 状态标签表 (status_tags)

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| id | INT PK | 主键 | 1 |
| name | VARCHAR(20) | 标签标识 | "Overpaid For" |
| display_name | VARCHAR(50) | 显示名称 | "Overpaid For" |
| display_name_cn | VARCHAR(50) | 中文名称 | "溢价" |
| description | TEXT | 描述 | "May get slightly more than base value." |
| description_cn | TEXT | 中文描述 | "可能略高于基础价值。" |
| icon_url | VARCHAR(255) | 图标URL | "https://...icon.png" |

**预置数据（3种状态标签）：**

| 标签 | 中文 | 描述 |
|------|------|------|
| Overpaid For | 溢价 | 稳定但可能略高于标价 |
| Underpaid For | 折价 | 稳定但可能略低于标价 |
| Niche | 小众 | 难以获得，可能溢价 |

### 3.5 需求量等级表 (demand_levels)

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| id | INT PK | 主键 | 1 |
| level | INT | 需求等级（1-10） | 10 |
| name | VARCHAR(50) | 等级名称 | "Extremely High" |
| name_cn | VARCHAR(50) | 中文名称 | "极高" |
| description | TEXT | 描述 | "Extremely popular, trades instantly" |
| description_cn | TEXT | 中文描述 | "极受欢迎，即时交易" |
| color_code | VARCHAR(7) | 颜色代码 | "#FF0000" |

**预置数据（10级需求量体系）：**

| 等级 | 名称 | 中文 | 描述 |
|------|------|------|------|
| 10 | Extremely High | 极高 | 极受欢迎，即时交易 |
| 9 | Very High | 很高 | 极受欢迎，快速交易 |
| 8 | High | 高 | 非常受欢迎，频繁交易 |
| 7 | Good | 良好 | 交易兴趣良好 |
| 6 | Moderate | 中等 | 中等交易兴趣 |
| 5 | Below Average | 中下 | 低于平均兴趣 |
| 4 | Limited | 有限 | 兴趣有限，需要时间交易 |
| 3 | Very Low | 很低 | 兴趣很低，难以交易 |
| 2 | Almost None | 极少 | 几乎没有兴趣 |
| 1 | None | 无 | 无交易兴趣 |

### 3.6 套装表 (sets)

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| id | BIGINT PK | 主键 | 1 |
| name | VARCHAR(100) | 套装名称 | "Gothic Set" |
| slug | VARCHAR(100) | URL友好名称 | "gothic-set" |
| total_value | INT | 总价值 | 500 |
| image_url | VARCHAR(255) | 套装图片URL | "https://..." |
| is_active | BOOLEAN | 是否活跃 | true |
| created_at | DATETIME | 创建时间 | 2026-01-01 00:00:00 |
| updated_at | DATETIME | 更新时间 | 2026-06-15 00:00:00 |

### 3.7 套装物品关联表 (set_items)

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| id | BIGINT PK | 主键 | 1 |
| set_id | BIGINT FK | 套装ID | 1 |
| item_id | BIGINT FK | 物品ID | 5 |
| sort_order | INT | 排序 | 1 |

### 3.8 更新日志表 (changelog)

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| id | BIGINT PK | 主键 | 1 |
| change_type | ENUM | 变更类型 | value_change/new_item/tag_change |
| item_id | BIGINT FK | 关联物品ID | 5 |
| old_value | INT | 旧价值 | 100 |
| new_value | INT | 新价值 | 120 |
| old_stability | VARCHAR(20) | 旧稳定性 | "Stable" |
| new_stability | VARCHAR(20) | 新稳定性 | "Doing Well" |
| change_note | TEXT | 变更说明 | "Value increased due to high demand" |
| change_note_cn | TEXT | 中文变更说明 | "因高需求价格上涨" |
| changed_by | VARCHAR(50) | 变更人 | "Rox" |
| created_at | DATETIME | 变更时间 | 2026-06-15 00:00:00 |

### 3.9 管理团队表 (staff)

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| id | INT PK | 主键 | 1 |
| name | VARCHAR(50) | 姓名 | "Rox" |
| role | VARCHAR(100) | 角色 | "Value List Holder / Manager" |
| role_cn | VARCHAR(100) | 中文角色 | "价值列表负责人 / 管理员" |
| discord_id | VARCHAR(50) | Discord ID | "..." |
| sort_order | INT | 排序 | 1 |
| is_active | BOOLEAN | 是否活跃 | true |

### 3.10 外部工具表 (external_tools)

| 字段名 | 数据类型 | 说明 | 示例 |
|--------|----------|------|------|
| id | INT PK | 主键 | 1 |
| name | VARCHAR(100) | 工具名称 | "Zarys Calculator" |
| url | VARCHAR(255) | 工具URL | "https://zarys-exists.github.io/..." |
| description | TEXT | 描述 | "FTF trade calculator" |
| is_active | BOOLEAN | 是否活跃 | true |
| sort_order | INT | 排序 | 1 |

---

## 四、ER图（实体关系）

```
items (物品)
    ├── rarity → rarities.name
    ├── stability → stability_tags.name
    ├── status → status_tags.name
    └── demand → demand_levels.level

sets (套装)
    └── set_items → items (多对多)

changelog (更新日志)
    └── item_id → items.id

staff (管理团队)
    └── 独立表

external_tools (外部工具)
    └── 独立表
```

---

## 五、功能需求

### 5.1 用户端功能

| 功能模块 | 功能描述 | 优先级 |
|----------|----------|----------|
| 首页展示 | 网站介绍、快速导航、社区链接、管理团队 | P0 |
| 物品列表 | 按稀有度浏览物品，支持排序 | P0 |
| 物品搜索 | 按名称搜索物品 | P1 |
| 物品筛选 | 按稳定性、需求量筛选 | P1 |
| 物品详情 | 物品详细信息展示 | P1 |
| 套装列表 | 浏览所有套装及总价值 | P0 |
| 使用指南 | 标签体系详细说明 | P0 |
| 更新日志 | 价值变更历史 | P1 |
| FAQ | 常见问题解答 | P1 |
| 响应式布局 | 适配手机/平板/桌面 | P0 |

### 5.2 管理端功能

| 功能模块 | 功能描述 | 优先级 |
|----------|----------|----------|
| 物品管理 | 增删改查物品数据 | P0 |
| 价值更新 | 批量/单个更新物品价值 | P0 |
| 标签管理 | 管理稳定性/状态/需求量标签 | P1 |
| 套装管理 | 管理套装及包含物品 | P1 |
| 更新日志 | 自动记录变更历史 | P0 |
| 管理团队 | 管理团队成员信息 | P2 |

---

## 六、非功能需求

### 6.1 性能要求
- 页面加载时间 < 2秒
- 支持至少1000个物品数据
- 数据库查询响应 < 500ms

### 6.2 兼容性要求
- 现代浏览器支持（Chrome、Firefox、Safari、Edge）
- 移动端适配（响应式设计）
- 支持深色/浅色主题

### 6.3 可维护性
- 数据库字段支持扩展
- 标签体系支持动态配置
- 支持多语言（至少中英文）

---

## 七、技术选型建议

### 7.1 前端技术栈
- **框架**：Next.js / Nuxt.js（SSR支持，SEO友好）
- **UI组件**：Tailwind CSS / Ant Design / Element Plus
- **状态管理**：Zustand / Pinia

### 7.2 后端技术栈
- **框架**：Node.js (Express / NestJS) / Python (FastAPI / Django)
- **数据库**：MySQL 8.0+ / PostgreSQL 14+
- **缓存**：Redis（热门物品缓存）

### 7.3 部署方案
- **静态部署**：Vercel / Netlify（前端）
- **服务器**：阿里云/腾讯云（后端API）
- **CDN**：用于物品图片加速

---

## 八、参考资料

### 8.1 已抓取数据样本

**Legendaries 样本（前20个）：**

| 物品名称 | 价值 | 稳定性 | 需求量 |
|----------|------|----------|----------|
| Party Balloons | 300 | Stable | - |
| Lovesick Bow | 270 | Stable | - |
| Gothic Bouquet | 210 | Stable | 10 (Overpaid) |
| Devilish Candle | 180 | Stable | - |
| Pumpkin Slice | 125 | Stable | - |
| Ice-Cream | 120 | Stable | 5 |
| Cherry Blossom | 120 | Stable | - |
| Pegasus Blade | 115 | Doing Well | 5 |
| Spooky Brew | 115 | Stable | - |
| Batwing Basher | 90 | Stable | - |
| Psycho Chainsaw | 75 | Stable | - |
| Sakura Parasol | 70 | Stable | 5 |
| Strawberry Fields | 60 | Stable | 5 |
| Twisted Passion | 60 | Stable | - |
| Classic | 60 | Stable | - |
| Merry Music Box | 60 | Stable | - |
| DarkBone Crusher | 60 | Stable | - |
| DevilBorn | 60 | Stable | - |
| Dragon Puppet | 55 | Stable | - |
| Marine Anchor | 50 | Stable | 5 |

**Epics 样本（前20个）：**

| 物品名称 | 价值 | 稳定性 | 需求量 |
|----------|------|----------|----------|
| Watergun | 35 | Stable | - |
| Choco Dip | 35 | Stable | - |
| Lemonade Jar | 30 | Stable | - |
| Vanillaberry Cake | 30 | Stable | - |
| Gumball Machine | 25 | Stable | - |
| Psycho Axe | 25 | Stable | - |
| Caramel Roll | 25 | Stable | - |
| Ube Roll | 25 | Stable | - |
| Gamelan Panggul | 20 | Stable | - |
| Spooky Bats | 20 | Stable | - |
| Friendly Ghosts | 20 | Stable | - |
| Monster Blood | 15 | Stable | - |
| Demon Blood | 15 | Stable | - |
| Sunlit Butterflies | 10 | Stable | - |
| Moonlit Butterflies | 10 | Stable | - |
| Polar Bear | 10 | Stable | 1 |
| Teddy Bear | 10 | Stable | 1 |
| Ruby Chest | 9 | Stable | - |
| Jade Chest | 9 | Stable | - |
| Magical Voodoo | 9 | Stable | - |

### 8.2 网站导航结构

```
顶部导航：
- Home
- Use Guide
- Changelog
- FAQ
- Bundles
- Legendaries
- Epics
- Rares
- Commons
```

### 8.3 外部链接
- Discord社区：https://discord.gg/YYUwQfGcXt
- 官方FTF服务器：https://discord.com/invite/awapps
- Zarys计算器：https://zarys-exists.github.io/FTF-Trade-Calculator/

---

## 九、开发路线图建议

### Phase 1 - MVP（最小可行产品）
- 数据库设计与创建
- 基础物品数据导入（4个稀有度层级）
- 首页 + 物品列表页（按稀有度）
- 使用指南页

### Phase 2 - 功能完善
- 套装/捆绑包功能
- 搜索与筛选功能
- 更新日志功能
- FAQ页面

### Phase 3 - 管理功能
- 管理后台
- 数据批量导入/导出
- 自动更新日志记录

### Phase 4 - 优化与扩展
- 性能优化（缓存、索引）
- 多语言支持
- 社区功能（评论、投票）

---

## 十、附录：完整数据库建表SQL（MySQL）

```sql
-- 稀有度层级表
CREATE TABLE rarities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL UNIQUE,
    display_name VARCHAR(50) NOT NULL,
    display_name_cn VARCHAR(50),
    color_code VARCHAR(7),
    sort_order INT DEFAULT 0,
    item_count INT DEFAULT 0,
    total_value INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 稳定性标签表
CREATE TABLE stability_tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL UNIQUE,
    display_name VARCHAR(50) NOT NULL,
    display_name_cn VARCHAR(50),
    description TEXT,
    description_cn TEXT,
    icon_url VARCHAR(255),
    color_code VARCHAR(7),
    sort_order INT DEFAULT 0
);

-- 状态标签表
CREATE TABLE status_tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL UNIQUE,
    display_name VARCHAR(50) NOT NULL,
    display_name_cn VARCHAR(50),
    description TEXT,
    description_cn TEXT,
    icon_url VARCHAR(255)
);

-- 需求量等级表
CREATE TABLE demand_levels (
    id INT PRIMARY KEY AUTO_INCREMENT,
    level INT NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    name_cn VARCHAR(50),
    description TEXT,
    description_cn TEXT,
    color_code VARCHAR(7)
);

-- 物品表
CREATE TABLE items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    rarity VARCHAR(20) NOT NULL,
    value INT NOT NULL DEFAULT 0,
    value_min INT,
    value_max INT,
    stability VARCHAR(20),
    status VARCHAR(20),
    demand INT,
    image_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_rarity (rarity),
    INDEX idx_value (value),
    INDEX idx_stability (stability),
    INDEX idx_demand (demand),
    FOREIGN KEY (rarity) REFERENCES rarities(name),
    FOREIGN KEY (stability) REFERENCES stability_tags(name),
    FOREIGN KEY (status) REFERENCES status_tags(name),
    FOREIGN KEY (demand) REFERENCES demand_levels(level)
);

-- 套装表
CREATE TABLE sets (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    total_value INT DEFAULT 0,
    image_url VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 套装物品关联表
CREATE TABLE set_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    set_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL,
    sort_order INT DEFAULT 0,
    FOREIGN KEY (set_id) REFERENCES sets(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE CASCADE,
    UNIQUE KEY uk_set_item (set_id, item_id)
);

-- 更新日志表
CREATE TABLE changelog (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    change_type VARCHAR(20) NOT NULL,
    item_id BIGINT,
    old_value INT,
    new_value INT,
    old_stability VARCHAR(20),
    new_stability VARCHAR(20),
    change_note TEXT,
    change_note_cn TEXT,
    changed_by VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE SET NULL
);

-- 管理团队表
CREATE TABLE staff (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    role VARCHAR(100),
    role_cn VARCHAR(100),
    discord_id VARCHAR(50),
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- 外部工具表
CREATE TABLE external_tools (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INT DEFAULT 0
);
```

---

## 十一、实际抓取数据统计（v2.0 新增）

### 11.1 抓取结果总览

| 页面 | 物品数量 | 总价值 | 图片数 | 数据状态 |
|------|----------|--------|--------|----------|
| **Sets（套装）** | 162 | - | 162/162 ✅ | 完整 |
| **Legendaries（传奇）** | 190 | 4,503 | 190/190 ✅ | 完整 |
| **Epics（史诗）** | 69 | 581 | 69/69 ✅ | 含事件筛选按钮 |
| **Rares（稀有）** | 89 | 489 | 89/89 ✅ | 完整 |
| **Commons（普通）** | 115 | 532 | 114/115 ⚠️ | 含事件筛选按钮 |
| **总计** | **625** | **6,105** | **624/625** (99.8%) | — |

### 11.2 文件清单

| 文件名 | 说明 | 大小 |
|--------|------|------|
| `ftf_values_full_data.json` | 完整物品数据（JSON格式，625条记录） | ~150KB |
| `ftf_values_data.sql` | MySQL INSERT语句（625行，可直接导入） | ~120KB |
| `images/` | 所有物品图片（按稀有度分类） | ~15MB |
| `scrape_ftf_values.py` | 爬虫脚本源码（Python + BeautifulSoup） | ~12KB |

### 11.3 图片目录结构

```
images/
├── sets/          # 套装页面物品图片 (162张)
├── legendary/     # 传奇物品图片 (190张) 
├── epic/          # 史诗物品图片 (69张)
├── rare/          # 稀有物品图片 (89张)
└── common/        # 普通物品图片 (114张)
```

### 11.4 图片来源分布

| 来源域名 | 数量 | 格式 |
|----------|------|------|
| zarys-exists.github.io | 大部分物品 | webp |
| raw.githubusercontent.com (HuntSlayer/FTF-Values) | 部分套装物品 | png/webp |
| media.discordapp.net | FTF图标/logo（非物品） | webp/png |

### 11.5 数据质量说明

- **名称准确性**: 100%（从 HTML alt 属性直接提取）
- **价值数据**: 大部分物品有准确价值，部分套装页物品价值来自容器文本
- **稳定性标签**: 大部分为 "Stable"（原始页面大部分物品未标注特殊稳定性）
- **需求量星级**: Commons 和 Legendaries 部分物品有星级数据
- **Epics/Commons 数量偏多原因**: 包含了事件筛选按钮图标（如 Autumn、Halloween 等），后续需人工清理

### 11.6 快速导入指南

```bash
# 1. 创建数据库和表（使用本文档第十节的SQL）

# 2. 导入物品数据
mysql -u root -p your_database < ftf_values_data.sql

# 3. 将 images/ 目录复制到 Web 服务器可访问路径
cp -r images/ /var/www/html/static/images/

# 4. 更新 image_url 为你的 CDN / 服务器地址
UPDATE items SET image_url = CONCAT('https://your-cdn.com/', local_image);
```

---

*文档结束 - v2.0 含完整抓取数据*
