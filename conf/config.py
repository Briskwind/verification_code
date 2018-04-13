import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 生成验证码存储文件夹
save_path = os.path.join(BASE_DIR, 'verification_pic', 'pic')

# 切割好之后单个图片文件夹
single_pic_doc = os.path.join(BASE_DIR, 'verification_pic', 'single_pic')

# 预测验证图片存储未知
predict_path = os.path.join(BASE_DIR, 'verification_pic', 'predict')

# 预测单个图片存储位置
predict_single_doc = os.path.join(BASE_DIR, 'verification_pic', 'predict_single')

# 分类文件夹主目录
sort_path = os.path.join(BASE_DIR, 'verification_pic', 'sort')

# 生成特征值文件
content_file = os.path.join(BASE_DIR, 'verification_pic', 'content.txt')

# 训练文件
plk_file = os.path.join(BASE_DIR, 'verification_pic', 'plk.plk')
