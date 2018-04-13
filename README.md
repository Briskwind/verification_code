# verification_code
验证码识别、sk-learn

我只是个代码的搬运工，进行了组合整理，写了这个验证码机器识别小栗子。

目前已经稍微训练了一个模型你可以直接调用进行预测(在`caller.py`文件中)：
```python
imger = Imager()
preparer = Preparer()
propheter = Propheter()
propheter_predict(30, del_predict_pic=True)

```

训练方式：

```python
imger = Imager()
preparer = Preparer()
propheter = Propheter()
imp = Improver(imger, propheter, preparer, plk_file)

# 对 100 张验证码进行处理准备
preparation(100)

# todo 这里需要人工将 sort 文件加下的文件进行正确的分类,用作训练数据

# 进行提取特征值，训练
make_propheter()

# 预测 100 张验证码
propheter_predict(30, del_predict_pic=True)



# propheter 的自我提升
# imp.create_pre_single_code(20)
# imp.predict_and_get_doc_list()

# todo 当再一次人工对 predict_sort 数据进行筛选之后合并两个分类文件
# imp.merge_sort()
```