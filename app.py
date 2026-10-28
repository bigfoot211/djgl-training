# -*- coding: utf-8 -*-
"""
《地籍管理》课程学习与实训系统 · Web版 V2.5
湖南农业大学 · 土地资源管理专业
中英双语 · 全部功能与桌面版一致
"""
import streamlit as st
import json, os, random, math, datetime, smtplib
from email.message import EmailMessage
import pandas as pd

# ============================================================
# 张老师吉祥物台词库（提前定义）
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
    ("🏞️ You'll be protecting China's land resources!", "🏞️ 将来你们要守护国家的土地资源！"),
    ("📈 This major has great job prospects!", "📈 咱们专业就业前景非常好！"),
    ("🏙️ Urban-rural integration needs your talent!", "🏙️ 城乡一体化建设需要你们这样的人才！"),
    ("🗺️ Every parcel tells a story of our country!", "🗺️ 每一宗地都记录着国家发展的故事！"),
    ("🌱 You'll be the guardians of cultivated land!", "🌱 你们是未来耕地保护的守护者！"),
    ("💻 Digital land management is the future!", "💻 数字国土、智慧城市都是你们的舞台！"),
    ("🏛️ You'll work for people's wellbeing!", "🏛️ 你们的工作关系到千家万户的安居乐业！"),
    ("🚀 Real estate registration is booming!", "🚀 不动产统一登记现在正是热门方向！"),
    ("🌳 Balancing development and protection is your mission!", "🌳 发展与保护平衡，就是你们这代人的使命！"),
    ("📊 Big data + land management = hot career!", "📊 大数据+土地管理，这就业方向多时髦！"),
    ("🏡 You'll help people get their home certificates!", "🏡 将来你们帮老百姓拿不动产权证，积德的事！"),
    ("🏔️ From mountains to cities, you'll map it all!", "🏔️ 从山林到城市，将来都是你们去丈量！"),
    ("💡 This is a golden age for land professionals!", "💡 现在是土地专业人才的黄金时代！"),
    ("👏 You chose a stable and meaningful major!", "👏 你们选了个稳定又有意义的好专业！"),
    ("🌏 Every inch of land matters to the country!", "🌏 每一寸土地都关系着国家发展大局！"),
]

