---
name: "exam-study-workbench"
description: "Creates a self-contained HTML exam study workbench with question bank, flashcards, smart import, knowledge points, tags, and progress tracking. Invoke when user wants to build a study/quiz/exam workbench website from question data (CSV/JSON/PDF/text)."
---

# Exam Study Workbench Builder

Creates a single-file HTML study workbench application from question bank data. Suitable for civil service exams (考公), professional certification exams, or any multiple-choice question bank.

## When to Invoke

- User wants to create a study/quiz/exam workbench website
- User has question data (CSV, JSON, PDF, plain text) and wants an interactive study tool
- User asks for a "学习工作台", "刷题工具", "题库网站", "考试复习工具"

## Architecture

The workbench is a **single HTML file** with embedded data (db.json injected via `/*__DB_JSON__*/null` marker). No server needed — all data and logic live in one file.

### Files Needed

1. **template.html** — The app template (HTML + CSS + JS)
2. **db.json** — Question bank data
3. **build.py** — Injects db.json into template.html to produce final HTML

### db.json Structure

```json
{
  "groups": [
    {
      "name": "行测",
      "categories": [
        {
          "name": "判断推理",
          "questions": [
            {
              "id": "q1",
              "title": "题目标题",
              "fields": {
                "错题": "题干全文（含选项）",
                "答案": "B",
                "错题解析": "解析内容",
                "知识点": "类比推理",
                "Tags": "对应关系,近义与反义"
              }
            }
          ]
        }
      ]
    }
  ]
}
```

### build.py

```python
import json, io, os
BASE = os.path.dirname(__file__)
tpl = io.open(os.path.join(BASE, "template.html"), encoding='utf-8').read()
db = io.open(os.path.join(BASE, "db.json"), encoding='utf-8').read()
db_safe = db.replace('</', '<\\/')
marker = '/*__DB_JSON__*/null'
out = tpl.replace(marker, db_safe)
io.open(os.path.join(BASE, "output.html"), 'w', encoding='utf-8').write(out)
```

## Core Features

### 1. Home Page (首页)
- Hero banner with total stats (questions, mastered, mastery rate)
- SVG progress ring showing mastery percentage
- Category navigation cards with per-category progress bars
- Quick action buttons (study, review, import)

### 2. Study Mode (学习模式)
- Single-question card view with prev/next navigation
- **Options are clickable** — clicking shows correct/wrong feedback (state clears on refresh)
- Answer and explanation hidden in collapsible sections by default
- Knowledge point prompts and similar questions in 2-column layout
- Question edit and delete buttons
- Personal notes (add/edit/delete, stored in localStorage)

### 3. Knowledge Points & Tags
- **12 fixed major categories** organized in 2 groups
- Each category has sub-knowledge-points, shown as expandable yellow items in sidebar
- Tags are user-customizable, searchable, and scoped to the current category
- Knowledge points are searchable and editable per question

### 4. Smart Import (智能导入)
- Paste raw text → auto-parse questions, options, answers, explanations
- Supports multiple formats: plain text, field-labeled, CSV
- Auto-completion: matches missing answers/explanations from existing question bank
- Per-question selectors for category, knowledge point, and tags
- Saved to localStorage "我的题库" (My Bank)

### 5. Flashcard Review (卡片复习)
- Review mastered questions as flashcards
- Select categories to review
- Spaced repetition via mastered/unmastered toggle

### 6. Sidebar Navigation
- Hierarchical: Group → Category (blue) → Knowledge Point (yellow, expandable)
- "全部题目", "我的题库", "其他（未分类）" entries
- Per-item question counts
- Search box for filtering

## Fixed Category & Knowledge Point System

This is the **standard classification** for civil service exam (考公) study. Do NOT create additional categories or knowledge points unless the user explicitly requests it.

### 行测 (Aptitude Test)

| Category | Knowledge Points |
|----------|-----------------|
| 判断推理 | 定义判断, 类比推理, 逻辑判断 |
| 言语理解 | 词语辨析, 成语辨析, 主旨概括, 细节理解, 语句填空, 语句排序 |
| 数量关系 | 数字特性, 容斥问题, 工程问题, 方程法, 其他问题 |
| 资料分析 | 增长量与增长率, 平均数与倍数, 速算技巧, 其他术语 |
| 图形推理 | 数量规律, 样式规律, 位置规律, 属性规律, 立体图形 |

### 常识 (General Knowledge)

