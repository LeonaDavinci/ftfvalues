# FTF Values 网站数据爬取与开发指南

## 一、网站技术分析

### 1.1 技术栈
- 前端框架：Base44 平台构建（基于 React 的单页应用）
- 数据加载：JavaScript 动态渲染（无需页面刷新）
- 路由：客户端路由（SPA 模式）

### 1.2 可访问页面（静态内容）
- ✅ 首页 (/) - 部分内容可抓取
- ✅ 使用指南 (/UseGuide) - 完全可抓取
- ✅ 传奇物品 (/Legendaries) - 完全可抓取
- ✅ 史诗物品 (/Epics) - 完全可抓取
- ⚠️ 稀有物品 (/Rares) - 动态加载，需浏览器渲染
- ⚠️ 普通物品 (/Commons) - 动态加载，需浏览器渲染
- ⚠️ 套装 (/Sets) - 动态加载，需浏览器渲染
- ⚠️ 更新日志 (/Changelog) - 动态加载，需浏览器渲染

---

## 二、完整数据爬取方案

### 方案A：使用浏览器自动化（推荐）

使用 Playwright / Puppeteer / Selenium 进行动态页面渲染后爬取：

```javascript
// 使用 Playwright 爬取示例
const { chromium } = require('playwright');

async function scrapeFTFValues() {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    
    // 爬取 Legendaries
    await page.goto('https://ftf-values.base44.app/Legendaries');
    await page.waitForLoadState('networkidle');
    const legendaries = await page.$$eval('.item-card', cards => {
        return cards.map(card => ({
            name: card.querySelector('.item-name')?.textContent,
            value: card.querySelector('.item-value')?.textContent,
            stability: card.querySelector('.stability-tag')?.textContent,
            demand: card.querySelector('.demand-level')?.textContent,
        }));
    });
    
    // 爬取 Epics
    await page.goto('https://ftf-values.base44.app/Epics');
    await page.waitForLoadState('networkidle');
    // ... 同理
    
    await browser.close();
    return { legendaries, epics, rares, commons };
}
```

### 方案B：抓包分析 API 接口

Base44 应用通常通过 API 接口获取数据：

1. 打开浏览器开发者工具（F12）
2. 切换到 Network（网络）标签
3. 访问目标页面（如 /Rares）
4. 查看 XHR/Fetch 请求，找到数据 API 端点
5. 直接调用 API 获取数据（通常返回 JSON）

**常见 Base44 API 模式：**
```
GET https://ftf-values.base44.app/api/items?rarity=rare
GET https://ftf-values.base44.app/api/sets
```

### 方案C：使用 Python + Selenium

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def scrape_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    # 等待内容加载
    time.sleep(3)
    
    items = []
    item_cards = driver.find_elements(By.CSS_SELECTOR, '.item-card')
    
    for card in item_cards:
        item = {
            'name': card.find_element(By.CSS_SELECTOR, '.item-name').text,
            'value': card.find_element(By.CSS_SELECTOR, '.item-value').text,
            'rarity': url.split('/')[-1].rstrip('s').capitalize(),
        }
        items.append(item)
    
    driver.quit()
    return items

# 爬取所有稀有度
rarities = ['Legendaries', 'Epics', 'Rares', 'Commons']
all_data = {}
for rarity in rarities:
    url = f'https://ftf-values.base44.app/{rarity}'
    all_data[rarity.lower()] = scrape_page(url)

with open('ftf_values_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)
```

---

## 三、已收集数据结构总结

### 3.1 稀有度层级（4级）

| 层级 | 英文标识 | 物品数量 | 总价值 |
|--------|----------|----------|----------|
| 传奇 | Legendaries | 190 | 4503 |
| 史诗 | Epics | 59 | 581 |
| 稀有 | Rares | （待爬取） | （待爬取） |
| 普通 | Commons | （待爬取） | （待爬取） |

### 3.2 物品核心字段（7个）

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 物品名称 |
| rarity | enum | 稀有度（4级） |
| value | int | 基础价值 |
| value_range | string | 价值区间（可选） |
| stability | enum | 稳定性标签（8种） |
| status | enum | 状态标签（3种，可选） |
| demand | int | 需求量（1-10） |

### 3.3 标签体系

**稳定性标签（8种）：**
- Rising（上涨中）、Doing Well（表现良好）、Improving（改善中）
- Stable（稳定）、Fluctuating（波动中）
- Struggling（挣扎中）、Receding（回落中）、Dropping（下跌中）

**状态标签（3种）：**
- Overpaid For（溢价）、Underpaid For（折价）、Niche（小众）

**需求量（10级）：**
- 10：极高（即时交易）~ 1：无（无交易兴趣）

---

## 四、开发建议

### 4.1 数据库初始化顺序

```sql
-- 1. 先插入标签数据
INSERT INTO stability_tags (name, display_name, display_name_cn) VALUES 
('Rising', 'Rising', '上涨中'),
('Doing Well', 'Doing Well', '表现良好'),
('Improving', 'Improving', '改善中'),
('Stable', 'Stable', '稳定'),
('Fluctuating', 'Fluctuating', '波动中'),
('Struggling', 'Struggling', '挣扎中'),
('Receding', 'Receding', '回落中'),
('Dropping', 'Dropping', '下跌中');

-- 2. 插入需求量数据
INSERT INTO demand_levels (level, name, name_cn) VALUES 
(10, 'Extremely High', '极高'),
(9, 'Very High', '很高'),
-- ... 以此类推

-- 3. 插入稀有度数据
INSERT INTO rarities (name, display_name, display_name_cn, sort_order) VALUES 
('legendary', 'Legendary', '传奇', 1),
('epic', 'Epic', '史诗', 2),
('rare', 'Rare', '稀有', 3),
('common', 'Common', '普通', 4);

-- 4. 最后插入物品数据（依赖以上三张表）
```

### 4.2 API 接口设计建议

```
GET    /api/items              # 获取物品列表（支持筛选、排序、分页）
GET    /api/items/:id          # 获取单个物品详情
GET    /api/items/rarity/:r   # 按稀有度获取物品
GET    /api/sets              # 获取套装列表
GET    /api/sets/:id          # 获取单个套装详情
GET    /api/changelog         # 获取更新日志
GET    /api/staff             # 获取管理团队
```

### 4.3 前端页面路由设计

```
/                   # 首页
/guide              # 使用指南
/changelog          # 更新日志
/faq                # 常见问题
/sets               # 套装列表
/items/legendaries  # 传奇物品
/items/epics        # 史诗物品
/items/rares       # 稀有物品
/items/commons     # 普通物品
/items/:id          # 物品详情
/admin              # 管理后台（需登录）
```

---

## 五、下一步行动建议

1. **完成数据爬取**：使用方案A或B获取Rares和Commons数据
2. **设计UI原型**：参考 ftf-values.base44.app 的布局设计
3. **搭建开发环境**：按技术选型建议搭建前后端
4. **数据库初始化**：使用本文档提供的SQL建表
5. **导入种子数据**：将爬取的数据导入数据库

---

*指南结束*
