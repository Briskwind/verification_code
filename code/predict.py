import os
import numpy as np
from sklearn.externals import joblib
from sklearn.svm import SVC

from sklearn.model_selection import cross_val_score as cs


class Propheter:
    """ 训练和预测"""

    def __init__(self):
        self.clf = None

    def load_data(self, content_file):
        """
        加载特征值
        :param content_file:
        :return:
        """
        dataset = np.loadtxt(content_file, delimiter=',')
        return dataset

    def cross_validation(self, content_file):
        """
        进行交叉验证
        :param content_file:
        :return:
        """
        dataset = self.load_data(content_file)
        row, col = dataset.shape
        X = dataset[:, :col - 1]
        Y = dataset[:, -1]
        clf = SVC(kernel='rbf', C=1000)
        clf.fit(X, Y)
        scores = cs(clf, X, Y, cv=5)
        print("Accuracy: %0.2f (+- %0.2f)" % (scores.mean(), scores.std()))

        return clf

    def train_creale_plk(self, content_file, plk_file):
        """
        训练数据并且生成训练结果文件
        :param content_file:
        :param plk_file: 训练结果文件
        :return:
        """

        dataset = self.load_data(content_file)
        if not dataset.any():
            raise Exception('特征值文件为空')
        row, col = dataset.shape
        X = dataset[:, :col - 1]
        Y = dataset[:, -1]
        clf = SVC(kernel='rbf', C=1000)
        clf.fit(X, Y)

        scores = cs(clf, X, Y, cv=5)
        print("Accuracy: %0.2f (+- %0.2f)" % (scores.mean(), scores.std()))
        joblib.dump(clf, plk_file)

    def get_propheter(self, plk_file):
        """
        返回先知
        :param plk_file:
        :return:
        """
        if not os.path.exists(plk_file):
            raise Exception('plk文件不存在，请先训练创建')

        self.clf = joblib.load(plk_file)

    def predict_pic(self, img_binary_pix):
        """
        预测图片
        :param img_binary_pix: pix图片
        :return:
        """
        res = self.clf.predict(img_binary_pix.reshape(1, -1))
        return chr(int(res[0]))