st.set_page_config(
    page_title="地籍管理实训系统 / Cadastral Training System",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")

# ============================================================
# 右上角固定漂浮吉祥物（答题几次后才出现，自动换话）
# ============================================================
if 'mascot_visits' not in st.session_state:
    st.session_state.mascot_visits = 0
st.session_state.mascot_visits += 1

# 答了3题后吉祥物才出现
if st.session_state.mascot_visits >= 3:
    if 'mascot_msg' not in st.session_state:
        st.session_state.mascot_msg = random.choice(MASCOT_QUOTES)
        st.session_state.mascot_count = 0

    # 每次交互都换一句话
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
    @keyframes bubbleFadeIn {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes bubbleFadeOut {
        from { opacity: 1; }
        to { opacity: 0; visibility: hidden; }
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
        animation: bubbleFadeIn 0.5s ease-out, bubbleFadeOut 0.5s ease-in 5s forwards;
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
def mascot_say():
    """随机弹出张老师的话"""
    en, zh = random.choice(MASCOT_QUOTES)
    text = f"👨‍🏫 {zh} / {en}"
    st.toast(text, icon="👨‍🏫")

# ============================================================
# 学生能力画像（文字画像 + SVG 能力雷达图 + SVG 卡通画像）
# 与桌面版六维口径一致：分类辨析/权属判断/面积计算/识图能力/流程逻辑/综合运用
# ============================================================
PORTRAIT_DIMS = [
    ("分类辨析", "class", "Classification"),
    ("权属判断", "own", "Ownership"),
    ("面积计算", "area", "Area"),
    ("识图能力", "map", "Parcel Map"),
    ("流程逻辑", "flow", "Flow"),
    ("综合运用", "quiz", "Quiz"),
]
PORTRAIT_LEVELS = [
    (85, "首席调查员", "Chief Surveyor"),
    (70, "高级调查员", "Senior Surveyor"),
    (50, "调查员", "Surveyor"),
    (30, "助理调查员", "Assistant Surveyor"),
    (0, "见习调查员", "Trainee Surveyor"),
]
PORTRAIT_ADVICE = {
    "class": "回到【土地分类练习】模块，用模式A/模式B结合实景图反复练习，牢记12个一级类与常见二级类的归属。",
    "own": "回到【权属判断】模块复习国有/集体土地所有权的判定原则，注意宅基地使用权、承包经营权与出让取得的区别。",
    "area": "回到【面积计算实训】模块，先点“查看参考答案”看坐标法步骤，再把每个宗地亲手算一遍。",
    "map": "回到【宗地图识别】模块，结合示例宗地图逐项确认界址点、界址线、地类注记、四至与指北针。",
    "flow": "完成【调查流程排序】模块，把初始地籍调查八步流程按正确顺序排出来，流程逻辑自然记牢。",
    "quiz": "回到【知识学习】模块把七个章节复习一遍，再参加【综合测验】检验综合运用能力。",
}


def portrait_scores_from(ss):
    """从会话状态计算六维得分 0-100（未作答维度计 0 分）"""
    def pct(s, t):
        return round(s / t * 100) if t else 0
    return {
        "class": pct(ss.get("class_score", 0), ss.get("class_total", 0)),
        "own": pct(ss.get("own_score", 0), ss.get("own_total", 0)),
        "area": pct(ss.get("area_score", 0), ss.get("area_total", 0)),
        "map": pct(ss.get("map_score", 0), ss.get("map_total", 0)),
        "flow": round(ss.get("flow_score", 0) / 8 * 100),
        "quiz": round(ss.get("quiz_score", 0)),
    }


def portrait_total(scores):
    """综合得分：测验40% + 分类15% + 权属15% + 面积10% + 识图10% + 流程10%"""
    return (scores["quiz"] * 0.4 + scores["class"] * 0.15 + scores["own"] * 0.15
            + scores["area"] * 0.1 + scores["map"] * 0.1 + scores["flow"] * 0.1)


def portrait_level_from(total):
    """按综合得分返回 (中文等级, 英文等级)"""
    for th, zh, en in PORTRAIT_LEVELS:
        if total >= th:
            return zh, en
    return PORTRAIT_LEVELS[-1][1], PORTRAIT_LEVELS[-1][2]


def portrait_summary_lines(scores, total):
    """文字画像：亮点/待提升等描述行"""
    lvl_zh, lvl_en = portrait_level_from(total)
    attempted = [(zh, scores[k]) for zh, k, _ in PORTRAIT_DIMS if scores[k] > 0]
    lines = [f"你的综合得分 {total:.0f} 分，能力等级为「{lvl_zh} / {lvl_en}」。"]
    if not attempted:
        lines.append("你还没有完成任何练习模块：先去【知识学习】浏览章节，再到各练习模块作答，能力画像会随成绩实时更新。")
        return lines
    strong = [(zh, v) for zh, v in attempted if v >= 80]
    weak = [(zh, v) for zh, v in attempted if v < 60]
    if strong:
        lines.append("能力亮点：" + "、".join(f"{zh}（{v}分）" for zh, v in strong[:3]) + "，继续保持！")
    if weak:
        lines.append("待提升：" + "、".join(f"{zh}（{v}分）" for zh, v in weak[:3]) + "，稍加练习就能明显进步。")
    if not strong and not weak and len(attempted) >= 3:
        lines.append("各维度发展均衡，属于稳扎稳打的均衡型学习者。")
    return lines


def portrait_advice_lines(scores):
    """成长建议：低于60分维度 + 未做的流程维度"""
    out = []
    tried_any = any(scores[k] > 0 for k in ("class", "own", "area", "map", "quiz"))
    for zh, k, _ in PORTRAIT_DIMS:
        if k == "flow":
            if tried_any and scores[k] == 0:
                out.append(PORTRAIT_ADVICE[k])
        elif 0 < scores[k] < 60:
            out.append(PORTRAIT_ADVICE[k])
    return out


def svg_radar(scores, width=400, height=380):
    """六维能力雷达图（内联 SVG，浏览器渲染中文，无服务器字体依赖）"""
    cx, cy, R = width / 2, height / 2 - 16, 118
    n = len(PORTRAIT_DIMS)

    def pt(i, r):
        ang = math.radians(-90 + i * 360.0 / n)
        return round(cx + r * math.cos(ang), 1), round(cy + r * math.sin(ang), 1)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    # 网格环 25/50/75/100
    for g in (25, 50, 75, 100):
        pts = " ".join(f"{x},{y}" for x, y in (pt(i, R * g / 100.0) for i in range(n)))
        parts.append(f'<polygon points="{pts}" fill="none" stroke="#CFD8DC" stroke-width="1"/>')
    # 轴线与维度名
    for i, (zh, k, en) in enumerate(PORTRAIT_DIMS):
        x, y = pt(i, R)
        lx, ly = pt(i, R + 28)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#B0BEC5" stroke-width="1"/>')
        parts.append(f'<text x="{lx}" y="{ly}" font-size="15" font-weight="bold" fill="#37474F" text-anchor="middle" dominant-baseline="middle">{zh}</text>')
    # 数据多边形
    pts = " ".join(f"{x},{y}" for x, y in (pt(i, R * scores[k] / 100.0) for i, (zh, k, en) in enumerate(PORTRAIT_DIMS)))
    parts.append(f'<polygon points="{pts}" fill="#BBDEFB" fill-opacity="0.85" stroke="#1565C0" stroke-width="2"/>')
    # 分数点与数值
    for i, (zh, k, en) in enumerate(PORTRAIT_DIMS):
        x, y = pt(i, R * scores[k] / 100.0)
        parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#1565C0"/>')
        if scores[k] > 0:
            parts.append(f'<text x="{x}" y="{y - 12}" font-size="13" fill="#0D47A1" text-anchor="middle">{scores[k]}</text>')
    parts.append(f'<text x="{cx}" y="{height - 10}" font-size="14" fill="#78909C" text-anchor="middle">能力雷达图 / Ability Radar</text>')
    parts.append('</svg>')
    return "".join(parts)


def svg_avatar(scores, total, lvl_zh, width=360, height=390):
    """卡通「小小地籍调查员」画像（SVG，随等级换帽子/装备/徽章）"""
    idx = 0
    for i, (th, zh, en) in enumerate(PORTRAIT_LEVELS):
        if total >= th:
            idx = i
    cx = width / 2
    skin, shirt = "#F6C9A0", "#1565C0"
    attempted = any(scores[k] > 0 for k in ("class", "own", "area", "map", "quiz"))
    P = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    # 地面
    P.append(f'<rect x="0" y="{height - 40}" width="{width}" height="40" fill="#E8F5E9"/>')
    P.append(f'<text x="{cx}" y="{height - 14}" font-size="12" fill="#66BB6A" text-anchor="middle">宗地 · 我的学习园地</text>')
    # 腿与鞋
    P.append(f'<rect x="{cx - 34}" y="296" width="26" height="40" fill="#455A64"/>')
    P.append(f'<rect x="{cx + 8}" y="296" width="26" height="40" fill="#455A64"/>')
    P.append(f'<ellipse cx="{cx - 22}" cy="336" rx="19" ry="10" fill="#37474F"/>')
    P.append(f'<ellipse cx="{cx + 22}" cy="336" rx="19" ry="10" fill="#37474F"/>')
    # 身体与手臂
    P.append(f'<ellipse cx="{cx}" cy="244" rx="46" ry="68" fill="{shirt}"/>')
    P.append(f'<ellipse cx="{cx - 52}" cy="233" rx="17" ry="26" fill="{shirt}"/>')
    P.append(f'<ellipse cx="{cx + 52}" cy="233" rx="17" ry="26" fill="{shirt}"/>')
    # 装备（5档：书→图纸卷→三角板→测旗）
    if idx == 0:
        P.append(f'<rect x="{cx + 32}" y="222" width="22" height="30" rx="3" fill="#EF5350"/>')
        P.append(f'<line x1="{cx + 34}" y1="226" x2="{cx + 52}" y2="226" stroke="#FFFFFF" stroke-width="2"/>')
        P.append(f'<line x1="{cx + 34}" y1="231" x2="{cx + 52}" y2="231" stroke="#FFFFFF" stroke-width="2"/>')
        P.append(f'<line x1="{cx + 34}" y1="236" x2="{cx + 52}" y2="236" stroke="#FFFFFF" stroke-width="2"/>')
    elif idx == 1:
        P.append(f'<rect x="{cx + 26}" y="218" width="34" height="24" rx="3" fill="#FFF8E1" stroke="#F9A825" stroke-width="2"/>')
        P.append(f'<line x1="{cx + 30}" y1="222" x2="{cx + 56}" y2="222" stroke="#9E9D24" stroke-width="2"/>')
        P.append(f'<line x1="{cx + 30}" y1="227" x2="{cx + 56}" y2="227" stroke="#9E9D24" stroke-width="2"/>')
        P.append(f'<line x1="{cx + 30}" y1="232" x2="{cx + 56}" y2="232" stroke="#9E9D24" stroke-width="2"/>')
    elif idx == 2:
        P.append(f'<polygon points="{cx + 44},{218} {cx + 66},{222} {cx + 44},{226}" fill="#FF8F00" stroke="#E65100" stroke-width="1"/>')
        P.append(f'<line x1="{cx + 46}" y1="224" x2="{cx + 46}" y2="240" stroke="#5D4037" stroke-width="2"/>')
    else:
        P.append(f'<line x1="{cx + 34}" y1="246" x2="{cx + 66}" y2="246" stroke="#5D4037" stroke-width="2"/>')
        P.append(f'<polygon points="{cx + 66},{238} {cx + 78},{244} {cx + 66},{250}" fill="#EF5350" stroke="#C62828" stroke-width="1"/>')
        P.append(f'<text x="{cx + 72}" y="{244 + 4}" font-size="11" fill="#FFFFFF" text-anchor="middle">测</text>')
    # 头
    P.append(f'<ellipse cx="{cx}" cy="123" rx="48" ry="49" fill="{skin}"/>')
    # 眼睛
    P.append(f'<circle cx="{cx - 17}" cy="123" r="6" fill="#212121"/>')
    P.append(f'<circle cx="{cx + 17}" cy="123" r="6" fill="#212121"/>')
    # 腮红
    P.append(f'<ellipse cx="{cx - 28}" cy="142" rx="7" ry="6" fill="#FFCDD2"/>')
    P.append(f'<ellipse cx="{cx + 28}" cy="142" rx="7" ry="6" fill="#FFCDD2"/>')
    # 微笑
    P.append(f'<path d="M {cx - 14} 144 Q {cx} 160 {cx + 14} 144" stroke="#212121" stroke-width="2" fill="none"/>')
    # 帽子（5档：草帽→鸭舌帽→安全帽→高级盔→皇冠）
    if idx == 0:
        P.append(f'<ellipse cx="{cx}" cy="78" rx="54" ry="18" fill="#A1887F"/>')
        P.append(f'<polygon points="{cx - 20},{78} {cx + 20},{78} {cx},{34}" fill="#8D6E63"/>')
        P.append(f'<rect x="{cx - 22}" y="58" width="44" height="4" fill="#6D4C41"/>')
    elif idx == 1:
        P.append(f'<path d="M {cx - 34} 96 Q {cx - 40} 62 {cx - 6} 64 L {cx + 8} 60 L {cx + 36} 92 L {cx + 26} 94 Z" fill="#EF6C00"/>')
        P.append(f'<path d="M {cx - 6} 64 L {cx + 8} 60 L {cx + 12} 92 L {cx - 2} 92 Z" fill="#E65100"/>')
    elif idx == 2:
        P.append(f'<ellipse cx="{cx}" cy="82" rx="48" ry="24" fill="#FFCA28"/>')
        P.append(f'<ellipse cx="{cx}" cy="68" rx="40" ry="18" fill="#FFB300"/>')
        P.append(f'<line x1="{cx - 40}" y1="82" x2="{cx + 40}" y2="82" stroke="#FFF176" stroke-width="2"/>')
    elif idx == 3:
        P.append(f'<path d="M {cx - 38} 96 L {cx - 44} 70 L {cx - 14} 78 L {cx} 44 L {cx + 14} 78 L {cx + 44} 70 L {cx + 38} 96 Z" fill="#9E9E9E"/>')
        P.append(f'<rect x="{cx - 40}" y="96" width="80" height="6" rx="3" fill="#757575"/>')
        P.append(f'<line x1="{cx}" y1="44" x2="{cx}" y2="36" stroke="#FFD54F" stroke-width="3"/>')
    else:
        P.append(f'<polygon points="{cx - 42},{88} {cx - 32},{56} {cx - 14},{74} {cx},{40} {cx + 14},{74} {cx + 32},{56} {cx + 42},{88}" fill="#FFD54F" stroke="#F9A825" stroke-width="2"/>')
        P.append(f'<circle cx="{cx}" cy="{40}" r="5" fill="#E53935"/>')
        P.append(f'<circle cx="{cx - 20}" cy="52" r="4" fill="#E53935"/>')
        P.append(f'<circle cx="{cx + 20}" cy="52" r="4" fill="#E53935"/>')
    # 胸前金星（≥80分维度）
    star_x = cx - 30
    for zh, k, en in PORTRAIT_DIMS:
        if scores[k] >= 80 and star_x <= cx + 34:
            P.append(f'<text x="{star_x}" y="208" font-size="16" fill="#FFB300" text-anchor="middle">★</text>')
            star_x += 22
    # 高级及以上金徽章
    if idx >= 3:
        P.append(f'<circle cx="{cx + 36}" cy="206" r="9" fill="#FFC107" stroke="#B8860B" stroke-width="1"/>')
        P.append(f'<text x="{cx + 36}" y="{206 + 4}" font-size="10" fill="#5D4037" text-anchor="middle">金</text>')
    # 鼓励气泡（有作答记录时）
    if attempted:
        tip = "继续加油！"
        if idx >= 3:
            tip = "太棒了！"
        P.append(f'<ellipse cx="{cx + 96}" cy="58" rx="52" ry="18" fill="#FFF8E1" stroke="#F9A825" stroke-width="2"/>')
        P.append(f'<polygon points="{cx + 66},{72} {cx + 80},{88} {cx + 88},{70}" fill="#FFF8E1" stroke="#F9A825" stroke-width="2"/>')
        P.append(f'<text x="{cx + 96}" y="{58 + 4}" font-size="13" fill="#E65100" text-anchor="middle">{tip}</text>')
    # 等级名牌
    P.append(f'<rect x="{cx - 92}" y="{height - 40}" width="184" height="22" rx="6" fill="#FFF8E1" stroke="#F9A825" stroke-width="1"/>')
    P.append(f'<text x="{cx}" y="{height - 40 + 15}" font-size="13" font-weight="bold" fill="#E65100" text-anchor="middle">{lvl_zh}</text>')
    P.append(f'<text x="{cx}" y="20" font-size="13" fill="#78909C" text-anchor="middle">小小地籍调查员 / My Surveyor Portrait</text>')
    P.append('</svg>')
    return "".join(P)


# ============================================================
# 内联 SVG 宗地图（浏览器端渲染中文，无服务器字体依赖）
# ============================================================
def svg_parcel_area(pts, pname, width=440, height=380):
    """面积计算实训：按坐标点绘制宗地多边形 + 网格轴刻度（内联 SVG）"""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    xr = (xmax - xmin) or 1.0
    yr = (ymax - ymin) or 1.0
    pad_x, pad_y = xr * 0.15, yr * 0.18
    plot_x, plot_y = 52, 58                       # 绘图区左上角
    plot_w = width - plot_x - 30
    plot_h = height - plot_y - 62
    scale = min(plot_w / (xr + 2 * pad_x), plot_h / (yr + 2 * pad_y))
    def px(v): return plot_x + (v - (xmin - pad_x)) * scale
    def py(v): return plot_y + ((ymax + pad_y) - v) * scale

    # 刻度步长
    xstep = 10 ** math.floor(math.log10((xr / 5) or 1))
    while xr / xstep > 5: xstep *= 2
    while xr / xstep < 2: xstep /= 2
    ystep = 10 ** math.floor(math.log10((yr / 5) or 1))
    while yr / ystep > 5: ystep *= 2
    while yr / ystep < 2: ystep /= 2

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    parts.append(f'<text x="{width/2}" y="24" font-size="15" font-weight="bold" fill="#1B5E20" text-anchor="middle">{pname}</text>')
    # 网格线与 X 轴刻度
    for v in range(int(math.ceil((xmin - pad_x) / xstep)) * xstep, int(xmax + pad_x) + 1, int(xstep)):
        if v < xmin - pad_x or v > xmax + pad_x: continue
        parts.append(f'<line x1="{px(v):.1f}" y1="{py(ymin-pad_y):.1f}" x2="{px(v):.1f}" y2="{py(ymax+pad_y):.1f}" stroke="#EEEEEE" stroke-width="1"/>')
        parts.append(f'<text x="{px(v):.1f}" y="{py(ymin-pad_y)+15:.1f}" font-size="10" fill="#666" text-anchor="middle">{v:g}</text>')
    # Y 轴刻度
    for v in range(int(math.ceil((ymin - pad_y) / ystep)) * ystep, int(ymax + pad_y) + 1, int(ystep)):
        if v < ymin - pad_y or v > ymax + pad_y: continue
        parts.append(f'<line x1="{px(xmin-pad_x):.1f}" y1="{py(v):.1f}" x2="{px(xmax+pad_x):.1f}" y2="{py(v):.1f}" stroke="#EEEEEE" stroke-width="1"/>')
        parts.append(f'<text x="{px(xmin-pad_x)-6:.1f}" y="{py(v)+4:.1f}" font-size="10" fill="#666" text-anchor="end">{v:g}</text>')
    # 坐标轴框
    parts.append(f'<rect x="{px(xmin-pad_x):.1f}" y="{py(ymax+pad_y):.1f}" width="{(xr+2*pad_x)*scale:.1f}" height="{(yr+2*pad_y)*scale:.1f}" fill="none" stroke="#BDBDBD" stroke-width="1"/>')
    # 宗地多边形（自动闭合）
    poly = " ".join(f"{px(p[0]):.1f},{py(p[1]):.1f}" for p in pts) + f" {px(pts[0][0]):.1f},{py(pts[0][1]):.1f}"
    parts.append(f'<polygon points="{poly}" fill="#A5D6A7" fill-opacity="0.45" stroke="#2E7D32" stroke-width="2"/>')
    # 顶点标注
    for i, (x, y) in enumerate(pts):
        parts.append(f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="4" fill="#1B5E20"/>')
        parts.append(f'<text x="{px(x)+8:.1f}" y="{py(y)-5:.1f}" font-size="11" font-weight="bold" fill="#1B5E20">P{i}</text>')
    parts.append(f'<text x="{plot_x+plot_w/2:.1f}" y="{height-9}" font-size="12" fill="#444" text-anchor="middle">X (m)</text>')
    parts.append(f'<text x="15" y="{plot_y+plot_h/2:.1f}" font-size="12" fill="#444" text-anchor="middle" transform="rotate(-90 15 {plot_y+plot_h/2:.1f})">Y (m)</text>')
    parts.append('</svg>')
    return "".join(parts)


def svg_parcel_card(parcel_id, holder, cls2, area, width=440, height=400):
    """宗地图示例：示意多边形 + 中文标注 + 北箭头（内联 SVG）"""
    xs = [0, 100, 120, 30, 0]
    ys = [0, 0, 80, 100, 0]
    plot_x, plot_y, plot_w, plot_h = 45, 60, width - 85, height - 120
    scale = min(plot_w / 130, plot_h / 110)
    def px(v): return plot_x + v * scale
    def py(v): return plot_y + (100 - v) * scale

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    parts.append(f'<text x="{width/2}" y="24" font-size="15" font-weight="bold" fill="#37474F" text-anchor="middle">宗地图 / Parcel Map</text>')
    poly = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in zip(xs, ys))
    parts.append(f'<polygon points="{poly}" fill="#C5E1A5" fill-opacity="0.5" stroke="#33691E" stroke-width="2"/>')
    for txt, yy in [(f"宗地号: {parcel_id}", 92), (f"权利人: {holder}", 84),
                    (f"地类: {cls2}", 76), (f"面积: {area:.0f} ㎡", 68)]:
        parts.append(f'<text x="{plot_x + 62 * scale:.1f}" y="{py(yy):.1f}" font-size="12" fill="#1B5E20" text-anchor="middle">{txt}</text>')
    # 北箭头
    ax_x = plot_x + 105 * scale
    parts.append(f'<line x1="{ax_x:.1f}" y1="{py(78):.1f}" x2="{ax_x:.1f}" y2="{py(94):.1f}" stroke="#D32F2F" stroke-width="2"/>')
    parts.append(f'<polygon points="{ax_x-5:.1f},{py(94):.1f} {ax_x+5:.1f},{py(94):.1f} {ax_x:.1f},{py(88):.1f}" fill="#D32F2F"/>')
    parts.append(f'<text x="{ax_x:.1f}" y="{py(98):.1f}" font-size="13" font-weight="bold" fill="#D32F2F" text-anchor="middle">北</text>')
    parts.append('</svg>')
    return "".join(parts)


def send_report_email(subject, body):
    """通过 Resend HTTP API 将学习报告发送到老师邮箱（绕过Streamlit SMTP端口限制）"""
    try:
        import requests
        api_key = st.secrets["resend"]["api_key"]
        teacher_email = st.secrets["resend"].get("to_email", "39116272@qq.com")
        from_email = st.secrets["resend"].get("from_email", "onboarding@resend.dev")
        
        resp = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "from": from_email,
                "to": [teacher_email],
                "subject": subject,
                "text": body
            },
            timeout=30
        )
        if resp.status_code in (200, 201):
            return True, ""
        else:
            return False, f"HTTP {resp.status_code}: {resp.text}"
    except Exception as e:
        return False, str(e)


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
    st.session_state.start_time = datetime.datetime.now()
    # 生成唯一防伪码
    import hashlib, secrets
    raw = f"{st.session_state.student_name}{st.session_state.student_id}{datetime.datetime.now()}{secrets.token_hex(8)}"
    code = hashlib.sha256(raw.encode()).hexdigest().upper()[:16]
    st.session_state.verify_code = f"DJGL-{code[:4]}-{code[4:8]}-{code[8:12]}-{code[12:16]}"

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
              "📚 在线刷题", "🧑🎓 学生能力画像", "📊 学习统计与提交", "ℹ️ 使用说明"]
