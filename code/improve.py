import os
import shutil

from conf.config import BASE_DIR


class Improver:
    """ 初步训练之后进行提升正确率"""

    def __init__(self, imger, propheter, preparer, plk_file):
        self.imger = imger
        self.propheter = propheter
        self.preparer = preparer
        self.plk_file = plk_file

        self.predict_path = os.path.join(BASE_DIR, 'verification_pic', 'predict')
        self.single_pic_doc = os.path.join(BASE_DIR, 'verification_pic', 'predict_single')
        self.predict_sort = os.path.join(BASE_DIR, 'verification_pic', 'predict_sort')
        self.sort_path = os.path.join(BASE_DIR, 'verification_pic', 'sort')

        self.doc_list = []

    def create_pre_single_code(self, count):
        """
        生成 count 张待预测的图片
        :param count:
        :return:
        """
        for i in range(count):
            new_img_path, code = self.imger.create_img(self.predict_path)
            self.imger.read_small_and_save(new_img_path, self.single_pic_doc, only_save=True)

    def predict_and_get_doc_list(self):
        """
        识别图片并且创建分类文件夹
        :return:
        """
        self.propheter.get_propheter(self.plk_file)

        for file_name in os.listdir(self.single_pic_doc):
            file_path = os.path.join(self.single_pic_doc, file_name)
            binary_pix_img = self.imger.get_binary_pix(file_path)
            singoe_code = self.propheter.predict_pic(binary_pix_img)
            self.make_doc_and_mv(singoe_code, file_path)

    def make_doc_and_mv(self, singoe_code, file_path):
        """
        创建分类文件夹并且对文件进行分类
        :param singoe_code:
        :param file_path:
        :return:
        """
        doc_path = os.path.join(self.predict_sort, singoe_code)

        if not os.path.exists(doc_path):
            os.makedirs(doc_path)
        shutil.move(file_path, doc_path)

    def merge_sort(self):
        """
        合并两个sort,扩大训练数据
        :return:
        """
        for root, dirs, files in os.walk(self.predict_sort):
            for doc in dirs:
                doc_path = os.path.join(self.predict_sort, doc)
                sort_path = os.path.join(self.sort_path, doc)

                if not os.path.exists(sort_path):
                    raise Exception('路径不存在:'.format(sort_path))

                for file in os.listdir(doc_path):
                    if file == '.DS_Store':
                        continue

                    file_path = os.path.join(doc_path, file)
                    shutil.move(file_path, sort_path)
