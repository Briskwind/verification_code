import os
import shutil

from code.Imager_maker import Imager


class Preparer:
    """
    训练之前的一些准备工作
        1、创建分类文件夹
        2、图片分类
        3、将图片特征值写入文件
    """

    def get_doc_list(self, single_pic_path):
        """
        获取分类文件夹
        :param single_pic_path: 单个图片保存路径
        :return:
        """

        name_list = []
        for root, dirs, files in os.walk(single_pic_path):
            for file_name in files:
                tem = file_name.split('.')
                doc_name = tem[0].split('_')[1]
                if doc_name not in name_list:
                    name_list.append(doc_name)
        return name_list

    def make_doc(self, doc_list, base_path):
        """
        在指定路径下创建文件夹
        :param doc_list:  文件夹列表
        :param base_path: 指定路径
        :return:
        """

        for name in doc_list:
            doc_path = os.path.join(base_path, name)
            if not os.path.exists(doc_path):
                os.makedirs(doc_path)

    def sort_pic(self, single_pic_path, base_sort_path):
        """
        对单个图片进行初步分类
        :param single_pic_path:
        :param base_sort_path:
        :return:
        """

        for root, dirs, files in os.walk(single_pic_path):
            for file_name in files:
                tem = file_name.split('.')
                doc_name = tem[0].split('_')[1]

                file_doc = os.path.join(base_sort_path, doc_name)

                shutil.move(os.path.join(single_pic_path, file_name), file_doc)

    def write_content(self, data, content_file_path):
        """
        将特征值写入文件
        :param data: 特征值
        :param content_file_path: 特征值文件
        :return:
        """
        with open(content_file_path, 'a+') as f:
            f.write(data)
            f.write('\n')

    def make_content_text(self, sort_doc_path, content_file):
        """
        将图片特征值写入文件
        :param sort_doc_path: 图片分类列表
        :param content_file: 特征值文件
        :return:
        """
        m = Imager()
        for doc in os.listdir(sort_doc_path):
            if doc == '.DS_Store':
                continue

            doc_path = os.path.join(sort_doc_path, doc)
            for file in os.listdir(doc_path):
                if file == '.DS_Store':
                    continue

                if doc != 'temp':
                    file_path = os.path.join(sort_doc_path, doc, file)
                    data = m.get_binary_pix(file_path)
                    data_list = data.tolist()

                    # 将字符转为ascii 放置最后一位，之后用于校验
                    data_list.append(ord(str(doc)))
                    str_data = [str(x) for x in data_list]
                    w_data = ','.join(str_data)
                    self.write_content(w_data, content_file)