| Category | Knowledge Points |
|----------|-----------------|
| 政治 | 时事政治, 中国特色社会主义, 马克思主义哲学, 马克思主义政治经济学, 毛泽东思想, 党史党建, 道德和礼仪 |
| 经济 | 宏观经济, 微观经济, 国际经济, 市场经济理论, 金融知识 |
| 文化 | 文学, 诗词, 艺术 |
| 地理环境 | 自然地理, 中国地理, 人文地理, 国情省情 |
| 历史 | 中国古代史, 近现代史 |
| 法律 | 宪法, 民法, 刑法, 行政法, 劳动法, 诉讼法, 法理学, 其他法 |
| 自然科技 | 基础科学, 高新技术, 生活常识, 科技史 |

## Embedded Tag Library

These tags are pre-loaded into the system as selectable options. Users can also create custom tags. Tags are scoped per category — when editing a question in a category, only that category's tags are shown by default.

### 判断推理
单定义, 多定义, 对应关系, 德摩根定理, 或关系, 推理判断, 语义关系-近义与反义, 集合关系-交叉关系, 集合关系-全同关系, 集合关系-包含关系, 集合关系-并列关系

### 言语理解
关联词-因果, 关联词-对策, 关联词-并列, 关联词-转折, 固定搭配, 填空-中间句, 实词填空, 对应关系-解释, 对应关系-重要词句, 成语辨析, 混搭填空, 细节判断, 行文脉络-分总, 行文脉络-分总分

### 数量关系
余数问题, 十字相乘法, 周期问题, 容斥问题, 工程问题, 年龄问题, 数列问题, 整除性, 方程法, 浓度问题, 溶质不变, 牛吃草问题, 等差数列

### 资料分析
（暂无预设标签，用户自行添加）

### 图形推理
一笔画, 元素数量, 其他规律, 图形叠加, 对称, 平移, 旋转, 点, 立体拼合, 线段数, 翻转, 面, 面积, 黑白运算

### 政治
11月热点新闻, 2023中央经济工作会议, "一带一路", "三步走"战略, "五位一体", "四个全面"战略, 三农问题, 中国梦, 中国特色大国外交, 中国精神, 中央一号文件, 中央经济工作会议, 中特, 主要任务, 主要内容, 习思想, 习思想理论贡献, 习近平新时代中国特色社会主义思想, 人民民主, 价值规律, 党史, 党旗党徽, 党的二十大报告, 党的作风建设, 党的十九大报告, 党的建设, 党的政治建设, 党的组织建设, 全面从严治党, 全面依法治国, 八个明确, 公民道德建设, 公民道德规范, 共同富裕, 十九届中央纪委六次全会, 十九届五中全会, 十九届六中全会, 十四五, 唯物史观, 商品经济的基本概念, 四个全面, 国家安全, 国际合作, 地方时政热点, 坚持新发展理念, 外交, 建设现代化经济体系, 总体国家安全观, 改革开放理论, 数字经济, 文化自信, 新发展格局, 新型国际关系, 新时代, 方法论, 时事政治, 时政热点, 构建人类命运共同体, 毛概, 毛泽东思想的形成和发展, 毛泽东诗词排序, 生态文明建设, 社会公德, 社会治理现代化, 神舟十三号出舱活动, 经济政策, 绿色发展, 职业道德, 遵义会议, 邓小平理论, 重要会议, 重要文件, 重要讲话, 马克思主义哲学, 马克思主义政治经济学

### 经济
世界经济的三大支柱组织, 供求均衡, 促进经济增长, 倾销的类型, 国际贸易, 宏观经济与调控政策, 宏观调控政策分析, 宏观调控的目标, 市场经济理论, 开放经济下的宏观经济学, 微观经济, 新贸易保护主义, 汇率制度, 稳定物价, 经济全球化, 经济增长, 经济学名词, 经济学术语, 货币政策, 贸易摩擦, 资源稀缺性, 资源配置, 通货膨胀, 重要经济组织, 金融知识, 需求和供给理论

### 文化
中国古代文学, 书法, 古代生活, 古代科技, 古代诗歌, 天文历法, 常识, 文史, 经典, 绘画, 诗歌, 诗词

### 地理环境
中国地理疆域和行政区划, 中国的非物质文化遗产, 主要地形及特征, 人文地理, 喀斯特地貌, 四大高原, 地壳和地质构造, 地球自转, 地理常识, 地质灾害, 地震, 天体系统, 旅游地理, 特殊地貌, 省情, 自然资源及其分布, 领海和内海, 黄土高原

### 历史
中国古代历史, 中国当代, 中国文学, 中国科技文化常识, 习近平用典, 人文, 人文历史常识, 历史人文, 历史常识, 建设时期, 文学常识, 科技文化

