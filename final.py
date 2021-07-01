"""
思路：
1、对文档jieba分词成列表，去掉停用词，再整理成集合形式
2、对集合中每一个元素进行检索，整理出字典类型的倒排记录表
3、将含有位置信息的倒排记录表转为无位置信息的，并对其进行布尔查询
4、对含有位置信息的倒排记录表 短语查询

倒排记录表 数据的结构  dp为带位置信息的倒排记录表
dp =
{   # 此处 1, 2, 5, 6 代表 “北京” 这个词在第几个个文档里出现过
    # 此处 7, 9, 1256 等四个列表表示这个词在对应的文档中的倒排记录表

    "疫情":{
                1: [7, 9, 1256],
                2: [56, 89, 784],
                5: [略],
                6: [略],
            },
    "人群":{
                1: [3, 5],
                5: [5, 9],
            }
}

"""
import os
import jieba


doc_path = r".\doc"
stopwords_file = "./停用词标点.txt"
dp = dict()  # 倒排记录表
all_words = []  # 不重复的所有词项

def get_file(path):
    """
    :param path: 数据文件夹路径
    :return: 列出指定路径下的所有目录和文件
    """
    paths = os.listdir(path)
    return paths

def del_stop_words(after_jieba):#去掉停用词以及标点符号，传出一个去掉之后的列表
    """
    :param after_jieba: 传入词语表
    :return: 输出去掉停用词以及标点符号后的词表
    """
    # 将停用词表读入列表
    file = open(stopwords_file, "r", encoding='utf-8')
    stop_words = list()
    for line in file.readlines():
        line = line.strip()
        if not len(line):
            continue
        stop_words.append(line)
    file.close
    stop_words.extend(["\n", "\t", "\xa0", " "])
    after_rm_stop = [x for x in after_jieba if x not in stop_words]  # 使用去除停用词后的变量进行计算
    return after_rm_stop


def cut_words(path):
    """

    :param path: 文件地址
    :return: jieba分词完成后的词项列表
    """
    str_all = open(path, encoding='utf-8').read()
    after_jieba = jieba.lcut(str_all, cut_all=False)
    after_jieba = [i for i in after_jieba if not i.isnumeric()]
    #print(after_jieba)
    return after_jieba


def clean_redundance(after_clean_stop):
    """

    :param after_clean_stop: 删除停用词表后的列表
    :return: 删除冗余词项后的列表
    """
    after_clean_redundency = list(set(after_clean_stop))
    #print(after_clean_redundency)
    return after_clean_redundency

def bool_retreive(dp, input1, input2, action):# 传入的参数是倒排记录表，打印布尔检索的结果。
    """
    打印布尔检索的结果
    :param dp: 倒排记录表
    :return: none
    """
    dp_rm_loc ={word:list(dp[word].keys()) for word in list(dp.keys())}
    print("无位置信息的倒排记录表如下：")
    print(dp_rm_loc)
    # input1 = input("请输入短语1")
    # input2 = input("请输入短语2")
    # input1 = "疫情"
    # input2 = "人群"
    print("指令: and/or/and not/or not")
    # action = input("请输入指令:")
    # action = "and"

    if(input1 not in dp_rm_loc or input2 not in dp_rm_loc):
        return "ERROR:输入词项不在表中"
    print("输入词项无位置信息的倒排记录表如下：：")
    print(input1, dp_rm_loc[input1])
    print(input2, dp_rm_loc[input2])
    print("'{}' {} '{}'  布尔检索结果如下：".format(input1,action,input2))
    ans=[]
    if action == 'and':
        ans = [doc_index for doc_index in dp_rm_loc[input1] if doc_index in dp_rm_loc[input2]]
        print(ans)
    if action == 'or':
        ans = list(set(dp_rm_loc[input1] + dp_rm_loc[input2]))  # 都统一为list
        print(ans)
    if action == 'and not':
        ans = [doc_index for doc_index in dp_rm_loc[input1] if doc_index not in dp_rm_loc[input2]]
        print(ans)
    if action == 'or not':
        ans = []
        for i in range(len(get_file(doc_path))):
            if i in dp_rm_loc[input1] or i not in dp_rm_loc[input2]:
                ans.append(i)

        print(ans)
    result = "'{}' {} '{}'  布尔检索结果如下：".format(input1,action,input2) + str(ans)
    return result


def quest_words(dp, duanyu):  # 这个函数是短语查询的 ， 传入的参数是倒排记录表，打印短语查询的结果
    """
    打印短语查询结果
    :param dp: 倒排记录表
    :return: none
    """
    # duanyu = input("请输入要查询的短语")

    after_jieba = [i for i in jieba.lcut(duanyu, cut_all=False) if i in list(dp.keys())]  # 去掉停用词
    # # 思路：先找词项共同存在的文档, 多个列表的合并，合并为一个集合
    # for word in after_jieba:
    #     print(word, dp[word])
    if len(dp)==0:
        print("短语查询未找到结果")
    a = set(list(dp[after_jieba[0]].keys())) #给a赋初值，某一个词项的 对应出现的 文档的列表转集合  例如 航空公司 a = {1,2,3}, 在1，2,3三篇文档中出现过

    for word in after_jieba:  # 合并所有词项对应的列表，得到一个总的，例如 三个 词项 都在 a（最终）的集合中出现过
        a = a.intersection(list(dp[word].keys()))


    # 再对每一篇文档进行检索 # 在共同存在的文档中再继续找
    is_retrieve = False
    result_doc = []
    for doc_index in a:
        for i in dp[after_jieba[0]][doc_index]:  #遍历 航空公司这个词在第 doc_index 篇的倒排记录表
            # p为指针
            p = i
            is_in = True
            for word in after_jieba[1:]:
                if p+1 not in dp[word][doc_index]:
                    is_in = False
                    break  #没能在这篇文档里一起出现，pass
                p+=1

            if is_in == True:
                is_retrieve = True
                print("在第{}篇文档里查询到短语，词项位置为{}".format(doc_index+1, p-len(after_jieba)+1))
                result_doc.append((doc_index,p-len(after_jieba)+1))
                print(result_doc)
    if is_retrieve == False:
        return 0
    # result = "分别在第{}篇文档里查询到短语，词项位置为{}".format(str(result_doc),str(result_p))
    return result_doc

def get_pre_info(paths, id, loc):
    """

    :param paths: 词项表
    :param id: 词所在的doc id
    :param loc: 词所在的位置
    :return: 包含所查询的词临近的结果
    """
    after_jieba = cut_words(paths[id])  # jieba分词
    # 定位分词与去重后的词项表的loc
    after_rm_stop = del_stop_words(after_jieba)
    # 将列表合并成字符串
    try:
        string = "".join(after_rm_stop[loc-5:loc+5])
    except:
        pass
    return string