modules_en = ["📖 Knowledge", "🌾 Land Classification", "⚖️ Ownership", "📐 Area Calculation",
              "🔢 Survey Procedure", "🔍 Parcel Search", "🗺️ Parcel Map Quiz", "📝 Final Quiz",
              "📚 Question Bank", "🧑🎓 Ability Portrait", "📊 My Scores & Report", "ℹ️ Help"]
modules = modules_zh if st.session_state.lang == "zh" else modules_en
module = st.sidebar.radio(t("功能模块", "Modules"), modules)

st.sidebar.markdown("---")
st.sidebar.caption("V2.5 Web版 · 含学生能力画像")

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
    mode_labels = [
        t("模式A：判断二级地类属于哪个一级类", "Mode A: which first-level class?"),
        t("模式B：选出属于某一级类的二级地类", "Mode B: pick second-level class"),
    ]
    mode_idx = st.radio(t("练习模式", "Mode"), range(len(mode_labels)),
                        format_func=lambda i: mode_labels[i])
    # 切换模式时清掉另一个模式的旧题目状态，保证切过去立刻出新题
    if st.session_state.get("_last_mode_idx", None) != mode_idx:
        st.session_state.pop("class_idx", None)
        st.session_state.pop("class_b_idx", None)
        st.session_state.pop("class_b_opts", None)
        st.session_state._last_mode_idx = mode_idx
    if mode_idx == 0:
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
        # 模式B：给出一个一级类，从4个二级类里选出正确的那个
        if 'class_b_idx' not in st.session_state or 'class_b_opts' not in st.session_state or st.button(t("换一题", "Next Question")):
            st.session_state.class_b_idx = random.randrange(len(CLASS_PRACTICE))
            # 生成固定选项，存在session里，不会每次点单选就变
            idx = st.session_state.class_b_idx
            # 干扰项必须从"不属于目标一级类"的二级类中抽取，
            # 否则同一级类下的其他二级类（如河流水面/坑塘水面/沟渠同属水域及水利设施用地）
            # 会被误抽成干扰项，导致一题中有多个正确答案。
            correct_first = CLASS_PRACTICE[idx][1]
            wrong_pool = [i for i in range(len(CLASS_PRACTICE)) if CLASS_PRACTICE[i][1] != correct_first]
            wrong = random.sample(wrong_pool, 3)
            all_opts = [idx] + wrong
            random.shuffle(all_opts)
            st.session_state.class_b_opts = all_opts
        idx = st.session_state.class_b_idx
        all_opts = st.session_state.class_b_opts
        correct_sub, correct_first, code = CLASS_PRACTICE[idx]
        correct_sub_en = ["Paddy field","Irrigated land","Dry land","Orchard","Tea plantation",
                  "Arbor forest","Bamboo forest","Natural pasture","Other grassland",
                  "Retail commercial","Catering","Hotel","Industrial","Warehousing","Mining",
                  "Urban residential","Rural homestead","Education","Medical","Parks & green",
                  "Military","Religious","Funeral","Railway","Highway","Rural road",
                  "River","Reservoir","Canal","Pond","Idle","Agri-facility","Sandy","Bare","Field ridge"][idx]
        opt_labels = []
        for i in all_opts:
            sub, first, _ = CLASS_PRACTICE[i]
            sub_en = ["Paddy field","Irrigated land","Dry land","Orchard","Tea plantation",
                  "Arbor forest","Bamboo forest","Natural pasture","Other grassland",
                  "Retail commercial","Catering","Hotel","Industrial","Warehousing","Mining",
                  "Urban residential","Rural homestead","Education","Medical","Parks & green",
                  "Military","Religious","Funeral","Railway","Highway","Rural road",
                  "River","Reservoir","Canal","Pond","Idle","Agri-facility","Sandy","Bare","Field ridge"][i]
            opt_labels.append(f"{sub} / {sub_en}")
        st.markdown(f"**{t('下列哪个二级地类属于', 'Which second-level class belongs to')} “{correct_first} / {FIRST_CLASSES_EN[FIRST_CLASSES.index(correct_first)]}”？**")
        chosen = st.radio("", opt_labels, key="class_b_opt")
        if st.button(t("提交答案", "Submit")):
            st.session_state.class_total += 1
            chosen_idx = all_opts[opt_labels.index(chosen)]
            if chosen_idx == idx:
                st.success(f"✅ {t('正确！', 'Correct!')} {correct_sub} / {correct_sub_en} {t('属于', 'belongs to')} {correct_first}")
                st.session_state.class_score += 1
                st.balloons()
                if random.random() < 0.5: mascot_say()
            else:
                st.error(f"❌ {t('错误。正确答案', 'Wrong. Correct answer')}：{correct_sub} / {correct_sub_en}")
            p = os.path.join(IMG_DIR, CLASS_IMAGES[idx])
            if os.path.exists(p): st.image(p, caption=f"{correct_sub} / {correct_sub_en}", width=300)
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
    choice = st.radio("", [t("国家所有（国有）", "State-owned"), t("集体所有", "Collectively-owned")], key="own_choice")
    if st.button(t("提交判断", "Submit")):
        st.session_state.own_total += 1
        correct = "国有" if choice.startswith(t("国家", "State-owned")) else "集体"
        # 上面的startswith在双语模式下可能匹配不上，直接判断是否包含国有/State
        if "国有" in choice or "State-owned" in choice:
            correct = "国有"
        else:
            correct = "集体"
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
    c1, c2 = st.columns([1, 1])
    with c1:
        st.dataframe(df_pts, use_container_width=True)
    with c2:
        # 自动画宗地图（内联 SVG，浏览器渲染中文，无服务器字体依赖）
        st.markdown(svg_parcel_area(pts, pname), unsafe_allow_html=True)
    st.caption(t("提示：使用鞋带公式 S = ½|Σ(xᵢyᵢ₊₁ − xᵢ₊₁yᵢ)|", "Hint: Use shoelace formula S = ½|Σ(xi·yi+1 − xi+1·yi)|"))
    user_area = st.number_input(t("请输入你计算的宗地面积（平方米）", "Enter your calculated area (m²)"),
                                min_value=0.0, step=1.0, format="%.2f")
    c1, c2 = st.columns(2)
    with c1:
        if st.button(t("提交答案", "Submit")):
            correct = shoelace(pts)
            st.session_state.area_total += 1
            if abs(user_area - correct) < 0.5:
                st.success(f"✅ {t('计算正确！面积', 'Correct! Area')} = {correct:.2f} ㎡ ≈ {mu_area(correct):.2f} {t('亩', 'mu')}")
                st.session_state.area_score += 1
                if random.random() < 0.5: mascot_say()
            else:
                st.error(f"❌ {t('计算有误。正确答案', 'Wrong. Correct answer')}：{correct:.2f} ㎡ ≈ {mu_area(correct):.2f} {t('亩', 'mu')}")
    with c2:
        if st.button(t("👀 查看参考答案", "👀 View Answer")):
            correct = shoelace(pts)
            # 计算鞋带公式的详细步骤
            s1 = sum(pts[i][0] * pts[(i+1) % len(pts)][1] for i in range(len(pts)))
            s2 = sum(pts[i][1] * pts[(i+1) % len(pts)][0] for i in range(len(pts)))
            st.info(f"📝 {t('参考答案', 'Reference Answer')}：\n"
                    f"Σ(xᵢyᵢ₊₁) = {s1:.2f}\n"
                    f"Σ(yᵢxᵢ₊₁) = {s2:.2f}\n"
                    f"S = ½|{s1:.2f} - {s2:.2f}| = {correct:.2f} ㎡\n"
                    f"≈ {mu_area(correct):.2f} 亩")
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
                if user_order[i] == i:
                    st.markdown(f"{i+1}. <span style='color:red;font-weight:bold;'>✅ {name}</span> —— {desc}", unsafe_allow_html=True)
                else:
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

    # 选择要查看详情的宗地
    if len(filtered) > 0:
        parcel_ids = filtered["宗地号"].tolist()
        selected_id = st.selectbox(t("选择要查看详情的宗地", "Select a parcel to view details"), parcel_ids)
        selected = filtered[filtered["宗地号"] == selected_id].iloc[0]

        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader(t("宗地详情", "Parcel Details"))
            st.write(f"**{t('宗地号', 'Parcel No.')}：** {selected['宗地号']}")
            st.write(f"**{t('坐落', 'Location')}：** {selected['坐落']}")
            st.write(f"**{t('权利人', 'Right Holder')}：** {selected['权利人']}")
            st.write(f"**{t('权属性质', 'Ownership')}：** {selected['权属性质']}")
            st.write(f"**{t('地类', 'Land Class')}：** {selected['一级类']} - {selected['二级类']}")
            st.write(f"**{t('面积', 'Area')}：** {selected['面积平方米']:.2f} ㎡ ≈ {selected['面积平方米']/666.67:.2f} 亩")
            st.write(f"**{t('登记类型', 'Registration')}：** {selected['登记类型']}")
        with c2:
            st.subheader(t("宗地图示例", "Parcel Map"))
            # 动态画宗地图，显示当前选中的宗地信息
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(5, 4))
            # 画一个示意多边形
            xs = [0, 100, 120, 30, 0]
            ys = [0, 0, 80, 100, 0]
            ax.fill(xs, ys, alpha=0.3, color='#8BC34A')
            ax.plot(xs, ys, 'k-', linewidth=2)
            ax.text(50, 95, "宗 地 图", ha='center', fontsize=16, fontweight='bold')
            ax.text(50, 85, f"宗地号: {selected['宗地号']}", ha='center', fontsize=10)
            ax.text(50, 75, f"权利人: {selected['权利人']}", ha='center', fontsize=10)
            ax.text(50, 65, f"地类: {selected['二级类']}", ha='center', fontsize=10)
            ax.text(50, 55, f"面积: {selected['面积平方米']:.0f} ㎡", ha='center', fontsize=10)
            ax.annotate('北', xy=(110, 90), fontsize=14, color='red')
            ax.arrow(110, 70, 0, 15, head_width=5, head_length=5, fc='red', ec='red')
            ax.set_xlim(-10, 130)
            ax.set_ylim(-10, 110)
            ax.axis('off')
            st.pyplot(fig, use_container_width=True)

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
# 模块8.6：在线刷题（历年真题题库，中英对照）
# ============================================================
elif module.startswith("📚"):
    st.header(t("📚 在线刷题 · 历年真题库", "📚 Question Bank · Past Exams"))

    # 加载题库
    qbank_path = os.path.join(BASE_DIR, "questions.json")
    if not os.path.exists(qbank_path):
        st.warning(t("题库文件 questions.json 不存在", "questions.json not found"))
    else:
        import json as _json
        with open(qbank_path, "r", encoding="utf-8") as f:
            QBANK = _json.load(f)

        # 题型中文/英文映射
        type_map = {
            "glossary":  ("名词解释", "Glossary"),
            "single":    ("单选题", "Single Choice"),
            "multiple":  ("多选题", "Multiple Choice"),
            "fill":      ("填空题", "Fill in the Blank"),
            "short":     ("简答题", "Short Answer"),
            "essay":     ("论述题", "Essay"),
        }
        type_zh_list = [v[0] for v in type_map.values()]
        type_en_list = [v[1] for v in type_map.values()]

        # 统计
        type_counts = {}
        for q in QBANK:
            type_counts[q["type"]] = type_counts.get(q["type"], 0) + 1
        st.caption(t(f"题库共 {len(QBANK)} 题：" +
                     " / ".join(f"{type_map[k][0]}{v}" for k, v in type_counts.items()),
                     f"Total {len(QBANK)} questions: " +
                     " / ".join(f"{type_map[k][1]}: {v}" for k, v in type_counts.items())))

        # 选择题型
        if st.session_state.lang == "zh":
            chosen_type_zh = st.selectbox(t("选择题型", "Select Question Type"), type_zh_list)
            chosen_type = [k for k, v in type_map.items() if v[0] == chosen_type_zh][0]
        else:
            chosen_type_en = st.selectbox(t("选择题型", "Select Question Type"), type_en_list)
            chosen_type = [k for k, v in type_map.items() if v[1] == chosen_type_en][0]

        # 筛选该题型的题目
        pool = [q for q in QBANK if q["type"] == chosen_type]
        if not pool:
            st.info(t("该题型暂无题目", "No questions in this type yet"))
        else:
            # 初始化/换题
            if "qb_idx" not in st.session_state or st.session_state.get("qb_type") != chosen_type:
                st.session_state.qb_idx = random.randrange(len(pool))
                st.session_state.qb_type = chosen_type
                st.session_state.qb_revealed = False
                st.session_state.qb_user_ans = None

            q = pool[st.session_state.qb_idx]

            # 题目展示（中英对照）
            st.subheader(f"{t('题目', 'Question')} {st.session_state.qb_idx + 1} / {len(pool)}")

            if st.session_state.lang == "zh":
                st.markdown(f"**🇨🇳 {q.get('q_zh','')}**")
                st.markdown(f"🇬🇧 {q['q_en']}")
            else:
                st.markdown(f"**🇬🇧 {q['q_en']}**")
                if q.get('q_zh'):
                    st.caption(f"🇨🇳 {q['q_zh']}")

            st.markdown("---")

            # 作答区
            if chosen_type in ("single", "multiple"):
                opts = q.get("options", {})
                opt_labels = [f"{k}. {v}" for k, v in opts.items()]
                if chosen_type == "single":
                    user_choice = st.radio(t("你的选择", "Your answer"),
                                           opt_labels, key=f"qb_opt_{st.session_state.qb_idx}",
                                           index=None)
                    if user_choice:
                        st.session_state.qb_user_ans = user_choice.split(".")[0]
                else:
                    chosen = st.multiselect(t("你的选择（多选）", "Your answer (multiple)"),
                                             opt_labels, key=f"qb_multi_{st.session_state.qb_idx}")
                    st.session_state.qb_user_ans = "".join(sorted(c.split(".")[0] for c in chosen))
            elif chosen_type == "fill":
                st.text_input(t("你的答案", "Your answer"),
                              key=f"qb_fill_{st.session_state.qb_idx}",
                              on_change=lambda: setattr(st.session_state, "qb_user_ans",
                                st.session_state.get(f"qb_fill_{st.session_state.qb_idx}", "")))
            elif chosen_type in ("glossary", "short", "essay"):
                st.text_area(t("你的作答（写完点查看答案对照）", "Your answer (click reveal to compare)"),
                             key=f"qb_text_{st.session_state.qb_idx}", height=120)

            st.markdown("---")

            # 按钮区
            c1, c2 = st.columns(2)
            with c1:
                if st.button(t("🔍 查看答案", "🔍 Reveal Answer"), type="primary"):
                    st.session_state.qb_revealed = True
            with c2:
                if st.button(t("➡️ 下一题", "➡️ Next Question")):
                    st.session_state.qb_idx = random.randrange(len(pool))
                    st.session_state.qb_revealed = False
                    st.session_state.qb_user_ans = None
                    st.rerun()

            # 答案展示
            if st.session_state.qb_revealed:
                st.markdown("### ✅ " + t("参考答案", "Reference Answer"))
                if chosen_type in ("single", "multiple"):
                    st.success(f"{t('正确答案', 'Correct answer')}：{q['answer']}")
                    # 自动判分
                    ua = st.session_state.qb_user_ans or ""
                    if chosen_type == "single":
                        if ua == q["answer"]:
                            st.balloons(); st.success(t("✅ 回答正确！", "✅ Correct!"))
                        elif ua:
                            st.error(t(f"❌ 你的答案：{ua}", f"❌ Your answer: {ua}"))
                    else:
                        ua_sorted = "".join(sorted(ua))
                        ca_sorted = "".join(sorted(q["answer"]))
                        if ua_sorted == ca_sorted:
                            st.balloons(); st.success(t("✅ 全对！", "✅ All correct!"))
                        elif ua:
                            st.warning(t(f"你选了：{ua}（正确：{q['answer']}）",
                                         f"Your choice: {ua} (correct: {q['answer']})"))
                else:
                    if st.session_state.lang == "zh":
                        st.info(f"🇨🇳 {q.get('answer_zh','')}")
                        if q.get('answer_en'):
                            st.caption(f"🇬🇧 {q['answer_en']}")
                    else:
                        st.info(f"🇬🇧 {q.get('answer_en','')}")
                        if q.get('answer_zh'):
                            st.caption(f"🇨🇳 {q['answer_zh']}")

