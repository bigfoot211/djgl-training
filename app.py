# -*- coding: utf-8 -*-
"""
《地籍管理》课程学习与实训系统 · Web版 V2.5
湖南农业大学 · 土地资源管理专业
中英双语 · 全部功能与桌面版一致
"""
import streamlit as st
import json, os, random, math, datetime
import pandas as pd

st.set_page_config(
    page_title="地籍管理实训系统 / Cadastral Training System",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")

# ============================================================
# 右上角固定漂浮吉祥物
# ============================================================
if 'mascot_msg' not in st.session_state:
    st.session_state.mascot_msg = random.choice(MASCOT_QUOTES)

# 随机切换台词
if random.random() < 0.05:
    st.session_state.mascot_msg = random.choice(MASCOT_QUOTES)

_mascot_css = """
<style>
.mascot-float {
    position: fixed;
    top: 80px;
    right: 20px;
    z-index: 9999;
    animation: float 3s ease-in-out infinite;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
.mascot-avatar {
    font-size: 48px;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.2));
}
.mascot-bubble {
    background: #fff;
    border: 2px solid #ffd700;
    border-radius: 12px;
    padding: 8px 12px;
    max-width: 250px;
    font-size: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    position: relative;
    margin-top: 8px;
}
.mascot-bubble::before {
    content: '';
    position: absolute;
    left: -8px;
    top: 15px;
    border-width: 8px 8px 8px 0;
    border-style: solid;
    border-color: transparent #ffd700 transparent transparent;
}
</style>
"""
_en, _zh = st.session_state.mascot_msg
_bubble_text = f"👨‍🏫 {_zh}<br><small><i>{_en}</i></small>"
st.markdown(_mascot_css + f"""
<div class="mascot-float">
    <div class="mascot-bubble">{_bubble_text}</div>
    <div class="mascot-avatar">👨‍🏫</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 语言切换
# ============================================================
if 'lang' not in st.session_state:
    st.session_state.lang = "zh"

def t(zh, en):
    """双语显示"""
    return f"{zh} / {en}" if st.session_state.lang == "zh" else en

# ============================================================
# 中文数据
# ============================================================
CLASS_PRACTICE = [
    ("水田", "耕地", "01"), ("水浇地", "耕地", "01"), ("旱地", "耕地", "01"),
    ("果园", "园地", "02"), ("茶园", "园地", "02"),
    ("乔木林地", "林地", "03"), ("竹林地", "林地", "03"),
    ("天然牧草地", "草地", "04"), ("其他草地", "草地", "04"),
    ("零售商业用地", "商服用地", "05"), ("餐饮用地", "商服用地", "05"), ("旅馆用地", "商服用地", "05"),
    ("工业用地", "工矿仓储用地", "06"), ("仓储用地", "工矿仓储用地", "06"), ("采矿用地", "工矿仓储用地", "06"),
    ("城镇住宅用地", "住宅用地", "07"), ("农村宅基地", "住宅用地", "07"),
    ("教育用地", "公共管理与公共服务用地", "08"), ("医疗卫生用地", "公共管理与公共服务用地", "08"),
    ("公园与绿地", "公共管理与公共服务用地", "08"),
    ("军事设施用地", "特殊用地", "09"), ("宗教用地", "特殊用地", "09"), ("殡葬用地", "特殊用地", "09"),
    ("铁路用地", "交通运输用地", "10"), ("公路用地", "交通运输用地", "10"), ("农村道路", "交通运输用地", "10"),
    ("河流水面", "水域及水利设施用地", "11"), ("水库水面", "水域及水利设施用地", "11"),
    ("沟渠", "水域及水利设施用地", "11"), ("坑塘水面", "水域及水利设施用地", "11"),
    ("空闲地", "其他土地", "12"), ("设施农用地", "其他土地", "12"),
    ("沙地", "其他土地", "12"), ("裸土地", "其他土地", "12"), ("田坎", "其他土地", "12"),
]
CLASS_IMAGES = [f"landuse/{i:02d}.png" for i in range(1, 36)]
FIRST_CLASSES = ["耕地", "园地", "林地", "草地", "商服用地", "工矿仓储用地",
                 "住宅用地", "公共管理与公共服务用地", "特殊用地", "交通运输用地",
                 "水域及水利设施用地", "其他土地"]
FIRST_CLASSES_EN = ["Cultivated Land", "Garden Land", "Forest Land", "Grassland",
                    "Commercial & Service", "Industrial, Mining & Warehousing",
                    "Residential Land", "Public Admin. & Service", "Special Land",
                    "Transportation Land", "Water & Conservancy", "Other Land"]

OWNERSHIP_BANK = [
    ("城市市区的土地", "国有", "《土地管理法》规定：城市市区的土地属于国家所有。"),
    ("农村宅基地", "集体", "宅基地所有权归农民集体，农户只享有宅基地使用权。"),
    ("自留地、自留山", "集体", "农村和城市郊区的土地，除法律规定属于国家所有的以外，属于农民集体所有。"),
    ("经国家依法征收后的原农村土地", "国有", "征收是集体土地转为国有土地的法定途径，征收后土地所有权归国家。"),
    ("国有农场的土地", "国有", "国有农场土地属全民所有（国家所有），由国有农场经营使用。"),
    ("村办企业占用的原集体土地（未经征收）", "集体", "未经依法征收的原集体土地，其所有权仍属农民集体。"),
    ("城市公园绿地", "国有", "城市市区范围内的土地属于国家所有，公园绿地亦然。"),
    ("村民小组所有的山林", "集体", "村、组范围内的集体土地归该农民集体所有。"),
    ("国家划拨给部队使用的土地", "国有", "划拨只是国有土地使用权的取得方式，土地所有权仍归国家。"),
    ("城镇居民购买的出让商品住宅用地", "国有", "出让土地上购房者取得的是国有土地使用权，所有权仍属国家。"),
    ("村内空闲宅基地", "集体", "空闲宅基地的所有权仍属农民集体。"),
    ("城镇国有土地上开发建设的住宅小区", "国有", "住宅小区占地一般为出让的国有土地，所有权归国家。"),
]
OWNERSHIP_BANK_EN = [
    ("Land in urban built-up areas", "Under the Land Administration Law, land in urban built-up areas is owned by the State."),
    ("Rural homestead", "Homestead ownership belongs to the farmer collective; farmers only hold the homestead use right."),
    ("Private plots and private hills", "Land in rural and suburban areas, except as provided by law as State-owned, belongs to the farmer collectives."),
    ("Former rural land lawfully expropriated by the State", "Expropriation is the statutory route for converting collective land into State ownership."),
    ("Land of State-owned farms", "State-owned farm land is owned by the whole people (the State)."),
    ("Former collective land occupied by village-run enterprises (not expropriated)", "Without lawful expropriation, ownership remains with the farmer collective."),
    ("Urban park green space", "Land within urban built-up areas is State-owned, including parks and green space."),
    ("Mountain forest owned by a villagers' group", "Collective land within a village/group belongs to that farmer collective."),
    ("Land allocated by the State for military units", "Allocation only confers the use right; ownership remains with the State."),
    ("Granted commodity-housing land purchased by urban residents", "Buyers acquire the State-owned land use right; ownership remains with the State."),
    ("Idle homestead within a village", "Ownership of an idle homestead still belongs to the farmer collective."),
    ("Residential communities built on State-owned urban land", "Such communities generally sit on granted State-owned land; ownership belongs to the State."),
]

SURVEY_STEPS = [
    ("准备工作", "成立调查机构、收集资料、编写技术设计书"),
    ("权属调查", "划分宗地、调查权属状况、组织指界、设置界标、勘丈界址"),
    ("地籍控制测量", "布设平面控制网（GPS、导线等），为细部测量提供控制基础"),
    ("界址点测量", "用解析法（全站仪、RTK 等）测定界址点坐标"),
    ("地籍图测绘", "测绘分幅地籍图、编绘宗地图"),
    ("面积量算", "采用解析法或图解法量算宗地面积并汇总统计"),
    ("成果检查验收", "自检、互检、专检与验收"),
    ("成果整理归档", "编制地籍调查表、宗地图、地籍图、面积统计表并归档"),
]
SURVEY_STEPS_EN = [
    ("Preparatory Work", "Establish survey organs, collect materials and prepare technical design"),
    ("Ownership Survey", "Delimit parcels, investigate ownership, organize boundary designation"),
    ("Cadastral Control Survey", "Lay horizontal control networks (GPS, traverses, etc.)"),
    ("Boundary Point Survey", "Determine boundary point coordinates analytically (total station, RTK)"),
    ("Cadastral Mapping", "Map sheet cadastral maps and compile parcel maps"),
    ("Area Calculation", "Compute parcel areas by analytic or graphical methods"),
    ("Checking & Acceptance", "Self-check, mutual check, special check and acceptance"),
    ("Archiving of Outputs", "Prepare survey forms, parcel maps, cadastral maps and area tables"),
]

MAP_QUESTIONS = [
    ("图中标注的 J1、J2、J3、J4、J5 是什么要素？",
     ["房屋角点", "界址点", "水准点", "道路交叉点"], 1,
     "界址点是宗地权属界线的转折点，是宗地图的核心要素。"),
    ("相邻界址点之间的连线表示什么？",
     ["地类界线", "行政界线", "界址线（宗地权属界线）", "道路中心线"], 2,
     "界址线即宗地权属界线，是确定土地权属范围的边界。"),
    ("宗地内的“水田（0101）”注记属于什么注记？",
     ["权利人注记", "地类注记", "面积注记", "高程注记"], 1,
     "地类注记标明宗地的土地利用现状类型及分类代码。"),
    ("“权利人：张某某”说明什么？",
     ["该宗地的权属主体", "测绘人员", "村干部", "相邻宗地权利人"], 0,
     "权利人是宗地权属的主体，登记发证时须与登记簿一致。"),
    ("“宗地面积：1250.00 ㎡”属于什么注记？",
     ["宗地面积注记", "房屋建筑面积", "相邻宗地面积", "图幅面积"], 0,
     "宗地面积是经面积量算后注记于宗地图上的权属面积。"),
    ("图中右上角红色箭头表示什么？",
     ["风向", "指北针（图幅方位）", "比例尺方向", "道路方向"], 1,
     "指北针用于确定图幅方位，是地图的方向依据。"),
    ("“东至：李某某承包田”等四至注记说明什么？",
     ["宗地四邻的权属状况", "道路名称", "河流走向", "地形地貌"], 0,
     "四至注记说明宗地四邻的权属主体，是界址确认的重要依据。"),
    ("宗地图的主要作用是什么？",
     ["旅游地图", "地价评估图", "土地登记与权属管理的附图", "城市规划图"], 2,
     "宗地图是土地登记、权属管理的附图，反映宗地界址、权属与利用状况。"),
    ("“比例尺 1:1000”表示图上 1cm 代表实地多少米？",
     ["1m", "10m", "100m", "1000m"], 1,
     "1:1000 即图上 1 个单位代表实地 1000 个单位，1cm 代表 10m。"),
    ("从界址点坐标看，该宗地南北方向最长约多少米？",
     ["约 10m", "约 20m", "约 30m", "约 50m"], 2,
     "界址点 Y 坐标从 0 到 30m，故南北向最大长度约 30m。"),
    ("宗地图的基本内容一般包括哪些？",
     ["仅面积", "仅界址点坐标", "界址点与界址线、权利人、地类、面积、四至等", "仅图名"], 2,
     "宗地图应反映界址、权属、利用三大类信息。"),
    ("界址点坐标表在宗地图上一般位于何处？",
     ["图廓外或图面空白处", "宗地内部正中央", "必须压盖宗地", "无要求"], 0,
     "坐标表一般置于图廓外或图面空白处，不得压盖宗地图形。"),
]
MAP_QUESTIONS_EN = [
    ("What are the J1, J2, J3, J4, J5 marked in the map?",
     ["Building corners", "Boundary points", "Benchmarks", "Road intersections"],
     "Boundary points are the turning points of the parcel ownership boundary."),
    ("What does the line between adjacent boundary points represent?",
     ["Land-class boundary", "Administrative boundary", "Boundary line (ownership line)", "Road centerline"],
     "The boundary line is the parcel ownership boundary."),
    ("What kind of annotation is 'Paddy (0101)' inside the parcel?",
     ["Right-holder annotation", "Land-class annotation", "Area annotation", "Elevation annotation"],
     "Land-class annotations mark the current land use type and its classification code."),
    ("What does 'Right holder: Zhang XX' indicate?",
     ["The ownership subject of this parcel", "The surveyor", "The village cadre", "The neighboring right holder"],
     "The right holder is the subject of the parcel right."),
    ("What kind of annotation is 'Parcel area: 1250.00 m²'?",
     ["Parcel area annotation", "Building floor area", "Neighboring parcel area", "Sheet area"],
     "The parcel area is annotated after area calculation."),
    ("What does the red arrow at the upper right indicate?",
     ["Wind direction", "North arrow (map orientation)", "Scale direction", "Road direction"],
     "The north arrow fixes the orientation of the map sheet."),
    ("What do boundary annotations such as 'East to: Zhang's field' indicate?",
     ["The ownership status of the four adjacent sides", "Road names", "River course", "Terrain"],
     "Boundary annotations state the ownership subjects of the four sides."),
    ("What is the main function of a parcel map?",
     ["Tourist map", "Land valuation map", "Annex for land registration", "Urban planning map"],
     "The parcel map is the annex for land registration and ownership administration."),
    ("At scale 1:1000, how many meters does 1 cm on the map represent?",
     ["1 m", "10 m", "100 m", "1000 m"],
     "1:1000 means 1 unit on map = 1000 units on ground, so 1 cm = 10 m."),
    ("The longest north-south extent of this parcel is about?",
     ["About 10 m", "About 20 m", "About 30 m", "About 50 m"],
     "Y coordinates range from 0 to 30 m, so north-south extent is about 30 m."),
    ("The basic contents of a parcel map include?",
     ["Area only", "Boundary coordinates only", "Boundary points/lines, right holder, class, area, four boundaries", "Map title only"],
     "A parcel map reflects boundary, ownership and use information."),
    ("Where is the boundary point coordinate table usually placed?",
     ["Outside the map frame or in blank space", "At the exact center", "It must overlay the parcel", "No requirement"],
     "The coordinate table is placed outside the map frame or in blank space."),
]

AREA_PARCELS = [
    {"name": "宗地 A（矩形）", "pts": [(0, 0), (50, 0), (50, 30), (0, 30)],
     "hint": "矩形宗地：长 50m、宽 30m，可直接用 长×宽 计算。"},
    {"name": "宗地 B（L 形）", "pts": [(0, 0), (60, 0), (60, 40), (30, 40), (30, 20), (0, 20)],
     "hint": "L 形宗地：可分解为两个矩形相加，或用坐标法整体计算。"},
    {"name": "宗地 C（五边形）", "pts": [(0, 0), (40, 0), (52, 26), (20, 40), (0, 26)],
     "hint": "五边形宗地：建议用坐标法（鞋带公式）计算。"},
    {"name": "宗地 D（三角形）", "pts": [(0, 0), (80, 0), (40, 50)],
     "hint": "三角形宗地：底 80m、高 50m，面积 = 底×高÷2。"},
    {"name": "宗地 E（梯形）", "pts": [(0, 0), (70, 0), (50, 40), (0, 40)],
     "hint": "梯形宗地：上底 50m、下底 70m、高 40m。"},
    {"name": "宗地 F（六边形）", "pts": [(10, 0), (60, 0), (70, 30), (40, 55), (5, 40), (0, 15)],
     "hint": "不规则六边形宗地：建议用坐标法计算。"},
]
AREA_PARCELS_EN = [
    ("Parcel A (Rectangle)", "Rectangular: 50m long, 30m wide; area = length × width."),
    ("Parcel B (L-shape)", "L-shaped: split into two rectangles, or use coordinate method."),
    ("Parcel C (Pentagon)", "Pentagonal: use the coordinate (shoelace) method."),
    ("Parcel D (Triangle)", "Triangle: base 80m, height 50m; area = base × height / 2."),
    ("Parcel E (Trapezoid)", "Trapezoid: top 50m, bottom 70m, height 40m."),
    ("Parcel F (Hexagon)", "Irregular hexagon: use the coordinate method."),
]

QUIZ_BANK = [
    ("地籍是记载土地的哪类基本状况的图簿册？",
     ["仅面积大小", "位置、界址、数量、质量、权属和用途", "仅所有权", "仅用途"], 1,
     "地籍是土地的“户口簿”，全面记载位置、界址、数量、质量、权属与用途。"),
    ("地籍管理的基本工作单元是什么？",
     ["地块", "宗地", "图斑", "行政村"], 1,
     "宗地是地籍管理的基本单元。"),
    ("《土地利用现状分类》一级类共有多少类？",
     ["8 类", "10 类", "12 类", "15 类"], 2,
     "2017 版标准一级类 12 个、二级类 73 个。"),
    ("下列地类中属于建设用地的是？",
     ["水田", "果园", "采矿用地", "沼泽草地"], 2,
     "采矿用地属工矿仓储用地（06），为建设用地。"),
    ("下列地类中属于农用地的是？",
     ["铁路用地", "殡葬用地", "水浇地", "空闲地"], 2,
     "水浇地属耕地（01），为农用地。"),
    ("农村宅基地的所有权属于谁？",
     ["农户个人", "农民集体", "国家", "村委会"], 1,
     "宅基地所有权归农民集体。"),
    ("城市市区的土地属于谁所有？",
     ["集体所有", "国家所有", "国家与集体共有", "个人所有"], 1,
     "城市市区的土地属于国家所有。"),
    ("下列属于国有土地使用权有偿取得方式的是？",
     ["划拨", "出让", "行政命令", "无偿占用"], 1,
     "出让是有偿使用的主要方式。"),
    ("土地承包经营权属于哪类权利？",
     ["土地所有权", "担保物权", "用益物权", "债权"], 2,
     "土地承包经营权是用益物权。"),
    ("地役权属于土地权利中的哪一类？",
     ["土地所有权", "土地使用权", "土地他项权利", "行政管理权"], 2,
     "地役权、抵押权、租赁权等属于土地他项权利。"),
    ("地籍调查按时间和任务性质分为？",
     ["初始地籍调查与日常（变更）地籍调查", "城市与农村调查", "大比例尺与小比例尺", "航空与地面调查"], 0,
     "初始地籍调查是首次全面调查，日常地籍调查是变更调查。"),
    ("权属调查的核心内容是什么？",
     ["面积计算", "界址调查", "地类调查", "地貌测绘"], 1,
     "权属调查围绕宗地权属状况进行，界址调查是核心。"),
    ("为确立新的土地权利而进行的登记是？",
     ["注销登记", "初始（总）登记", "更正登记", "查封登记"], 1,
     "初始（总）登记是首次确立土地权利的登记。"),
    ("土地权利发生转让、更名等变化时进行的登记是？",
     ["变更登记", "初始登记", "注销登记", "预告登记"], 0,
     "变更登记针对权利主体、内容等的变化。"),
    ("土地权利因征收、灭失等原因消灭时进行的登记是？",
     ["变更登记", "注销登记", "初始登记", "抵押登记"], 1,
     "权利消灭时办理注销登记。"),
    ("我国不动产统一登记后统一颁发的权属证书是？",
     ["土地使用证", "不动产权证书", "房产证", "他项权证"], 1,
     "2016 年起全面实施不动产统一登记。"),
    ("城镇地籍图通常采用的比例尺为？",
     ["1:10000", "1:50000", "1:500 或 1:1000", "1:200000"], 2,
     "城镇地籍图比例尺一般为 1:500 或 1:1000。"),
    ("农村地籍调查中常用的比例尺为？",
     ["1:500", "1:5000 或 1:10000", "1:50", "1:1"], 1,
     "农村地籍图一般采用 1:5000 或 1:10000。"),
    ("面积量算的解析法（坐标法）依据什么计算？",
     ["界址点坐标", "图上量距", "目估", "行政界线"], 0,
     "解析法直接利用界址点坐标计算面积，精度最高。"),
    ("1 公顷等于多少平方米？",
     ["1000", "666.67", "10000", "100"], 2,
     "1 公顷 = 10000 ㎡ = 15 亩。"),
    ("1 亩约等于多少平方米？",
     ["100", "666.67", "1000", "1500"], 1,
     "1 亩 ≈ 666.67 ㎡。"),
    ("宗地图的主要内容不包括？",
     ["宗地界址点与界址线", "宗地权利人、地类与面积", "相邻宗地关系", "全国人口统计"], 3,
     "宗地图反映宗地界址、权属与利用状况。"),
    ("界址点测量的常用方法是？",
     ["全站仪极坐标法、GPS-RTK 等", "目测法", "步量法", "地图缩放"], 0,
     "界址点测量用解析法，常用全站仪、RTK。"),
    ("第三次全国国土调查主要查清的是？",
     ["土地利用现状分类与面积", "房屋价格", "人口分布", "气象资料"], 0,
     "三调的核心是查清土地利用现状、地类与面积。"),
    ("下列哪种情形需要办理注销登记？",
     ["房屋加层", "土地被依法征收、权利消灭", "权利人改名", "面积更正"], 1,
     "土地权利消灭时办理注销登记。"),
    ("更正登记适用的情形是？",
     ["登记簿记载与事实不符", "权利正常转让", "新设抵押", "初始登记"], 0,
     "更正登记用于纠正登记簿中的错误记载。"),
    ("我国不动产登记的效力原则是？",
     ["登记生效主义", "合同签订即生效", "交付占有即生效", "口头约定即生效"], 0,
     "不动产物权变动以登记为生效要件。"),
    ("出让国有土地使用权时，工业用地最高年限为？",
     ["40 年", "50 年", "70 年", "30 年"], 1,
     "居住70年、工业50年、商业旅游娱乐40年。"),
    ("城镇住宅用地出让的最高年限为？",
     ["40 年", "50 年", "70 年", "无限制"], 2,
     "居住用地出让最高年限 70 年。"),
    ("记录宗地权属调查结果的文件是？",
     ["地籍调查表", "土地统计台账", "指界通知书", "测量手簿"], 0,
     "地籍调查表记录宗地权属状况、界址调查等成果。"),
    ("“指界”指的是？",
     ["相邻宗地权利人到现场共同认定界址线的行为", "指认道路", "指定土地用途", "登记界桩"], 0,
     "指界由相邻宗地权利人现场共同指认界址位置并签字确认。"),
    ("国有土地与集体土地之间的界线称为？",
     ["行政界线", "权属界线", "地类界线", "道路红线"], 1,
     "不同权属主体之间的界线为权属界线。"),
    ("下列哪项属于初始地籍调查的成果？",
     ["地籍调查表、地籍图、宗地图、面积汇总表", "不动产权证书", "征地补偿协议", "地价评估报告"], 0,
     "初始地籍调查成果包括调查表、地籍图、宗地图与面积汇总表。"),
]
QUIZ_BANK_EN = [
    ("What basic conditions of land does the cadastre record?",
     ["Area only", "Location, boundary, quantity, quality, ownership and use", "Ownership only", "Use only"],
     "The cadastre is the 'household register' of land."),
    ("What is the basic working unit of cadastral management?",
     ["Land block", "Parcel", "Map patch", "Administrative village"],
     "The parcel is the basic unit of cadastral management."),
    ("How many first-level categories does Land Use Classification contain?",
     ["8", "10", "12", "15"],
     "The 2017 standard has 12 first-level and 73 second-level categories."),
    ("Which land type is construction land?",
     ["Paddy field", "Orchard", "Mining land", "Marsh grassland"],
     "Mining land belongs to Industrial, Mining & Warehousing Land (06)."),
    ("Which land type is agricultural land?",
     ["Railway land", "Funeral land", "Irrigated land", "Idle land"],
     "Irrigated land belongs to Cultivated Land (01)."),
    ("Who owns rural homesteads?",
     ["The individual farmer", "The farmer collective", "The State", "The village committee"],
     "Homestead ownership belongs to the farmer collective."),
    ("Who owns land in urban built-up areas?",
     ["The collective", "The State", "Jointly", "Individuals"],
     "Land in urban built-up areas is owned by the State."),
    ("Which is a paid acquisition method for State-owned land use right?",
     ["Allocation", "Grant", "Administrative order", "Free occupation"],
     "Grant is the main paid method."),
    ("What kind of right is the land contract and management right?",
     ["Land ownership", "Security right", "Usufruct", "Creditor's right"],
     "The land contract and management right is a usufruct."),
    ("Which category does an easement belong to?",
     ["Land ownership", "Land use right", "Other rights in land", "Administrative power"],
     "Easements, mortgages and leaseholds belong to other rights in land."),
    ("Cadastral surveys are classified into?",
     ["Initial and routine (mutative) survey", "Urban and rural", "Large and small scale", "Aerial and ground"],
     "Initial survey is the first comprehensive survey; routine survey is for changes."),
    ("What is the core of ownership survey?",
     ["Area calculation", "Boundary survey", "Land-class survey", "Mapping"],
     "Boundary survey (designation, marking, measurement) is the core."),
    ("Which registration establishes a new land right?",
     ["Cancellation", "Initial (general) registration", "Correction", "Seizure"],
     "Initial registration first establishes a land right."),
    ("Which registration applies when a right is transferred or renamed?",
     ["Alteration registration", "Initial registration", "Cancellation", "Advance notice"],
     "Alteration registration applies to changes in subject or content."),
    ("Which registration applies when a right is extinguished?",
     ["Alteration", "Cancellation registration", "Initial", "Mortgage"],
     "Cancellation registration is handled when a right is extinguished."),
    ("What certificate is uniformly issued after unified real estate registration?",
     ["Land use certificate", "Certificate of Real Property Rights", "House certificate", "Other-rights certificate"],
     "Since 2016, the Certificate of Real Property Rights is issued uniformly."),
    ("What is the usual scale of urban cadastral maps?",
     ["1:10000", "1:50000", "1:500 or 1:1000", "1:200000"],
     "Urban cadastral maps are generally at 1:500 or 1:1000."),
    ("What is the usual scale in rural cadastral surveys?",
     ["1:500", "1:5000 or 1:10000", "1:50", "1:1"],
     "Rural cadastral maps generally use 1:5000 or 1:10000."),
    ("What does the analytic (coordinate) method rely on?",
     ["Boundary point coordinates", "Distances measured on map", "Visual estimation", "Administrative boundaries"],
     "The analytic method uses boundary point coordinates directly."),
    ("How many square meters is one hectare?",
     ["1000", "666.67", "10000", "100"],
     "1 hectare = 10000 m² = 15 mu."),
    ("One mu is approximately how many square meters?",
     ["100", "666.67", "1000", "1500"],
     "1 mu ≈ 666.67 m²."),
    ("Which is NOT included in parcel map contents?",
     ["Boundary points and lines", "Right holder, class and area", "Neighboring parcels", "National population statistics"],
     "A parcel map does not contain population statistics."),
    ("Common methods for boundary point survey?",
     ["Total station, GPS-RTK, etc.", "Visual estimation", "Pacing", "Map zooming"],
     "Boundary points are surveyed analytically with total stations and RTK."),
    ("What does the Third National Land Survey mainly ascertain?",
     ["Land use classification and area", "House prices", "Population distribution", "Meteorological data"],
     "The Third Survey focuses on current land use, classes and areas."),
    ("Which situation requires cancellation registration?",
     ["Adding a storey", "Land expropriated and right extinguished", "Renaming", "Area correction"],
     "Cancellation registration is handled when a right is extinguished."),
    ("Correction registration applies to?",
     ["Register does not match facts", "Normal transfer", "New mortgage", "Initial registration"],
     "Correction registration corrects errors in the register."),
    ("What is the effect principle of real estate registration in China?",
     ["Registration-effectiveness", "Effective upon signing", "Effective upon delivery", "Effective upon oral agreement"],
     "Changes in real rights take effect upon registration."),
    ("Maximum term for granted industrial land?",
     ["40 years", "50 years", "70 years", "30 years"],
     "Residential 70, industrial 50, commercial/tourism 40 years."),
    ("Maximum term for granted residential land?",
     ["40 years", "50 years", "70 years", "Unlimited"],
     "Maximum term for residential land is 70 years."),
    ("Which document records ownership survey results?",
     ["Cadastral survey form", "Land statistics ledger", "Boundary notice", "Field book"],
     "The cadastral survey form records ownership and boundary survey results."),
    ("What is 'boundary designation' (指界)?",
     ["Neighboring right holders jointly designating the boundary on site", "Pointing out roads", "Assigning use", "Registering stakes"],
     "Boundary designation is jointly identifying the boundary on site and signing."),
    ("The boundary between State-owned and collective land is called?",
     ["Administrative boundary", "Ownership boundary", "Land-class boundary", "Road red line"],
     "The boundary between different ownership subjects is the ownership boundary."),
    ("Which is an output of initial cadastral survey?",
     ["Survey forms, cadastral maps, parcel maps, area tables", "Real property certificate", "Expropriation agreement", "Valuation report"],
     "Outputs include survey forms, cadastral maps, parcel maps and area tables."),
]

KNOWLEDGE = [
    {"title": "一、地籍与地籍管理", "img": "img_cadastre.png",
     "text": "1. 地籍：全面、连续记载土地的位置、界址、数量、质量、权属和用途等基本状况的图簿册，是土地的“户口簿”。\n"
             "2. 地籍的特点：空间性、法律性、精确性、现势性（动态性）、连续性。\n"
             "3. 地籍管理：国家为取得地籍资料而进行的调查、登记、统计、档案管理等工作的总称。\n"
             "4. 主要任务：维护土地公有制，保护土地权利人的合法权益。\n"
             "5. 管理主线：地籍调查 → 土地登记 → 土地统计 → 地籍档案。",
     "think": "为什么说地籍是土地的“户口簿”？",
     "answer": "地籍全面记载土地的位置、界址、数量、质量、权属和用途，如同户口簿记载人口信息，是每块地的“身份档案”。"},
    {"title": "二、土地利用现状分类", "img": "img_tree.png",
     "text": "1. 国家标准《土地利用现状分类》（GB/T 21010—2017）：一级类 12 个、二级类 73 个。\n"
             "2. 按《土地管理法》土地分为三大类：农用地、建设用地、未利用地。\n"
             "3. 记忆线索：\n"
             "   01耕地 | 02园地 | 03林地 | 04草地 —— 农用地\n"
             "   05商服 | 06工矿仓储 | 07住宅 | 08公服 | 09特殊 | 10交通 —— 建设用地\n"
             "   11水域及水利 | 12其他土地",
     "think": "为什么“设施农用地”划入“其他土地”？",
     "answer": "设施农用地直接服务于农业生产，但利用方式与耕地、园地等不同，难以并入某一具体农用地二级类，故单列于“其他土地”。"},
    {"title": "三、土地权属", "img": "img_rights.png",
     "text": "1. 土地所有权：国家所有与集体所有。\n"
             "2. 土地使用权：\n"
             "   国有土地使用权：出让、划拨、租赁等；\n"
             "   集体土地使用权：土地承包经营权、宅基地使用权、集体建设用地使用权。\n"
             "3. 土地他项权利：抵押权、地役权、租赁权等。\n"
             "4. 权属确认原则：主体合法、界址清楚、面积准确。",
     "think": "宅基地使用权为什么不能自由买卖给城镇居民？",
     "answer": "宅基地使用权主体限定为本集体经济组织成员，具有身份性、福利性和保障性，法律明确规定不得向城镇居民转让。"},
    {"title": "四、地籍调查", "img": "img_flow.png",
     "text": "1. 分类：初始地籍调查与日常地籍调查（变更调查）。\n"
             "2. 内容：权属调查 + 地籍测量（控制测量、界址点测量、地籍图测绘、面积量算）。\n"
             "3. 界址调查：相邻宗地权利人须到现场共同指界并签字盖章确认。\n"
             "4. 成果：地籍调查表、地籍图、宗地图、面积汇总统计表。",
     "think": "“指界”为什么必须由相邻权利人共同确认？",
     "answer": "界址线是相邻宗地权利人权益的分界线，必须由相邻权利人共同到现场指认、签字确认，才能保证界址认定合法有效。"},
    {"title": "五、地籍图与宗地图", "img": "img_parcel.png",
     "text": "1. 分幅地籍图：城镇 1:500 或 1:1000，农村 1:5000 或 1:10000。\n"
             "2. 宗地图：以宗地为单元绘制，是土地登记发证的附图。\n"
             "3. 地籍要素：行政界线、权属界线、地类界线、界址点、各类注记。\n"
             "4. 宗地图内容：界址点与界址线、权利人、地类、面积、四至、指北针、比例尺、坐标表。",
     "think": "分幅地籍图与宗地图有什么区别与联系？",
     "answer": "分幅地籍图按标准图幅编制；宗地图以宗地为单元单独编绘，比例尺更大、内容更详细，是登记发证的法定附图。"},
    {"title": "六、面积量算", "img": "img_area.png",
     "text": "1. 解析法：坐标法（鞋带公式）\n"
             "   S = ½ |Σ(xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|，直接利用界址点坐标计算，精度最高。\n"
             "2. 图解法：几何图形法、求积仪法等，精度较低。\n"
             "3. 单位换算：1 公顷 = 10000 ㎡ = 15 亩；1 亩 ≈ 666.67 ㎡。\n"
             "4. 质量要求：分级控制、按图幅理论面积校核。",
     "think": "为什么解析法精度高于图解法？",
     "answer": "解析法直接利用界址点坐标按公式计算，避免了图纸伸缩、量测误差等人为因素；图解法受图面比例尺和量测工具限制。"},
    {"title": "七、土地登记", "img": None,
     "text": "1. 我国实行不动产统一登记，统一颁发《不动产权证书》。\n"
             "2. 登记类型：初始登记、变更登记、注销登记、更正登记、抵押登记、查封登记等。\n"
             "3. 登记效力：登记生效主义——不动产物权变动自记载于登记簿时发生效力。\n"
             "4. 登记程序：申请 → 受理 → 审核 → 登簿 → 发证。",
     "think": "更正登记与变更登记有何区别？",
     "answer": "更正登记针对登记簿记载错误的纠正；变更登记针对权利主体或内容依法发生的变化（如转让、更名等）。"},
]
KNOWLEDGE_EN = [
    ("Cadastre & Cadastral Management",
     "1. Cadastre: maps, registers and records documenting land location, boundary, quantity, quality, ownership and use; the 'household register' of land.\n"
     "2. Characteristics: spatial, legal, precise, current (dynamic), continuous.\n"
     "3. Cadastral management: survey, registration, statistics and archive management.\n"
     "4. Main tasks: safeguard public ownership, protect lawful rights of holders.\n"
     "5. Mainline: survey → registration → statistics → archives.",
     "Why is the cadastre called the 'household register' of land?",
     "The cadastre records all basic conditions of land, just as a household register records population information."),
    ("Land Use Classification",
     "1. National standard GB/T 21010-2017: 12 first-level and 73 second-level categories.\n"
     "2. Three broad categories: agricultural land, construction land, unutilized land.\n"
     "3. Memory clue:\n"
     "   01 Cultivated | 02 Garden | 03 Forest | 04 Grassland - agricultural\n"
     "   05 Commercial | 06 Industrial | 07 Residential | 08 Public | 09 Special | 10 Transport - construction\n"
     "   11 Water & Conservancy | 12 Other Land",
     "Why is 'agricultural facility land' under 'Other Land'?",
     "It serves agriculture but differs from productive agricultural land, so it is listed separately."),
    ("Land Ownership",
     "1. Ownership: State ownership and collective ownership.\n"
     "2. Use rights:\n"
     "   State-owned: grant, allocation, lease, etc.;\n"
     "   Collective: contract management, homestead, collective construction land use right.\n"
     "3. Other rights: mortgage, easement, leasehold.\n"
     "4. Principles: lawful subject, clear boundaries, accurate area.",
     "Why can homestead use right not be freely sold to urban residents?",
     "It is restricted to collective members, identity-based and welfare-oriented; the law prohibits transfer to urban residents."),
    ("Cadastral Survey",
     "1. Classification: initial survey and routine (mutative) survey.\n"
     "2. Contents: ownership survey + cadastral measurement (control, boundary point, mapping, area).\n"
     "3. Boundary survey: neighboring right holders must jointly designate the boundary on site.\n"
     "4. Outputs: survey forms, cadastral maps, parcel maps, area tables.",
     "Why must boundary designation be jointly confirmed by neighboring holders?",
     "Boundary is the dividing line of rights; joint on-site confirmation ensures legality and reduces disputes."),
    ("Cadastral Maps & Parcel Maps",
     "1. Sheet cadastral map: urban 1:500 or 1:1000; rural 1:5000 or 1:10000.\n"
     "2. Parcel map: parcel as unit, annex for registration and certification.\n"
     "3. Cadastral elements: administrative, ownership, land-class boundaries, boundary points, annotations.\n"
     "4. Parcel map contents: boundary points/lines, right holder, class, area, four boundaries, north arrow, scale, coordinates.",
     "What are the differences between sheet and parcel maps?",
     "Sheet map covers an area by standard sheets; parcel map is drawn per parcel at larger scale for registration."),
    ("Area Calculation",
     "1. Analytic (coordinate/shoelace) method: S = ½|Σ(xi·yi+1 - xi+1·yi)|; highest accuracy.\n"
     "2. Graphical method: geometric decomposition, planimeter; lower accuracy.\n"
     "3. Conversions: 1 hectare = 10000 m² = 15 mu; 1 mu ≈ 666.67 m².\n"
     "4. Quality: hierarchical control, closure checks.",
     "Why is analytic method more accurate than graphical method?",
     "It uses coordinates directly, avoiding paper distortion and manual measurement errors."),
    ("Land Registration",
     "1. China implements unified real estate registration; Certificate of Real Property Rights.\n"
     "2. Types: initial, alteration, cancellation, correction, mortgage, seizure, etc.\n"
     "3. Effect: registration-effectiveness - real right changes take effect upon entry in register.\n"
     "4. Procedure: application → acceptance → examination → entry → issuance.",
     "What is the difference between correction and alteration registration?",
     "Correction fixes errors in the register; alteration reflects lawful changes in holder or content."),
]

SAMPLE_PARCELS = [
    {"宗地号": "GB0001", "坐落": "长沙市岳麓区望岳街道金星村二组", "权利人": "张某某", "权属性质": "集体土地使用权",
     "一级类": "耕地", "二级类": "水田", "面积平方米": 1250.00, "登记类型": "初始登记（土地承包经营权）"},
    {"宗地号": "GB0002", "坐落": "长沙市岳麓区望岳街道金星村二组", "权利人": "李某某", "权属性质": "集体土地使用权",
     "一级类": "耕地", "二级类": "水田", "面积平方米": 980.50, "登记类型": "初始登记（土地承包经营权）"},
    {"宗地号": "GB0003", "坐落": "长沙市岳麓区莲花镇某村", "权利人": "王某某", "权属性质": "集体土地使用权",
     "一级类": "园地", "二级类": "果园", "面积平方米": 860.00, "登记类型": "初始登记（土地承包经营权）"},
    {"宗地号": "GB0004", "坐落": "长沙市望城区高塘岭街道某村", "权利人": "某村民委员会", "权属性质": "集体土地所有权",
     "一级类": "耕地", "二级类": "旱地", "面积平方米": 12500.00, "登记类型": "初始登记（集体土地所有权）"},
    {"宗地号": "GB0005", "坐落": "长沙高新区麓谷工业园", "权利人": "某智能装备科技有限公司", "权属性质": "国有土地使用权",
     "一级类": "工矿仓储用地", "二级类": "工业用地", "面积平方米": 8600.00, "登记类型": "出让登记（50 年）"},
    {"宗地号": "GB0006", "坐落": "长沙市岳麓区梅溪湖片区", "权利人": "某房地产开发有限公司", "权属性质": "国有土地使用权",
     "一级类": "住宅用地", "二级类": "城镇住宅用地", "面积平方米": 35600.00, "登记类型": "出让登记（70 年）"},
    {"宗地号": "GB0007", "坐落": "长沙市天心区五一商圈", "权利人": "某商业管理有限公司", "权属性质": "国有土地使用权",
     "一级类": "商服用地", "二级类": "零售商业用地", "面积平方米": 4200.00, "登记类型": "出让登记（40 年）"},
    {"宗地号": "GB0008", "坐落": "长沙市芙蓉区人民中路", "权利人": "湖南农业大学", "权属性质": "国有土地使用权",
     "一级类": "公共管理与公共服务用地", "二级类": "教育用地", "面积平方米": 85000.00, "登记类型": "划拨登记"},
    {"宗地号": "GB0009", "坐落": "长沙市岳麓区某镇", "权利人": "某市交通运输局", "权属性质": "国有土地使用权",
     "一级类": "交通运输用地", "二级类": "公路用地", "面积平方米": 32000.00, "登记类型": "划拨登记"},
    {"宗地号": "GB0010", "坐落": "长沙市望城区某村", "权利人": "周某某", "权属性质": "集体土地使用权",
     "一级类": "住宅用地", "二级类": "农村宅基地", "面积平方米": 150.00, "登记类型": "初始登记（宅基地使用权）"},
    {"宗地号": "GB0011", "坐落": "长沙市岳麓区某镇", "权利人": "某农机专业合作社", "权属性质": "集体土地使用权",
     "一级类": "其他土地", "二级类": "设施农用地", "面积平方米": 5600.00, "登记类型": "变更登记"},
    {"宗地号": "GB0012", "坐落": "长沙市望城区某国有林场", "权利人": "某国有林场", "权属性质": "国有土地使用权",
     "一级类": "林地", "二级类": "乔木林地", "面积平方米": 120000.00, "登记类型": "划拨登记"},
    {"宗地号": "GB0013", "坐落": "长沙市望城区某镇", "权利人": "某水库管理所", "权属性质": "国有土地使用权",
     "一级类": "水域及水利设施用地", "二级类": "水库水面", "面积平方米": 45000.00, "登记类型": "划拨登记"},
    {"宗地号": "GB0014", "坐落": "长沙市望城区某镇", "权利人": "某镇人民政府", "权属性质": "集体土地所有权",
     "一级类": "草地", "二级类": "其他草地", "面积平方米": 6800.00, "登记类型": "初始登记（集体土地所有权）"},
    {"宗地号": "GB0015", "坐落": "长沙市开福区金霞物流园", "权利人": "某仓储物流有限公司", "权属性质": "国有土地使用权",
     "一级类": "工矿仓储用地", "二级类": "仓储用地", "面积平方米": 12000.00, "登记类型": "出让登记（50 年）"},
    {"宗地号": "GB0016", "坐落": "长沙市岳麓区洋湖片区", "权利人": "某村集体", "权属性质": "集体土地使用权",
     "一级类": "公共管理与公共服务用地", "二级类": "公园与绿地", "面积平方米": 2300.00, "登记类型": "变更登记"},
    {"宗地号": "GB0017", "坐落": "长沙市雨花区某镇", "权利人": "某殡仪馆", "权属性质": "国有土地使用权",
     "一级类": "特殊用地", "二级类": "殡葬用地", "面积平方米": 15000.00, "登记类型": "划拨登记"},
    {"宗地号": "GB0018", "坐落": "长沙市岳麓区含浦街道某村", "权利人": "刘某某", "权属性质": "集体土地使用权",
     "一级类": "耕地", "二级类": "水浇地", "面积平方米": 1350.00, "登记类型": "初始登记（土地承包经营权）"},
    {"宗地号": "GB0019", "坐落": "长沙市望城区靖港镇某村", "权利人": "某茶厂", "权属性质": "集体土地使用权",
     "一级类": "园地", "二级类": "茶园", "面积平方米": 22000.00, "登记类型": "初始登记（土地承包经营权）"},
    {"宗地号": "GB0020", "坐落": "长沙市芙蓉区车站北路", "权利人": "某铁路局", "权属性质": "国有土地使用权",
     "一级类": "交通运输用地", "二级类": "铁路用地", "面积平方米": 89000.00, "登记类型": "划拨登记"},
    {"宗地号": "GB0021", "坐落": "长沙市望城区某村", "权利人": "孙某某", "权属性质": "集体土地使用权",
     "一级类": "其他土地", "二级类": "田坎", "面积平方米": 45.00, "登记类型": "初始登记（土地承包经营权）"},
    {"宗地号": "GB0022", "坐落": "长沙市岳麓区某小区", "权利人": "陈某某", "权属性质": "国有土地使用权",
     "一级类": "住宅用地", "二级类": "城镇住宅用地", "面积平方米": 89.50, "登记类型": "出让登记（70 年）"},
    {"宗地号": "GB0023", "坐落": "长沙市望城区某镇", "权利人": "某开发区管理委员会", "权属性质": "国有土地使用权",
     "一级类": "水域及水利设施用地", "二级类": "坑塘水面", "面积平方米": 5200.00, "登记类型": "划拨登记"},
    {"宗地号": "GB0024", "坐落": "长沙市望城区湘江沿岸某村", "权利人": "某村集体", "权属性质": "集体土地所有权",
     "一级类": "其他土地", "二级类": "沙地", "面积平方米": 3100.00, "登记类型": "初始登记（集体土地所有权）"},
]

# ============================================================
# 工具函数
# ============================================================
def shoelace(points):
    n = len(points)
    if n < 3: return 0.0
    s = 0.0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0

def mu_area(sqm):
    return sqm / 666.67

# ============================================================
# 张老师吉祥物随机互动
# ============================================================
MASCOT_QUOTES = [
    ("👍 Great job!", "👍 做得不错！"),
    ("💪 Keep going, you can do it!", "💪 继续加油，你可以的！"),
    ("🤔 What do you think of Professor Zhang?", "🤔 你觉得张老师人怎么样？"),
    ("📚 Are you interested in this course?", "📚 你对这门课程感兴趣吗？"),
    ("🎓 What are your plans after graduation?", "🎓 你毕业后准备干嘛？"),
    ("😊 Did you pay attention in class today?", "😊 今天上课认真听了吗？"),
    ("💡 Any questions? Feel free to ask!", "💡 有什么不懂的随时问！"),
    ("🌟 Well done! Keep it up!", "🌟 做得好，保持住！"),
    ("😎 You're getting better and better!", "😎 你越来越棒了！"),
    ("🏆 Aim for the best!", "🏆 争取拿满分！"),
    ("📝 Remember: practice makes perfect!", "📝 记住：熟能生巧！"),
    ("🌍 Land management is a promising field!", "🌍 土地管理是个很有前景的领域！"),
    ("🤓 Do you want to pursue graduate studies?", "🤓 你有考研的打算吗？"),
    ("💼 Any internship plans?", "💼 有没有实习计划呀？"),
    ("🎉 Every question makes you stronger!", "🎉 每做一道题你就更强一点！"),
]

def mascot_say():
    """随机弹出张老师的话"""
    en, zh = random.choice(MASCOT_QUOTES)
    text = f"👨‍🏫 {zh} / {en}"
    st.toast(text, icon="👨‍🏫")

# ============================================================
# 会话状态
# ============================================================
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""
    st.session_state.student_class = ""
    st.session_state.student_id = ""
    st.session_state.class_score = 0
    st.session_state.class_total = 0
    st.session_state.own_score = 0
    st.session_state.own_total = 0
    st.session_state.area_score = 0
    st.session_state.area_total = 0
    st.session_state.map_score = 0
    st.session_state.map_total = 0
    st.session_state.flow_score = 0

# ============================================================
# 侧边栏
# ============================================================
st.sidebar.title("📐 地籍管理实训系统")
st.sidebar.caption("湖南农业大学 · 土地资源管理专业")

# 语言切换
lang_choice = st.sidebar.radio("语言 / Language", ["中文", "English"])
st.session_state.lang = "zh" if lang_choice == "中文" else "en"

# 学生信息
with st.sidebar.expander(t("👤 学生信息登记", "Student Registration"), expanded=True):
    st.session_state.student_name = st.text_input(t("姓名", "Name"), st.session_state.student_name)
    st.session_state.student_class = st.text_input(t("班级", "Class"), st.session_state.student_class)
    st.session_state.student_id = st.text_input(t("学号", "Student ID"), st.session_state.student_id)

# ============================================================
# 张老师聊天机器人
# ============================================================
def teacher_reply(user_msg):
    """根据学生输入返回张老师的回复"""
    msg = user_msg.lower()
    replies = [
        (["你好", "老师好", "hello", "hi", "在吗"], "你好同学！有什么问题随时问我 😊\nHello! How can I help you?"),
        (["难", "不会", "不懂", "学不会"], "别着急，慢慢来！先从知识学习模块开始看，多做几道题就熟练了。\nDon't worry, take your time. Start with the Knowledge section."),
        (["考试", "怎么考", "考点", "重点"], "考试重点都在这9个模块里，把每个练习都做一遍，综合测验能上80分就没问题。\nThe exam covers all 9 modules; score 80+ on the quiz and you're good."),
        (["作业", "任务", "要交"], "做完各模块练习后，到「学习统计与提交」下载报告发给我就行。\nFinish the modules, then download your report from the Scores page."),
        (["毕业", "就业", "工作", "考研", "前途"], "土地资源管理专业就业面很广：自然资源局、规划院、房地产公司、测绘单位都可以，考研也很有优势。\nThis major has great career prospects: natural resources bureau, planning institutes, real estate, surveying."),
        (["张老师", "你怎么样", "老师好帅", "老师人好"], "哈哈，谢谢同学！好好学这门课，将来你会比我更厉害 💪\nHaha thanks! Study hard, you'll be better than me!"),
        (["感兴趣", "喜欢", "有意思"], "很好！地籍管理是不动产统一登记的基础，现在自然资源系统很缺这方面的人才。\nGreat! Cadastral management is the foundation of real estate registration."),
        (["谢谢", "感谢", "thanks", "thank"], "不客气！有问题随时找我 🙏\nYou're welcome! Feel free to ask anytime."),
        (["无聊", "不想学", "累"], "坚持一下！做完这道题休息10分钟，然后继续 💪\nHang in there! Take a 10-min break after this question."),
    ]
    for keywords, reply in replies:
        for kw in keywords:
            if kw in msg:
                return reply
    # 默认回复
    defaults = [
        "嗯，这个问题不错，你先看看知识学习模块里有没有相关内容 📖",
        "Good question! Check the Knowledge section first 📖",
        "你先做两道练习题试试，有具体问题再来问我 😊",
        "Try doing a few practice questions first, then ask me if you get stuck.",
        "这个问题我们下节课讲到，你先预习一下第四章地籍调查 📚",
    ]
    return random.choice(defaults)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [("assistant", "👨‍🏫 同学你好！有什么问题可以问我哦～\nHi! What can I do for you?")]

with st.sidebar.expander(t("💬 和张老师聊天", "💬 Chat with Prof. Zhang"), expanded=False):
    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(text)
    user_input = st.chat_input(t("说点什么...", "Say something..."))
    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        reply = teacher_reply(user_input)
        st.session_state.chat_history.append(("assistant", "👨‍🏫 " + reply))
        st.rerun()

# 模块导航
modules_zh = ["📖 知识学习", "🌾 土地分类练习", "⚖️ 权属判断", "📐 面积计算实训",
              "🔢 调查流程排序", "🔍 宗地数据查询", "🗺️ 宗地图识别", "📝 综合测验",
              "📊 学习统计与提交", "ℹ️ 使用说明"]
modules_en = ["📖 Knowledge", "🌾 Land Classification", "⚖️ Ownership", "📐 Area Calculation",
              "🔢 Survey Procedure", "🔍 Parcel Search", "🗺️ Parcel Map Quiz", "📝 Final Quiz",
              "📊 My Scores & Report", "ℹ️ Help"]
modules = modules_zh if st.session_state.lang == "zh" else modules_en
module = st.sidebar.radio(t("功能模块", "Modules"), modules)

st.sidebar.markdown("---")
st.sidebar.caption("V2.5 Web版")

# ============================================================
# 模块1：知识学习
# ============================================================
if module.startswith("📖"):
    st.header(t("📖 知识学习", "📖 Knowledge Study"))
    klist = KNOWLEDGE if st.session_state.lang == "zh" else KNOWLEDGE_EN
    chapter_idx = st.selectbox(t("选择章节", "Select Chapter"), range(len(klist)),
                               format_func=lambda i: klist[i][0] if st.session_state.lang == "en" else KNOWLEDGE[i]["title"])
    if st.session_state.lang == "zh":
        ch = KNOWLEDGE[chapter_idx]
        st.subheader(ch["title"])
        if ch["img"]:
            p = os.path.join(IMG_DIR, ch["img"])
            if os.path.exists(p): st.image(p, use_column_width=True)
        st.markdown(ch["text"])
        st.markdown("---")
        st.markdown(f"**💭 {t('思考题', 'Thinking Question')}：** {ch['think']}")
        with st.expander(t("查看参考答案", "View Answer")):
            st.info(ch["answer"])
    else:
        title, text, think, answer = KNOWLEDGE_EN[chapter_idx]
        st.subheader(title)
        img = KNOWLEDGE[chapter_idx]["img"]
        if img:
            p = os.path.join(IMG_DIR, img)
            if os.path.exists(p): st.image(p, use_column_width=True)
        st.markdown(text)
        st.markdown("---")
        st.markdown(f"**💭 Thinking Question:** {think}")
        with st.expander("View Answer"):
            st.info(answer)

# ============================================================
# 模块2：土地分类练习
# ============================================================
elif module.startswith("🌾"):
    st.header(t("🌾 土地分类练习", "🌾 Land Classification Practice"))
    mode = st.radio(t("练习模式", "Mode"),
        [t("模式A：判断二级地类属于哪个一级类", "Mode A: which first-level class?"),
         t("模式B：选出属于某一级类的二级地类", "Mode B: pick second-level class")])
    if mode.startswith(t("模式A", "Mode A")):
        if 'class_idx' not in st.session_state or st.button(t("换一题", "Next Question")):
            st.session_state.class_idx = random.randrange(len(CLASS_PRACTICE))
        idx = st.session_state.class_idx
        sub, first, code = CLASS_PRACTICE[idx]
        sub_en = ["Paddy field","Irrigated land","Dry land","Orchard","Tea plantation",
                  "Arbor forest","Bamboo forest","Natural pasture","Other grassland",
                  "Retail commercial","Catering","Hotel","Industrial","Warehousing","Mining",
                  "Urban residential","Rural homestead","Education","Medical","Parks & green",
                  "Military","Religious","Funeral","Railway","Highway","Rural road",
                  "River","Reservoir","Canal","Pond","Idle","Agri-facility","Sandy","Bare","Field ridge"][idx]
        first_en = FIRST_CLASSES_EN[FIRST_CLASSES.index(first)]
        st.markdown(f"**{t('下列二级地类', 'Which first-level class does the second-level land type')} “{sub} / {sub_en}” {t('属于哪个一级类？', 'belong to?')}**")
        choices = [t(c, FIRST_CLASSES_EN[i]) for i, c in enumerate(FIRST_CLASSES)]
        answer = st.radio("", choices, key=f"class_a_{idx}")
        if st.button(t("提交答案", "Submit")):
            st.session_state.class_total += 1
            chosen_first = FIRST_CLASSES[choices.index(answer)]
            if chosen_first == first:
                st.success(f"✅ {t('正确', 'Correct')}！{sub} → {first}（{code}）")
                st.session_state.class_score += 1
                st.balloons()
                if random.random() < 0.5: mascot_say()
            else:
                st.error(f"❌ {t('错误。正确答案', 'Wrong. Correct answer')}：{first} / {first_en}（{code}）")
            p = os.path.join(IMG_DIR, CLASS_IMAGES[idx])
            if os.path.exists(p): st.image(p, caption=f"{sub} / {sub_en}", width=300)
    else:
        target = st.selectbox(t("选择一级地类", "Select first-level class"),
                              [t(c, FIRST_CLASSES_EN[i]) for i, c in enumerate(FIRST_CLASSES)])
        target_zh = FIRST_CLASSES[ [t(c, FIRST_CLASSES_EN[i]) for i,c in enumerate(FIRST_CLASSES)].index(target) ]
        candidates = [(i, c[0]) for i, c in enumerate(CLASS_PRACTICE) if c[1] == target_zh]
        if candidates:
            opts = [c[1] for c in candidates]
            st.markdown(f"**{t('请选出属于', 'Pick the second-level class of')} “{target}” {t('的二级地类', '')}**")
            chosen = st.radio("", opts, key="class_b")
            if st.button(t("确认选择", "Confirm")):
                st.session_state.class_total += 1
                st.session_state.class_score += 1
                st.success(f"✅ {t('正确！', 'Correct!')} {chosen} {t('属于', 'belongs to')} {target}")
    st.caption(f"{t('当前得分', 'Score')}：{st.session_state.class_score} / {st.session_state.class_total}")

# ============================================================
# 模块3：权属判断
# ============================================================
elif module.startswith("⚖️"):
    st.header(t("⚖️ 权属判断", "⚖️ Ownership Judgment"))
    if 'own_idx' not in st.session_state or st.button(t("下一题", "Next Question")):
        st.session_state.own_idx = random.randrange(len(OWNERSHIP_BANK))
    idx = st.session_state.own_idx
    statement, answer, explain = OWNERSHIP_BANK[idx]
    statement_en, explain_en = OWNERSHIP_BANK_EN[idx]
    st.markdown(f"**{t('判断下列土地属于国家所有还是集体所有：', 'Is the following land State-owned or collectively-owned?')}**")
    st.markdown(f"### “{statement}”")
    if st.session_state.lang == "en": st.markdown(f"*{statement_en}*")
    choice = st.radio("", [t("国家所有（国有）", "State-owned"), t("集体所有", "Collectively-owned")])
    if st.button(t("提交判断", "Submit")):
        st.session_state.own_total += 1
        correct = "国有" if choice.startswith(t("国家", "State")) else "集体"
        if correct == answer:
            st.success(f"✅ {t('判断正确！', 'Correct!')}")
            st.session_state.own_score += 1
            if random.random() < 0.5: mascot_say()
        else:
            st.error(f"❌ {t('判断错误。正确答案', 'Wrong. Correct answer')}：{t(answer, 'State-owned' if answer=='国有' else 'Collectively-owned')}")
        st.info(f"📖 {t('解析', 'Explanation')}：{explain if st.session_state.lang=='zh' else explain_en}")
    p = os.path.join(IMG_DIR, "img_ownership.png")
    if os.path.exists(p): st.image(p, use_column_width=True)
    st.caption(f"{t('当前得分', 'Score')}：{st.session_state.own_score} / {st.session_state.own_total}")

# ============================================================
# 模块4：面积计算实训
# ============================================================
elif module.startswith("📐"):
    st.header(t("📐 面积计算实训", "📐 Area Calculation Practice"))
    pidx = st.selectbox(t("选择宗地", "Select Parcel"), range(len(AREA_PARCELS)),
        format_func=lambda i: AREA_PARCELS[i]["name"] if st.session_state.lang=="zh" else AREA_PARCELS_EN[i][0])
    parcel = AREA_PARCELS[pidx]
    pname = parcel["name"] if st.session_state.lang=="zh" else AREA_PARCELS_EN[pidx][0]
    phint = parcel["hint"] if st.session_state.lang=="zh" else AREA_PARCELS_EN[pidx][1]
    st.markdown(f"**{pname}**")
    st.markdown(f"💡 {phint}")
    pts = parcel["pts"]
    df_pts = pd.DataFrame(pts, columns=["X(m)", "Y(m)"])
    st.dataframe(df_pts, use_container_width=True)
    st.caption(t("提示：使用鞋带公式 S = ½|Σ(xᵢyᵢ₊₁ − xᵢ₊₁yᵢ)|", "Hint: Use shoelace formula S = ½|Σ(xi·yi+1 − xi+1·yi)|"))
    user_area = st.number_input(t("请输入你计算的宗地面积（平方米）", "Enter your calculated area (m²)"),
                                min_value=0.0, step=1.0, format="%.2f")
    if st.button(t("提交答案", "Submit")):
        correct = shoelace(pts)
        st.session_state.area_total += 1
        if abs(user_area - correct) < 0.5:
            st.success(f"✅ {t('计算正确！面积', 'Correct! Area')} = {correct:.2f} ㎡ ≈ {mu_area(correct):.2f} {t('亩', 'mu')}")
            st.session_state.area_score += 1
            if random.random() < 0.5: mascot_say()
        else:
            st.error(f"❌ {t('计算有误。正确答案', 'Wrong. Correct answer')}：{correct:.2f} ㎡ ≈ {mu_area(correct):.2f} {t('亩', 'mu')}")
    st.caption(f"{t('当前得分', 'Score')}：{st.session_state.area_score} / {st.session_state.area_total}")

# ============================================================
# 模块5：调查流程排序
# ============================================================
elif module.startswith("🔢"):
    st.header(t("🔢 初始地籍调查流程排序", "🔢 Cadastral Survey Procedure Order"))
    st.write(t("请将下列 8 个步骤按正确顺序排列", "Arrange the following 8 steps in correct order"))
    if 'flow_order' not in st.session_state:
        st.session_state.flow_order = list(range(len(SURVEY_STEPS)))
        random.shuffle(st.session_state.flow_order)
    if st.button(t("🔀 重新乱序", "🔀 Shuffle")):
        random.shuffle(st.session_state.flow_order)
        st.rerun()
    order = st.session_state.flow_order
    user_order = []
    for pos in range(8):
        opts = []
        for j in range(8):
            idx = order[j]
            name = SURVEY_STEPS[idx][0] if st.session_state.lang=="zh" else SURVEY_STEPS_EN[idx][0]
            opts.append(f"{j+1}. {name}")
        choice = st.selectbox(f"{t('第', 'Step ')}{pos+1}{t('步是？', ' is:')}", opts, key=f"flow_{pos}")
        chosen_idx = int(choice.split(".")[0]) - 1
        user_order.append(order[chosen_idx])
    if st.button(t("提交排序", "Submit Order")):
        correct_count = sum(1 for i, v in enumerate(user_order) if v == i)
        st.session_state.flow_score = correct_count
        if correct_count == 8:
            st.success(f"🎉 {t('全部正确！8/8 步排序完全正确！', 'Perfect! All 8 steps correct!')}")
        else:
            st.warning(f"{t('正确', 'Correct')} {correct_count}/8。{t('正确顺序如下：', 'Correct order:')}")
            for i in range(8):
                name = SURVEY_STEPS[i][0] if st.session_state.lang=="zh" else SURVEY_STEPS_EN[i][0]
                desc = SURVEY_STEPS[i][1] if st.session_state.lang=="zh" else SURVEY_STEPS_EN[i][1]
                st.write(f"{i+1}. **{name}** —— {desc}")

# ============================================================
# 模块6：宗地数据查询
# ============================================================
elif module.startswith("🔍"):
    st.header(t("🔍 宗地数据查询", "🔍 Parcel Data Search"))
    df = pd.DataFrame(SAMPLE_PARCELS)
    col1, col2, col3 = st.columns(3)
    with col1:
        kw = st.text_input(t("关键字搜索", "Keyword"), "")
    with col2:
        fclass = st.selectbox(t("一级类", "First-level Class"), [t("全部", "All")] + list(df["一级类"].unique()))
    with col3:
        own = st.selectbox(t("权属性质", "Ownership"), [t("全部", "All")] + list(df["权属性质"].unique()))
    filtered = df.copy()
    if kw:
        mask = df["宗地号"].str.contains(kw) | df["坐落"].str.contains(kw) | df["权利人"].str.contains(kw)
        filtered = filtered[mask]
    if fclass != t("全部", "All"): filtered = filtered[filtered["一级类"] == fclass]
    if own != t("全部", "All"): filtered = filtered[filtered["权属性质"] == own]
    st.write(f"{t('共', 'Total')} {len(filtered)} {t('宗', 'parcels')}")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.markdown("---")
    st.subheader(t("宗地图示例", "Sample Parcel Map"))
    st.image(os.path.join(IMG_DIR, "img_parcel.png"), caption="GB0001", use_column_width=True)

# ============================================================
# 模块7：宗地图识别
# ============================================================
elif module.startswith("🗺️"):
    st.header(t("🗺️ 宗地图识别", "🗺️ Parcel Map Identification"))
    st.image(os.path.join(IMG_DIR, "img_parcel.png"), caption=t("宗地图示例", "Sample Parcel Map"), use_column_width=True)
    st.markdown("---")
    if 'map_q_idx' not in st.session_state: st.session_state.map_q_idx = 0
    q_idx = st.session_state.map_q_idx % len(MAP_QUESTIONS)
    if st.session_state.lang == "zh":
        q, opts, correct, explain = MAP_QUESTIONS[q_idx]
    else:
        q, opts, explain = MAP_QUESTIONS_EN[q_idx]
        correct = MAP_QUESTIONS[q_idx][2]
    st.markdown(f"**{t('第', 'Question')} {q_idx+1} / {len(MAP_QUESTIONS)}**")
    st.markdown(f"**{q}**")
    choice = st.radio("", opts, key=f"map_q_{q_idx}")
    if st.button(t("提交答案", "Submit")):
        st.session_state.map_total += 1
        if opts.index(choice) == correct:
            st.success("✅ " + t("回答正确！", "Correct!"))
            st.session_state.map_score += 1
            if random.random() < 0.5: mascot_say()
        else:
            st.error(f"❌ {t('回答错误。正确答案', 'Wrong. Correct answer')}：{opts[correct]}")
        st.info(f"📖 {explain}")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ " + t("上一题", "Previous")):
            st.session_state.map_q_idx = (q_idx - 1) % len(MAP_QUESTIONS)
            st.rerun()
    with c2:
        if st.button(t("下一题", "Next") + " ➡️"):
            st.session_state.map_q_idx = (q_idx + 1) % len(MAP_QUESTIONS)
            st.rerun()
    st.caption(f"{t('当前得分', 'Score')}：{st.session_state.map_score} / {st.session_state.map_total}")

# ============================================================
# 模块8：综合测验
# ============================================================
elif module.startswith("📝"):
    st.header(t("📝 综合测验", "📝 Final Quiz"))
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if not st.session_state.quiz_started:
        st.write(t("随机抽取 15 题，每题 1 分，满分 100 分。", "15 random questions, 1 point each, 100 points total."))
        if st.button(t("开始测验", "Start Quiz"), type="primary"):
            n = min(15, len(QUIZ_BANK))
            st.session_state.quiz_questions = random.sample(range(len(QUIZ_BANK)), n)
            st.session_state.quiz_answers = [None] * n
            st.session_state.quiz_submitted = False
            st.session_state.quiz_started = True
            st.rerun()
    else:
        qidx_list = st.session_state.quiz_questions
        for i, qi in enumerate(qidx_list):
            if st.session_state.lang == "zh":
                q, opts, correct, explain = QUIZ_BANK[qi]
            else:
                q, opts, explain = QUIZ_BANK_EN[qi]
                correct = QUIZ_BANK[qi][2]
            st.markdown(f"**{t('第', 'Q')} {i+1}**：{q}")
            if st.session_state.quiz_submitted:
                user_ans = st.session_state.quiz_answers[i]
                if user_ans == correct:
                    st.success(f"✅ {opts[user_ans]}")
                else:
                    st.error(f"❌ {t('你的答案', 'Your answer')}：{opts[user_ans] if user_ans is not None else t('未作答','N/A')} | {t('正确答案', 'Correct')}：{opts[correct]}")
                st.caption(f"📖 {explain}")
            else:
                choice = st.radio("", opts, key=f"quiz_{i}", index=None)
                st.session_state.quiz_answers[i] = opts.index(choice) if choice else None
            st.markdown("---")
        if not st.session_state.quiz_submitted:
            if st.button(t("交卷", "Submit Paper"), type="primary"):
                st.session_state.quiz_submitted = True
                score = sum(1 for i, qi in enumerate(qidx_list)
                           if st.session_state.quiz_answers[i] == QUIZ_BANK[qi][2])
                st.session_state.quiz_score = round(score / len(qidx_list) * 100, 1)
                mascot_say()
                st.rerun()
        else:
            score = st.session_state.quiz_score
            st.subheader(f"🎯 {t('测验成绩', 'Score')}：{score} {t('分', 'points')}")
            if score >= 80:
                st.balloons(); st.success(t("优秀！🎉", "Excellent! 🎉"))
            elif score >= 60: st.info(t("良好，继续加油！", "Good, keep it up!"))
            else: st.warning(t("需要复习哦！", "Need to review!"))
            if st.button(t("重新抽题再测一次", "Try Again")):
                st.session_state.quiz_started = False
                st.rerun()

# ============================================================
# 模块9：学习统计与提交
# ============================================================
elif module.startswith("📊"):
    st.header(t("📊 学习统计与成绩提交", "📊 My Scores & Report"))
    st.subheader(t("学生信息", "Student Information"))
    name = st.session_state.student_name or t("未登记", "Not registered")
    cls = st.session_state.student_class or "-"
    sid = st.session_state.student_id or "-"
    st.write(f"**{t('姓名', 'Name')}：** {name}  |  **{t('班级', 'Class')}：** {cls}  |  **{t('学号', 'ID')}：** {sid}")

    st.markdown("---")
    st.subheader(t("各模块得分", "Module Scores"))

    quiz_score = st.session_state.get("quiz_score", 0)
    class_pct = (st.session_state.class_score / st.session_state.class_total * 100) if st.session_state.class_total > 0 else 0
    own_pct = (st.session_state.own_score / st.session_state.own_total * 100) if st.session_state.own_total > 0 else 0
    area_pct = (st.session_state.area_score / st.session_state.area_total * 100) if st.session_state.area_total > 0 else 0
    map_pct = (st.session_state.map_score / st.session_state.map_total * 100) if st.session_state.map_total > 0 else 0
    flow_pct = st.session_state.flow_score / 8 * 100

    score_data = {
        t("模块", "Module"): [t("综合测验", "Final Quiz"), t("土地分类练习", "Classification"),
                            t("权属判断", "Ownership"), t("面积计算", "Area Calc"),
                            t("宗地图识别", "Map Quiz"), t("流程排序", "Procedure")],
        t("得分率", "Score %"): [f"{quiz_score:.0f}%", f"{class_pct:.1f}%",
                               f"{own_pct:.1f}%", f"{area_pct:.1f}%",
                               f"{map_pct:.1f}%", f"{flow_pct:.1f}%"],
    }
    st.dataframe(score_data, use_container_width=True, hide_index=True)

    # 综合成绩 = 测验40% + 分类15% + 权属15% + 面积10% + 识图10% + 流程10%
    total = quiz_score*0.4 + class_pct*0.15 + own_pct*0.15 + area_pct*0.1 + map_pct*0.1 + flow_pct*0.1
    st.markdown("---")
    st.subheader(f"🎯 {t('综合成绩', 'Overall Score')}：**{total:.1f}** {t('分', 'points')}")

    # 生成报告文本
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"""地籍管理实训系统 学习报告
============================
姓名 / Name: {name}
班级 / Class: {cls}
学号 / Student ID: {sid}
时间 / Time: {now}
----------------------------
综合测验 Final Quiz: {quiz_score:.1f} 分
土地分类练习 Classification: {class_pct:.1f}% ({st.session_state.class_score}/{st.session_state.class_total})
权属判断 Ownership: {own_pct:.1f}% ({st.session_state.own_score}/{st.session_state.own_total})
面积计算 Area Calc: {area_pct:.1f}% ({st.session_state.area_score}/{st.session_state.area_total})
宗地图识别 Map Quiz: {map_pct:.1f}% ({st.session_state.map_score}/{st.session_state.map_total})
流程排序 Procedure: {flow_pct:.1f}% ({st.session_state.flow_score}/8)
----------------------------
综合成绩 Overall: {total:.1f} 分
"""

    st.markdown("---")
    st.subheader(t("提交方式", "How to Submit"))
    st.info(t("请将下方学习报告下载或截图，发送给老师邮箱 39116272@qq.com，或在课程群提交。",
              "Please download or screenshot the report below and send to your teacher."))

    st.download_button(
        label=t("📥 下载学习报告（.txt）", "📥 Download Report (.txt)"),
        data=report,
        file_name=f"学习报告_{name}_{now[:10]}.txt",
        mime="text/plain",
    )

    with st.expander(t("预览报告内容", "Preview Report")):
        st.code(report)

# ============================================================
# 模块10：使用说明
# ============================================================
elif module.startswith("ℹ️"):
    st.header(t("ℹ️ 使用说明", "ℹ️ Help"))
    st.markdown("""
    ### 《地籍管理》课程学习与实训系统
    **湖南农业大学 · 土地资源管理专业**

    """)
    st.markdown(t("""
    **使用方法：**
    1. 在左侧边栏填写姓名、班级、学号
    2. 通过左侧导航选择要练习的模块
    3. 各答题模块会自动记录你的得分
    4. 完成后请截图测验成绩提交给老师

    **模块说明：**
    - 📖 知识学习：7章核心知识点图文学习
    - 🌾 土地分类练习：GB/T 21010—2017 土地分类练习
    - ⚖️ 权属判断：国有/集体土地所有权判断
    - 📐 面积计算实训：坐标解析法计算宗地面积
    - 🔢 调查流程排序：初始地籍调查八步流程
    - 🔍 宗地数据查询：24宗示例宗地检索
    - 🗺️ 宗地图识别：结合宗地图识别各类要素
    - 📝 综合测验：随机抽15题自动判分
    """,
    """
    **How to use:**
    1. Fill in your name, class and student ID in the sidebar
    2. Select a module from the navigation
    3. Your scores are tracked automatically
    4. Screenshot your quiz score and submit to your teacher

    **Modules:**
    - 📖 Knowledge: 7 chapters with illustrations
    - 🌾 Land Classification: GB/T 21010-2017 practice
    - ⚖️ Ownership: State vs collective land rights
    - 📐 Area Calculation: Shoelace method practice
    - 🔢 Survey Procedure: 8-step cadastral survey order
    - 🔍 Parcel Search: 24 sample parcels database
    - 🗺️ Parcel Map Quiz: Identify map elements
    - 📝 Final Quiz: 15 random questions, auto-graded
    """))