### 法律
不当得利, 不授予专利权的对象, 专利权, 个人信息保护法, 居民身份证法, 中国公民的概念, 人民法院与地方各级人大, 人身权, 代理, 以危险方法危害公共安全, 依法治国, 侵害英雄烈士名誉, 侵权行为, 侵权责任, 侵犯财产罪, 保险法, 信用信息, 债的发生原因, 党纪党规, 冒名顶替, 减轻或免除侵权责任的事由, 减轻或免除民事责任事由, 刑事诉讼法, 刑事诉讼程序, 刑法分论, 刑法总论, 刑法的基本原则, 刑法的概述, 刑法的适用范围, 刑罚, 动产物权的变动, 劳动与社会保险法, 劳动合同法, 劳动合同的条款, 劳动合同的解除与终止, 单位犯罪, 危害公共安全罪, 商法与经济法, 回避制, 国体, 国家制度, 国家基本经济制度, 国家机关, 国家机构, 国家赔偿, 地方人大常委会, 基本原则, 夫妻财产制度, 妨害社会管理秩序罪, 婚姻, 安全生产相关法, 宣告死亡的保险责任, 宪法修正案, 宪法国家机关, 宪法概述, 宪法的基本内容, 宪法的基本理论, 宪法的特征, 居住权, 所有权, 所有权的一般规定, 所有权的取得, 抵押权, 担保物权, 政府信息公开, 民事法律关系主体之自然人, 民事诉讼法, 民事诉讼法的基本制度, 民事责任, 民族区域自治制度, 民法典, 民法概述, 法定继承, 法治, 法理学非常规考点, 法的正式渊源, 法的渊源, 物权, 物权的变动, 特殊侵权责任, 犯罪主体, 犯罪排除事由, 犯罪构成, 犯罪的构成要件, 犯罪的特征, 用益物权, 监护, 盗窃罪, 知识产权, 紧急避险, 继承, 继父母子女关系, 网络侵权责任, 肖像权, 荣誉罪, 著作权, 行政处罚, 行政处罚的种类, 行政处罚的程序, 行政处罚的设定, 行政复议, 行政复议的申请, 行政复议范围, 行政法与行政诉讼法, 行政法概述, 行政行为概述, 行政行为的分类, 行政许可, 行政许可的听证, 行政许可的实施, 行政诉讼, 行政诉讼的诉讼参加人, 行政赔偿, 辩护, 辩护与代理, 违约责任, 选举制度, 附加刑, 隐私权, 贪污罪, 贪污贿赂罪

### 自然科技
"中国天眼", 中国现当代科技史, 人体的生理现象, 信息技术, 光的传播, 其他高新技术, 力学, 化学常识, 化学知识, 反射, 常见疾病, 微生物, 新材料, 新能源技术, 有机化合物, 水生态, 海洋科技, 激光, 灭火器, 灾害应对, 物理常识, 物理知识, 物质, 环保知识, 生活常识, 生物医学知识, 生物多样性, 生物常识, 生物知识, 石墨, 石油化工, 碳, 科技, 科技其他, 科技发展, 科技常识, 科技理论与成就, 糖尿病, 航空航天, 药水, 遗传物质, 酒精, 金属元素, 铜, 高新科技

## Data Schema Details

### Question Object
| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier |
| `title` | Yes | Short title (shown in list) |
| `fields.错题` | No | Full question stem with options |
| `fields.答案` | No | Answer letter (A/B/C/D) or text |
| `fields.错题解析` | No | Explanation text |
| `fields.知识点` | No | Major knowledge point name (must be one of the fixed KPs above) |
| `fields.Tags` | No | Comma-separated tags |
| `fields.相关链接` | No | Reference URL |

### Title vs Stem Display Rules
- When a question has no `错题` or `题目` field, the `title` is used as the question stem (via `stemOf()` fallback)
- The title is always shown in the header, but truncated: if `title` length > 10, show first 10 chars + "…" (e.g., "不真正连带责任，是指…")
- If `title` length ≤ 10, show the full title
- The `stemOf()` function fallback chain: `错题` → `题目` → `title` → empty

### localStorage Keys
| Key | Purpose |
|-----|---------|
| `exam_mine` | User's custom questions |
| `exam_edited` | User's edits to built-in questions |
| `exam_deleted` | Deleted question IDs |
| `exam_notes` | Personal notes per question |
| `exam_mastered` | Mastered question IDs |
| `exam_usertags` | User-created tags |

## Key Design Constraints

