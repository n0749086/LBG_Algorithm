#coding:utf-8

from __future__ import with_statement
from __future__ import unicode_literals

'''
参考URL
    http://hil.t.u-tokyo.ac.jp/~sagayama/applied-acoustics/2009/D3-VQ.pdf
    http://www.vision.cs.chubu.ac.jp/flabresearcharchive/bachelor/B06/Paper/yasu.pdf
    http://www.cs.nthu.edu.tw/~cchen/CS6531/2012/LBG.pdf
    http://www.data-compression.com/vq.html
'''

import csv
import numpy as np
import scipy.cluster
from pylab import *

class codebook(object):
    """docstring for codebook"""

    def __init__(self, input):
        self.__vector = []
        for i in input:
            self.vector.append(np.array(i))
        self.__centroid = 0.0

    def __str__(self):
        return "centroid:" + str(self.__centroid) + " vector_count:" + str(len(self.__vector))

    #中央の計算
    @property
    def centroid(self):
        return self.__centroid

    def _get_vector(self):
        return self.__vector

    def _set_vector(self, value):
        self.__vector.append(value)

    def _del_vector(self):
        self.__vector = []

    vector = property(_get_vector, _set_vector, _del_vector)

    def calc_centroid(self, eps = 0.0):
        if len(self.__vector) < 1:
            return False

        c = np.zeros([len(self.__vector[0])])
        for i in self.__vector:
            c += i
        self.__centroid = (c / len(self.__vector))* (1.0 + eps)

        return True



class LBG_splitting(object):
    """LBG+Splitting Algorithm"""

    #歪みの計算（評価指標/収束判定）
    def calc_D(self):
        result = 0.0

        for code in self.__codebook:
            center = code.centroid
            for child in code.vector:
                result += np.linalg.norm(center - child)

        return result

    def start(self, N, input, eps = np.float64(0.00001)):
        delta = np.float64(0.01)
        eps = np.float64(eps)
        #初期コードブックの作成/初期化
        self.__codebook = []
        N /= 2
        d = int(len(input)/N)
        for i in range(N):
            tmp = input[i*d:(i+1)*d]


            #+deltaと-deltaの分のコードブックを作成する
            code = codebook(tmp)
            code.calc_centroid(delta)
            self.__codebook.append(code)

            code = codebook(tmp)
            code.calc_centroid(-1*delta)
            self.__codebook.append(code)

        #歪み計算
        D = self.calc_D()

        cnt = 0

        #クラスタリングするよ
        while True:
            #とりあえず、前の結果を削除
            for i in self.__codebook:
                del(i.vector)

            #クラスタリング部分
            for vector in input:
                d = np.finfo(np.float64).max
                pos = -1
                for i in range(len(self.__codebook)):
                    code = self.__codebook[i]
                    tmp = np.linalg.norm(vector - code.centroid)
                    if d >= tmp:
                        d = tmp
                        pos = i
                self.__codebook[pos].vector = vector

            #中央値の再計算
            temp_codebook = []
            for i in self.__codebook:
                if i.calc_centroid():
                    temp_codebook.append(i)

            self.__codebook = temp_codebook


            #評価指標の計算
            tmp_D = self.calc_D()
            if (D - tmp_D) / D <= eps:
                break

            D = tmp_D

    @property
    def codebook(self):
        return self.__codebook


def main():
    N = 4           #クラスタ数
    data = []       #入力データ

    with open("./test.csv", "rU") as f:
        for i in csv.reader(f):
            tmp = []
            for j in i:
                tmp.append(int(j))
            data.append(tmp)

    clustering = LBG_splitting()

    clustering.start(N, data)

    for i in range(len(clustering.codebook)):
        codebook = clustering.codebook[i]
        print "Cluster%d" % (i)
        print "\tcentroid:%s" % (codebook.centroid)
        print "\tvectors:"
        for j in codebook.vector:
            print "\t\t%s" % (j)

if __name__ == '__main__':
    main()