# ============================================================
# 模块8.5：学生能力画像（文字画像 + 能力雷达图 + 卡通画像）
# ============================================================
elif module.startswith("🧑🎓"):
    st.header(t("🧑🎓 学生能力画像", "🧑🎓 Ability Portrait"))
    scores = portrait_scores_from(st.session_state)
    total = portrait_total(scores)
    lvl_zh, lvl_en = portrait_level_from(total)
    st.progress(min(100, int(total)))
    st.caption(f"综合得分 **{total:.0f}** 分　|　{t('能力等级', 'Rank')} **{lvl_zh} / {lvl_en}**")

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(svg_radar(scores), unsafe_allow_html=True)
    with c2:
        st.markdown(svg_avatar(scores, total, lvl_zh), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"**{t('六维能力值', 'Six Dimension Scores')}**")
    for zh, k, en in PORTRAIT_DIMS:
        v = scores[k]
        stars = "★" * (v // 20) + "☆" * (5 - v // 20)
        st.markdown(f"- {zh} / {en}：**{v}** 分　{stars}")

    # 学习投入标签
    elapsed = datetime.datetime.now() - st.session_state.start_time
    mins = int(elapsed.total_seconds() // 60)
    total_answered = (st.session_state.class_total + st.session_state.own_total
                      + st.session_state.area_total + st.session_state.map_total)
    tags = []
    if mins >= 60:
        tags.append(t("勤奋专注", "Dedicated"))
    if total_answered >= 20:
        tags.append(t("练习充分", "Practice-oriented"))
    if tags:
        st.markdown(f"**{t('学习投入', 'Learning Input')}：**" + "、".join(tags) + "。")

    st.markdown("---")
    st.markdown(f"**{t('文字画像', 'Portrait Description')}**")
    for ln in portrait_summary_lines(scores, total):
        st.markdown("- " + ln)

    adv = portrait_advice_lines(scores)
    if adv:
        st.markdown(f"**{t('成长建议', 'Growth Advice')}**")
        for a in adv:
            st.markdown("- " + a)

    # 晋升提示
    promoted = False
    for th, zh, en in PORTRAIT_LEVELS:
        if total < th:
            st.caption(f"🚀 {t('再提升', 'Gain another')} **{th - total:.0f}** {t('分即可晋升为', 'points to become')}「{zh} / {en}」！")
            promoted = True
            break
    if not promoted:
        st.caption("🏆 " + t("已达到最高等级「首席调查员 / Chief Surveyor」，实至名归！", "You reached the top rank: Chief Surveyor!"))

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

    # 在线时长
    elapsed = datetime.datetime.now() - st.session_state.start_time
    minutes = int(elapsed.total_seconds() // 60)
    seconds = int(elapsed.total_seconds() % 60)
    total_answered = st.session_state.class_total + st.session_state.own_total + st.session_state.area_total + st.session_state.map_total

    c1, c2 = st.columns(2)
    with c1:
        st.metric(t("⏱️ 本次学习时长", "⏱️ Study Time"), f"{minutes}分{seconds}秒")
    with c2:
        st.metric(t("📝 累计答题数", "📝 Questions Answered"), f"{total_answered} 题")

    st.info(f"🔐 {t('本报告防伪码', 'Report Verification Code')}：**{st.session_state.verify_code}**")

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

    # 学生能力画像（与桌面版同口径：六维得分 + 5档等级 + 文字画像 + 成长建议）
    p_scores = portrait_scores_from(st.session_state)
    p_total = portrait_total(p_scores)
    p_lvl_zh, p_lvl_en = portrait_level_from(p_total)
    p_lines = portrait_summary_lines(p_scores, p_total)
    p_adv = portrait_advice_lines(p_scores)
    p_summary_txt = "；".join(p_lines[1:]) if len(p_lines) > 1 else p_lines[0]
    p_adv_txt = "；".join(p_adv) if p_adv else "各维度保持练习，持续进步。"

    # 生成报告文本
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"""地籍管理实训系统 学习报告
============================
姓名 / Name: {name}
班级 / Class: {cls}
学号 / Student ID: {sid}
学习时间 / Time: {now}
在线时长 / Duration: {minutes}分{seconds}秒
累计答题 / Total Questions: {total_answered} 题
----------------------------
综合测验 Final Quiz: {quiz_score:.1f} 分
土地分类练习 Classification: {class_pct:.1f}% ({st.session_state.class_score}/{st.session_state.class_total})
权属判断 Ownership: {own_pct:.1f}% ({st.session_state.own_score}/{st.session_state.own_total})
面积计算 Area Calc: {area_pct:.1f}% ({st.session_state.area_score}/{st.session_state.area_total})
宗地图识别 Map Quiz: {map_pct:.1f}% ({st.session_state.map_score}/{st.session_state.map_total})
流程排序 Procedure: {flow_pct:.1f}% ({st.session_state.flow_score}/8)
----------------------------
综合成绩 Overall: {total:.1f} 分
----------------------------
学生能力画像 Ability Portrait
能力等级 Rank: {p_lvl_zh} / {p_lvl_en}
分类辨析 Classification: {p_scores['class']} 分
权属判断 Ownership: {p_scores['own']} 分
面积计算 Area Calc: {p_scores['area']} 分
识图能力 Parcel Map: {p_scores['map']} 分
流程逻辑 Flow: {p_scores['flow']} 分
综合运用 Quiz: {p_scores['quiz']} 分
{p_summary_txt}
成长建议 Growth Advice: {p_adv_txt}
----------------------------
防伪码 Verify Code: {st.session_state.verify_code}
"""

    st.markdown("---")
    st.subheader(t("提交给老师", "Submit to Teacher"))

    email_subject = f"地籍管理实训报告 - {name} - {sid}"
    if st.button(t("🚀 一键提交学习报告给老师", "🚀 Submit Report to Teacher"), 
                 type="primary", use_container_width=True):
        with st.spinner(t("正在发送...", "Sending...")):
            ok, err = send_report_email(email_subject, report)
            if ok:
                st.success(t("✅ 报告已成功发送给老师！", "✅ Report sent to teacher successfully!"))
                st.balloons()
            else:
                st.error(t(f"发送失败：{err}", f"Send failed: {err}"))
                st.info(t("如果多次失败，请下载报告后手动发送至老师邮箱。", 
                          "If sending keeps failing, please download the report and send it manually."))

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
    - 🧑🎓 学生能力画像：六维雷达图 + 卡通调查员画像 + 文字画像，随成绩成长
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
    - 🧑🎓 Ability Portrait: radar chart + cartoon surveyor + text portrait, grows with your scores
    """))
