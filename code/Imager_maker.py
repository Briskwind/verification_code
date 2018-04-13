import time
import os
import random
import numpy as np
from pytesseract import pytesseract
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from conf.config import BASE_DIR

_letter_cases = "abcdefghjkmnpqrstuvwxy"

_upper_cases = _letter_cases.upper()

_numbers = ''.join(map(str, range(3, 10)))

init_chars = ''.join((_letter_cases, _upper_cases, _numbers))


def is_number(number):
    """
    判断是否是数字
    :param number:
    :return:
    """
    return 48 <= ord(str(number)) <= 57


def is_alphabet(char_):
    return 65 <= ord(str(char_)) <= 90 or 97 <= ord(str(char_)) <= 122


def is_value_name(name):
    """
    返回是否是数字或者字母
    :param name:
    :return:
    """
    if not name:
        return name

    if is_number(name) or is_alphabet(name):
        return name

    return None


def create_validate_code(code='code', size=(120, 30), mode="RGB",
                         bg_color=(255, 255, 255), fg_color=(0, 0, 255),
                         font_size=18):
    width, height = size  # 宽， 高
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    def create_lines():
        """ 绘制干扰线 """
        line_num = random.randint(*(1, 2))  # 干扰线条数

        for i in range(line_num):  # pylint: disable=unused-variable

            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        """ 绘制干扰点"""
        chance = min(100, max(0, int(2)))  # 大小限制在[0, 100]

        for w in range(width):  # pylint: disable=invalid-name

            for h in range(height):  # pylint: disable=invalid-name

                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        """ 绘制验证码字符"""
        c_chars = list(code)
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开
        file_path = os.path.join(BASE_DIR, 'font', 'FZYTK.TTF')
        font = ImageFont.truetype(file_path, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    create_lines()
    create_points()

    create_strs()
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
    return img


class Imager:
    """ 图片相关处理"""

    _letter_cases = "abcdefghjkmnpqrstuvwxy"
    _upper_cases = _letter_cases.upper()

    def init_chars(self):
        _numbers = ''.join(map(str, range(3, 10)))
        return ''.join((self._letter_cases, self._upper_cases, _numbers))

    def create_img(self, save_path):
        """
        创建验证码图片
        :param save_path:验证码保存路径
        :return:
        """
        length = 4
        chars = self.init_chars()
        code = random.sample(chars, length)
        code_img = create_validate_code(code)
        file_path = '{0}/{1}.png'.format(save_path, ''.join(code))
        code_img.save(file_path)
        return file_path, code

    def get_4_distance(self, img_path):
        """
        获取四个字母所占的宽度
        :param img_path:
        :return:
        """
        img = img_path
        pixdata = img.load()
        w, h = img.size

        x_list = []
        for x in range(0, w):
            for y in range(0, h):
                if pixdata[x, y] <= 245:
                    x_list.append(x)
                    continue

        return list(set(x_list))

    def find_distance(self, num_list):
        """
        找到4个字母的间距
        :param num_list:
        :return:
        """
        start = num_list[0]
        tem_list = []

        for index, num in enumerate(num_list):
            try:
                if num_list[index + 1] - num_list[index] != 1:
                    if (num - start) != 1:
                        tem = {'start': start, 'end': num}
                        tem_list.append(tem)
                        start = num_list[index + 1]
            except IndexError:
                pass
        if (num_list[-1] - start) != 1:
            tem = {
                'start': start,
                'end': num_list[-1]
            }
            tem_list.append(tem)
        return tem_list

    def cut_one(self, bw_pic, x1, y1, x2, y2):
        """
        裁剪一张图片
        :param bw_pic:
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return:
        """
        im = bw_pic
        crop_img = im.crop((x1, y1, x2, y2))
        return crop_img

    def cutting_pic_update(self, img_path):
        """
        精确切割图片
        :param img_path:
        :return:
        """
        img_obj = Image.open(img_path)
        img_obj = self.whitening(img_obj)
        num_list = self.get_4_distance(img_obj)

        disance_list = self.find_distance(num_list)
        small_pics_obj = []
        for dis in disance_list:
            time.sleep(0.01)
            x1, y1, x2, y2 = int(dis['start']) - 1, 0, int(dis['end']) + 2, 30
            crop_img_obj = self.cut_one(img_obj, x1, y1, x2, y2)
            small_pics_obj.append(crop_img_obj)
        return small_pics_obj

    def whitening(self, img_obj):
        """
        去除干扰
        :param open_img: image obj
        :return:
        """
        img_obj = img_obj.convert('L')
        pixdata = img_obj.load()
        w, h = img_obj.size
        for y in range(0, h):
            for x in range(0, w):
                if pixdata[x, y] == 0:
                    pixdata[x, y] = 255
        return img_obj

    def cutting_pic(self, img_path):
        """
        切割图片
        :param img_path: 图片路径
        :return:
        """
        img_obj = Image.open(img_path)

        windows, start_x, end_x, start_y, end_y = 15, 20, 80, 0, 30
        img_obj = self.whitening(img_obj)
        crop_img = img_obj.crop((start_x, start_y, end_x, end_y))
        small_img_objs = []
        for j in range(4):
            small_img_obj = crop_img.crop((windows * j, start_y, windows * (j + 1), end_y))
            small_img_objs.append(small_img_obj)

        return small_img_objs

    def read_small_and_save(self, img_path, single_pic_doc, only_save=False):
        """
        识别小图片并且保存
        :param img_path: 图片路径
        :param single_pic_doc: 单个文件进行保存的路径
        :return:
        """
        # 旧的切割图片方式
        # small_pics = self.cutting_pic(img_path)

        small_img_objs = self.cutting_pic_update(img_path)
        if only_save:
            name_list = []
            for small_img_obj in small_img_objs:
                time.sleep(0.1)
                single_pic_path = '{0}/{1}.png'.format(single_pic_doc, int(time.time() * 10))
                resized = small_img_obj.resize((20, 30), Image.ANTIALIAS)
                resized.save(single_pic_path)
                name_list.append(single_pic_path)
            return name_list

        else:
            for small_img_obj in small_img_objs:
                text = pytesseract.image_to_string(small_img_obj, config='-psm 10')
                if not is_value_name(text):
                    text = 'temp'
                small_img_path = '{0}/{1}_{2}.png'.format(single_pic_doc, int(time.time() * 10), ''.join(text))
                resized = small_img_obj.resize((20, 30), Image.ANTIALIAS)
                resized.save(small_img_path)
                print("单个图识别结果：", text)

    def get_binary_pix(self, img_path):
        """
        将图片转换成 0 1 二进制，作为特征值
        :param img_path: 图片路径
        :return:
        """

        img_obj = Image.open(img_path)
        img_array = np.array(img_obj)
        rows, cols = img_array.shape
        for i in range(rows):
            for j in range(cols):
                if img_array[i, j] <= 128:
                    img_array[i, j] = 0
                else:
                    img_array[i, j] = 1
        return np.ravel(img_array)
