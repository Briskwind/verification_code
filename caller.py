import os

from code.Imager_maker import Imager
from code.improve import Improver
from code.predict import Propheter
from code.prepare import Preparer

from conf.config import (plk_file, predict_path, predict_single_doc, sort_path, content_file, save_path, single_pic_doc)


def preparation(count):
    """
    生成验证码，对验证码进行分类，切割成小图
    :param count:
    :return:
    """

    for i in range(count):
        img_path, code = imger.create_img(save_path)
        imger.read_small_and_save(img_path, single_pic_doc)

    # 获取分类文件夹
    doc_list = preparer.get_doc_list(single_pic_doc)

    # 创建分类文件夹
    preparer.make_doc(doc_list, sort_path)
    # 图片分类
    preparer.sort_pic(single_pic_doc, sort_path)


def make_propheter():
    """人工将识别文件进行分类之后进行特征值提取，训练模型创建"""

    preparer.make_content_text(sort_path, content_file)

    # 加载特征值文件，进行交叉验证,训练模型
    propheter.train_creale_plk(content_file, plk_file)


def propheter_predict(count, del_predict_pic=False):
    """ 生成新的验证图片，进行二值化、切割、预测"""
    propheter.get_propheter(plk_file)
    success = 0
    for i in range(count):

        new_img_path, code = imger.create_img(predict_path)
        img_list = imger.read_small_and_save(new_img_path, predict_single_doc, only_save=True)
        tem_list = []
        for img in img_list:
            res = imger.get_binary_pix(img)
            singoe_code = propheter.predict_pic(res)
            tem_list.append(singoe_code)

        first_code = ''.join(code).lower()
        predict_result = ''.join(tem_list).lower()

        if first_code == predict_result:
            success += 1
            print('验证成功:', first_code, predict_result)
        else:
            print('尴尬了,验证失败:', first_code, predict_result)

    if del_predict_pic:
        # 删除预测生成的原图
        for predict_img in os.listdir(predict_path):
            tem_path = os.path.join(predict_path, predict_img)
            os.remove(tem_path)

        # 删除预测生成的裁剪图
        for predict_img_single in os.listdir(predict_single_doc):
            tem_path = os.path.join(predict_single_doc, predict_img_single)
            os.remove(tem_path)

    print('success number:', success)


if __name__ == '__main__':
    imger = Imager()
    preparer = Preparer()
    propheter = Propheter()

    try:
        # imp = Improver(imger, propheter, preparer, plk_file)

        # 对 100 张验证码进行处理准备
        # preparation(100)

        # todo 这里需要人工将 sort 文件加下的文件进行正确的分类,用作训练数据

        # 进行提取特征值，训练
        # make_propheter()

        # 预测 100 张验证码
        propheter_predict(30, del_predict_pic=True)



        # propheter 的自我提升
        # imp.create_pre_single_code(20)
        # imp.predict_and_get_doc_list()

        # todo 当再一次人工对 predict_sort 数据进行筛选之后合并两个分类文件

        # imp.merge_sort()

    except KeyboardInterrupt:
        print('手动终止')