1. **Answer hiding**: Answers (参考答案, 答案分析, 解析) must be in collapsible sections, hidden by default
2. **No answer highlight in preview**: During import preview, don't highlight correct options in green
3. **Knowledge points are fixed**: Only the 12 major categories + their sub-KPs listed above appear in sidebar
4. **Tags are scoped**: Tag selector shows tags from the current category's questions only
5. **No native dialogs**: Use in-app modals instead of `alert()`/`confirm()` (sandbox compatibility)
6. **Sidebar hierarchy**: Category = blue, Knowledge point = yellow (expandable under category)
7. **Knowledge point selector is searchable**: Include a filter input above the KP list
8. **Tag selector is searchable**: Include a filter input, show selected tags by default, hide unselected

## Building from Data Sources

### From CSV
1. Parse CSV rows into question objects
2. Map columns to fields (题目→title, 错题→fields.错题, 答案→fields.答案, etc.)
3. Determine category from a "分类" or "category" column, or by asking the user
4. Assign knowledge points based on a "知识点" column or content keywords

### From PDF
1. Extract text with PDF text extraction
2. Parse question blocks: identify question numbers, options (A. B. C. D.), answers (【答案】), explanations (解析：), knowledge tags (【考点】)
3. Split multi-question documents by question number patterns
4. Map 考点 paths to major knowledge points using the keyword mapping below

### From Plain Text
1. The smart parser should auto-detect:
   - Question stems (lines starting with numbers: "51." or "51、")
   - Options (lines starting with A. B. C. D. or ① ② ③ ④)
   - Answers (lines with "答案：", "【答案】", "选B")
   - Explanations (lines with "解析：", "解析：")
   - Knowledge tags (lines with "【考点】", "考点：")
2. Split multiple questions by question number gaps
3. Auto-complete missing answers/explanations by matching similar questions in the existing bank

### Knowledge Point Mapping Rules
When importing questions with detailed 考点 paths (e.g., "法律 刑法 刑法总论 犯罪的特征"):
- Set `知识点` to the major KP (e.g., "刑法")
- Split the full path into individual tags (e.g., ["法律", "刑法", "刑法总论", "犯罪的特征"])
- Store tags in `Tags` field, comma-separated

#### Mapping Keywords
| Keyword in 考点 path | → Category | → Knowledge Point |
|---------------------|-----------|-------------------|
| 政治, 时政, 党, 中特, 习近平, 马哲, 马政经, 毛概, 道德 | 政治 | (by sub-keyword) |
| 经济, 宏观, 微观, 金融, 贸易, 通货膨胀 | 经济 | (by sub-keyword) |
| 法律, 法, 刑法, 民法, 宪法, 行政法, 劳动 | 法律 | (by sub-keyword) |
| 科技, 科学, 物理, 化学, 生物, 新能源, 信息技术 | 自然科技 | (by sub-keyword) |
| 历史, 古代史, 近现代史, 人文历史 | 历史 | (by sub-keyword) |
| 地理, 地质, 地形, 气候, 省情, 国情 | 地理环境 | (by sub-keyword) |
| 文化, 文学, 诗词, 艺术, 书法 | 文化 | (by sub-keyword) |
| 判断, 定义, 类比, 逻辑, 推理 | 判断推理 | (by sub-keyword) |
| 言语, 词语, 成语, 片段, 填空, 排序 | 言语理解 | (by sub-keyword) |
| 数量, 数学, 数字, 工程, 容斥, 方程 | 数量关系 | (by sub-keyword) |
| 资料, 增长率, 倍数, 速算 | 资料分析 | (by sub-keyword) |
| 图形, 规律, 对称, 平移, 旋转, 立体 | 图形推理 | (by sub-keyword) |

## Step-by-Step Build Process

1. **Gather data**: Collect questions from CSV/JSON/PDF/text
2. **Create db.json**: Normalize all questions into the schema above, assign categories and knowledge points
3. **Get template.html**: Use the provided template
4. **Run build.py**: Injects db.json into template
5. **Verify**: Check syntax with `node -e "new Function(script)"`
6. **Test**: Open in browser, verify all features work

## Customization

### Changing Colors
Edit CSS variables in `:root`:
```css
--brand:#3d5afe;    /* Primary blue */
--accent:#ff8a00;   /* Accent orange */
--ok:#16a34a;       /* Correct green */
--warn:#dc2626;     /* Wrong red */
```

### Adding Images
Questions can reference images via base64 data URIs in the 错题 field:
```html
<img src="data:image/png;base64,..." style="max-width:100%">
```
