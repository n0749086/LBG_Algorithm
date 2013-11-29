# coding: UTF-8

from __future__ import unicode_literals
from __future__ import with_statement

'''
参考URL
http://hil.t.u-tokyo.ac.jp/~sagayama/applied-acoustics/2009/D3-VQ.pdf
http://www.vision.cs.chubu.ac.jp/flabresearcharchive/bachelor/B06/Paper/yasu.pdf
http://www.cs.nthu.edu.tw/~cchen/CS6531/2012/LBG.pdf
http://www.data-compression.com/vq.html
'''

import sys

N = 2
n = N / 2.0
e = 0.001   #収束判定

def calc_centroid(v):
    c = 0.0
    for i in v:
        c += i
    c /= len(v)
    return int(c)

def calc_delta(c, v):
    delta = -1
    max_v = -1
    for i in v:
        if abs(c-i) > delta:
            delta = abs(c-i)
            max_v = i
    return int(float(i) / 100)

def calc_D(codebook):
    d = 0.0
    cnt = 0
    for i in codebook:
        for j in codebook[i]:
            cnt += 1
            d += pow(i-j, 2)

    return d/cnt

def main():
    #ファイルからのベクトル読み込み
    vectors = []
    with open("test.txt") as f:
        for i in f:
            vectors.append(float(i.decode("utf-8")))


    #level.1のセントロイド（重心）と歪みDを求める
    #centroidの計算
    centroid = {}
    d = len(vectors) / n
    for i in range(int(n)):
        centroid[calc_centroid(vectors[int(d*i):int(d*(i+1))])] = vectors[int(d*i):int(d*(i+1))]

    #歪みの計算
    d = calc_D(centroid)


    #level.1のコードブックの作成（スプリッティングしてるだけ）
    codebook = {}
    for i in centroid:
        delta = calc_delta(i, centroid[i])
        codebook[i+delta] = []
        codebook[i-delta] = []


    #頑張ってクラスタリングするよ！！
    #一個前の歪みの保持
    d_back = d
    count = 0
    while True:
        count += 1
        #どこのクラスタに所属するかをチェック！
        for i in vectors:
            min_d = sys.maxint
            min_Q = -1
            for j in codebook:
                if abs(i-j) < min_d:
                    min_d = abs(i-j)
                    min_Q = j
            codebook[min_Q].append(i)

        #セントロイドの計算
        tmp_codebook = {}
        for i in codebook:
            tmp_codebook[calc_centroid(codebook[i])] = codebook[i]

        codebook = tmp_codebook

        #歪みの計算
        d = calc_D(codebook)

        #収束判定
        print count, (float(d_back) - d) / d
        if ((float(d_back) - d) / d < e):
            break

        d_back = d

    print sorted(codebook.keys())


if __name__ == '__main__':
    main()