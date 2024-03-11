import streamlit as st
from PIL import Image
import requests
import io
from io import BytesIO
from PIL import ImageDraw
from PIL import ImageFont

# 标题
st.markdown("<h1 style='text-align: center;'>图像字幕生成系统</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>合肥工业大学 巫佳聪</h6>", unsafe_allow_html=True)

# URL输入框
url_input = st.text_input("请输入图片URL，并按回车键确认:")
if (url_input != "") and (url_input != None):
    response = requests.get(url_input)
    image = Image.open(BytesIO(response.content))
    st.image(image, caption='图片上传成功！')

# 检查图片格式函数
def check_image_format(image):
    try:
        img = Image.open(io.BytesIO(image))
        img.verify()
        return True
    except Exception as e:
        return False

# 导入本地图片按钮
uploaded_file = st.file_uploader("或者，您可以点击右侧按钮导入本地图片:", type=["jp", "jpeg", "png"])

if uploaded_file is not None:
    # 使用本地上传的图片
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption='图片上传成功！')
    except:
        st.error("图片上传失败，请上传有效的图片格式！")

# 显示测试用的默认字幕
default_captions = ["正在投出棒球的男人", "穿着棒球服的男人在球场上", "一个带着鸭舌帽男人在投球"]
# 默认字体列表
default_fonts = {"黑体": "simhei.ttf", "微软雅黑": "msyhbd.ttc","楷体": "simkai.ttf","新宋体": "simsun.ttc"}

# 导入图片后执行
if 'image' in locals():
    chosen_caption = st.selectbox("请选择一条图片字幕以嵌入到图片中：", options=default_captions)
    chosen_font = st.selectbox("选择字体:", options=default_fonts)
    chosen_font_path = default_fonts[chosen_font]
    # 字体样式选项
    font_size = st.slider("选择字体大小:", min_value=10, max_value=50, step=2, value=25)
    font_color = st.color_picker("选择字体颜色:", "#000000")

# 定义生成图片字幕的函数
def generate_captioned_image(image, caption, font_size, font_color):
    draw = ImageDraw.Draw(image)  # 创建图像绘制对象
    font = ImageFont.truetype(chosen_font_path, font_size)  # 指定字体和大小，使用 Arial 字体

    # 设置字体样式，将十六进制颜色值转换为 RGB 元组
    font_color = tuple(int(font_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))

    # 在图片下方添加字幕
    text_width, text_height = draw.textsize(caption, font=font)  # 获取字幕文本的宽度和高度
    image_width, image_height = image.size  # 获取图片的宽度和高度

    # 计算字幕文本的位置，使其位于图片中心的下方
    text_position = ((image_width - text_width) // 2, image_height - text_height - 10)

    # 绘制字幕文本
    draw.text(text_position, caption, font=font, fill=font_color)

# 显示选取按钮和字幕编辑选单
if 'image' in locals() and 'chosen_caption' in locals():
    if st.button("将选中的图像字幕嵌入图像"):
        st.empty()  # 清空输出
        generate_captioned_image(image, chosen_caption, font_size, font_color)
        st.image(image, caption='已更新为嵌入图像字幕后的图像！')
