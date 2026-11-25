"""生成一页两套语法的对照表，给秦羲子自己改站时翻。"""

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

OUT = r"C:\Workarea\qinxi-site\docs\语法对照.docx"

INK = RGBColor(0x1B, 0x18, 0x14)
SOFT = RGBColor(0x6B, 0x62, 0x58)
ACCENT = RGBColor(0x8E, 0x35, 0x27)


def set_font(run, latin="宋体", east="宋体", size=10.5, bold=False, color=None):
    run.font.name = latin
    run.font.size = Pt(size)
    run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), latin)
    rfonts.set(qn("w:hAnsi"), latin)
    rfonts.set(qn("w:eastAsia"), east)


def shade(cell, hexcolor):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcpr.append(shd)


def polish(table):
    """表头每页重复，行不跨页断。"""

    for row in table.rows:
        trpr = row._tr.get_or_add_trPr()
        trpr.append(OxmlElement("w:cantSplit"))
    hdr_trpr = table.rows[0]._tr.get_or_add_trPr()
    hdr_trpr.append(OxmlElement("w:tblHeader"))


def para(doc, text="", size=10.5, bold=False, color=INK, space_after=6, latin="宋体", align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.38
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    set_font(r, latin=latin, size=size, bold=bold, color=color)
    return p


def heading(doc, text, new_page=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(13)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    if new_page:
        p.paragraph_format.page_break_before = True
    r = p.add_run(text)
    set_font(r, latin="黑体", size=13, bold=True, color=ACCENT)
    return p


def cell_text(cell, text, mono=False, bold=False, size=9.5, color=INK):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(text)
    if mono:
        set_font(r, latin="Consolas", east="宋体", size=size, bold=bold, color=color)
    else:
        set_font(r, latin="宋体", size=size, bold=bold, color=color)


doc = Document()
section = doc.sections[0]
section.page_width = Cm(21)
section.page_height = Cm(29.7)
section.left_margin = Cm(2.2)
section.right_margin = Cm(2.2)
section.top_margin = Cm(2.0)
section.bottom_margin = Cm(2.0)

# 标题区
para(doc, "秦羲子站", size=9.5, color=SOFT, space_after=2)
para(doc, "Markdown 与 Astro 语法对照", size=20, bold=True, space_after=4, latin="黑体")
para(
    doc,
    "左边那列是你要做的事，中间是写 md 时的写法，右边是改 astro 页面时的写法。同一个意思，两套写法。",
    size=10,
    color=SOFT,
    space_after=10,
)

heading(doc, "一、常用语法对照")

rows = [
    ("一级标题", "# 标题", "<h1>标题</h1>"),
    ("二级标题", "## 标题", "<h2>标题</h2>"),
    ("三级标题", "### 标题", "<h3>标题</h3>"),
    ("段落", "空一行就是新段落", "<p>一段话</p>"),
    ("加粗", "**字**", "<strong>字</strong>"),
    ("斜体", "*字*", "<em>字</em>"),
    ("引用", "> 一句话", "<blockquote>一句话</blockquote>"),
    ("无序列表", "- 一条\n- 又一条", "<ul>\n  <li>一条</li>\n  <li>又一条</li>\n</ul>"),
    ("有序列表", "1. 第一条\n2. 第二条", "<ol>\n  <li>第一条</li>\n  <li>第二条</li>\n</ol>"),
    ("链接", "[名字](https://网址)", '<a href="https://网址">名字</a>'),
    ("图片", "![说明](/images/x.jpg)", '<img src="/images/x.jpg" alt="说明" />'),
    ("分隔线", "***", "<hr />"),
    ("行内代码", "`代码`", "<code>代码</code>"),
    ("代码块", "用三个反引号围起来", "<pre><code>代码</code></pre>"),
    ("强制换行不断段", "行末敲两个空格", "<br />"),
    ("注释", "<!-- 注释 -->", "<!-- 注释 -->"),
]

table = doc.add_table(rows=1, cols=3)
table.style = "Table Grid"
table.alignment = WD_TABLE_ALIGNMENT.CENTER
widths = [Cm(3.6), Cm(5.4), Cm(7.6)]

hdr = table.rows[0].cells
for i, text in enumerate(["要做的事", "Markdown 里", "Astro 里"]):
    cell_text(hdr[i], text, bold=True, size=9.5, color=RGBColor(0xFF, 0xFF, 0xFF))
    shade(hdr[i], "8E3527")

for idx, (what, md, astro) in enumerate(rows):
    cells = table.add_row().cells
    cell_text(cells[0], what, size=9.5, bold=True)
    cell_text(cells[1], md, mono=True)
    cell_text(cells[2], astro, mono=True)
    if idx % 2 == 1:
        for c in cells:
            shade(c, "F6F1E7")

for row in table.rows:
    for i, w in enumerate(widths):
        row.cells[i].width = w
polish(table)

heading(doc, "二、Astro 独有的几样东西", new_page=True)

para(doc, "一个 .astro 文件分成两半。最上面夹在三横线里的那一段是脚本区，写 import 和取数据。往下就是 HTML。", size=10, space_after=6)

astro_bits = [
    ("文件顶部\n---\nimport Base from \"../layouts/Base.astro\";\n---", "脚本区，夹在三横线中间，装 import 和变量。三横线不能删。"),
    ("{变量名}", "插值。花括号里可以是变量，也可以是算式，还会当场算出来。"),
    ("{条件 && <p>话</p>}", "条件渲染，前面成立才显示后面那块。"),
    ("{列表.map((x) => <li>{x}</li>)}", "循环，把数组里每一条变成一行。"),
    ("<Base title=\"关于\">…</Base>", "组件。首字母大写的是别的文件里定义好的东西，不是普通标签。"),
    ("<style> p { color: red } </style>", "写在这个文件里的样式，只作用在这个文件。"),
    ("<script> console.log(1) </script>", "发给浏览器的 JavaScript，跟构建无关。"),
]

table2 = doc.add_table(rows=1, cols=2)
table2.style = "Table Grid"
hdr2 = table2.rows[0].cells
for i, text in enumerate(["写法", "意思"]):
    cell_text(hdr2[i], text, bold=True, size=9.5, color=RGBColor(0xFF, 0xFF, 0xFF))
    shade(hdr2[i], "8E3527")

for idx, (code, mean) in enumerate(astro_bits):
    cells = table2.add_row().cells
    cell_text(cells[0], code, mono=True, size=9)
    cell_text(cells[1], mean, size=9.5)
    if idx % 2 == 1:
        for c in cells:
            shade(c, "F6F1E7")

for row in table2.rows:
    row.cells[0].width = Cm(7.2)
    row.cells[1].width = Cm(9.4)
polish(table2)

heading(doc, "三、写文章时开头那几行")

para(doc, "每篇 md 开头都有一小段配置，夹在三横线中间，告诉网站这篇文章叫什么、算哪一类。字段就这么几个。", size=10, space_after=6)

fields = [
    ("title", "必填", "标题。列表和网页标题都取这个。"),
    ("kind", "必填", "fiction 作品，longform 长文，essay 随笔。决定它进哪个栏目。"),
    ("slug", "选填", "网址里那一段。不写就按文件名。"),
    ("date", "选填", "写成 2026-11-20 这样。列表里显示的日子，也决定排序。"),
    ("category", "选填", "分类小字，比如 短篇、考据、日记。"),
    ("summary", "选填", "列表里显示的一句话摘要。"),
    ("order", "选填", "数字，越小越靠前。不写就按日期排。"),
    ("draft", "选填", "写 true 就不显示。写废了又不想删的时候用。"),
]

table3 = doc.add_table(rows=1, cols=3)
table3.style = "Table Grid"
hdr3 = table3.rows[0].cells
for i, text in enumerate(["字段", "填不填", "管什么"]):
    cell_text(hdr3[i], text, bold=True, size=9.5, color=RGBColor(0xFF, 0xFF, 0xFF))
    shade(hdr3[i], "8E3527")

for idx, (name, req, mean) in enumerate(fields):
    cells = table3.add_row().cells
    cell_text(cells[0], name, mono=True)
    cell_text(cells[1], req, size=9.5)
    cell_text(cells[2], mean, size=9.5)
    if idx % 2 == 1:
        for c in cells:
            shade(c, "F6F1E7")

for row in table3.rows:
    row.cells[0].width = Cm(3.2)
    row.cells[1].width = Cm(2.2)
    row.cells[2].width = Cm(11.2)
polish(table3)

heading(doc, "四、容易摔的坑")

pits = [
    "astro 里的标签必须成对，<p> 开了就得有 </p>。md 里没有这回事，段落空一行就断。",
    "md 文件最开头那组三横线是配置，不是分隔线。想画分隔线用 ***，别用 ---。",
    "花括号 {} 是代码的地盘。页面里想打出花括号，得写成转义，不然它当成算式去算。",
    "改 astro 页面之前先把文件复制一份，改坏了直接换回来，比看报错快。",
    "冒号后面跟空格还是跟中文，都不影响。但引号要成对，中英文引号别混着用。",
]
for i, t in enumerate(pits, 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.first_line_indent = Cm(-0.6)
    r = p.add_run(f"{i}. ")
    set_font(r, latin="Consolas", size=10, bold=True, color=ACCENT)
    r2 = p.add_run(t)
    set_font(r2, size=10)

doc.save(OUT)
print("saved", OUT)

# 校验
check = Document(OUT)
print("段落数", len(check.paragraphs))
print("表格数", len(check.tables))
print("第一张表行数", len(check.tables[0].rows))
print("标题", check.paragraphs[1].text)
