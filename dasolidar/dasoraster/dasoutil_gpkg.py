# -*- coding: utf-8 -*-
'''
/***************************************************************************
        begin                : 2024-12-10
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Jose Bengoa
        email                : dasolidar@gmail.com
 ***************************************************************************/
'''
# import numpy as np
# import math
# a = [2.40693537, 3.05403731, 3.8442875, 4.01401263, 2.57073673, 3.17501312, 3.25257009, 3.51023934, 3.52858761, 2.17859906, 4.26439529, 4.43296013, 4.30312711, 4.34945201, 4.50076341, 2.22192408, 2.8768062, 3.72267627, 3.04756245, 2.74127699, 4.07041003, 4.13340567, 3.54435967, 3.10172933, 3.68561508, 4.1476734, 4.46660295, 4.48932153, 4.76290965, 4.68832833, 4.84888689, 4.44474741, 3.47953024, 2.95317239, 2.16756388]
# #a = np.array([1, 2, 5, 4, 3, 6, 7, 8, 9, 10])
# b = [4.70281554e-01, 8.63061989e-01, 1.12209436e+00, 1.11688287e-01,
#  5.86029689e-01, 1.02866589e+00, 1.07668404e+00, 6.16712822e-02,
#  6.21309765e-01, 9.68648885e-01, 1.12058043e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.68425293e-01,
#  8.33524414e-01, 1.23625178e+00, 1.46566735e+00, 2.27541326e-01,
#  7.65947732e-01, 4.73354174e-01, 3.24863750e-02, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 1.05048838e-01, 8.78810987e-01,
#  1.30114957e+00, 1.70999783e+00, 0.00000000e+00, 2.90596296e-01,
#  5.66169776e-01, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 1.04550789e+00, 1.56694452e+00,
#  1.62376658e-01, 4.71579427e-01, 3.19776094e-01, 4.74559348e-01,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 1.58530159e+00, 0.00000000e+00,
#  0.00000000e+00, 1.32492109e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  9.80346694e-01, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.23729424e-01,
#  7.26398132e-01, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  2.51048380e-01, 2.40693537e+00, 0.00000000e+00, 3.05403731e+00,
#  0.00000000e+00, 3.84428750e+00, 0.00000000e+00, 4.01401263e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 2.57073673e+00,
#  0.00000000e+00, 3.17501312e+00, 0.00000000e+00, 3.25257009e+00,
#  0.00000000e+00, 3.51023934e+00, 0.00000000e+00, 3.52858761e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  2.97837225e-01, 2.10467125e-01, 1.23427150e-01, 2.54258904e-01,
#  1.41073940e+00, 0.00000000e+00, 2.17859906e+00, 0.00000000e+00,
#  0.00000000e+00, 4.26439529e+00, 0.00000000e+00, 5.47374825e-01,
#  0.00000000e+00, 0.00000000e+00, 1.48644249e-01, 3.80727403e-01,
#  3.05873288e-01, 4.13377200e-01, 5.81613748e-01, 1.79020190e-01,
#  4.43296013e+00, 0.00000000e+00, 0.00000000e+00, 4.30312711e+00,
#  0.00000000e+00, 4.34945201e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 3.67582824e-01, 4.04719580e-01,
#  4.61044478e-01, 4.95255904e-01, 8.09617864e-01, 4.89929078e-01,
#  0.00000000e+00, 0.00000000e+00, 4.50076341e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 3.77385087e-01,
#  4.83987045e-01, 4.57849023e-01, 6.97006847e-01, 1.28337055e+00,
#  2.48307774e-01, 8.33812720e-02, 1.59285950e-01, 0.00000000e+00,
#  0.00000000e+00, 5.64534255e-01, 2.22192408e+00, 1.71140890e-01,
#  0.00000000e+00, 1.62521578e-01, 6.06316234e-01, 2.92471275e-01,
#  4.23672373e-01, 2.87680620e+00, 0.00000000e+00, 0.00000000e+00,
#  1.20908574e-01, 3.72787056e-01, 1.02079095e+00, 1.46809756e+00,
#  0.00000000e+00, 2.09089482e-01, 0.00000000e+00, 3.98424628e-01,
#  5.67302731e-01, 3.31285887e-01, 4.39576824e-01, 4.61116382e-01,
#  0.00000000e+00, 0.00000000e+00, 3.92701149e-02, 5.26616058e-01,
#  5.30974818e-01, 5.73693389e-01, 1.21168896e+00, 6.63670367e-01,
#  4.04261741e-01, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 4.67594234e-01, 8.96873237e-01,
#  6.07187550e-01, 1.14460797e+00, 5.07348170e-01, 0.00000000e+00,
#  1.30344919e+00, 1.26127896e+00, 1.08766109e+00, 7.72125981e-01,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.34875665e+00,
#  0.00000000e+00, 0.00000000e+00, 1.50994897e+00, 1.34393213e+00,
#  9.04760680e-01, 1.21433060e-01, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 2.90804945e-01, 1.75685205e+00,
#  1.62247539e+00, 1.29922016e+00, 8.98171346e-01, 2.36024820e-03,
#  0.00000000e+00, 0.00000000e+00, 4.86043130e-02, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  5.55374067e-01, 1.70076012e+00, 1.38568618e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 2.33147716e-01,
#  4.59838346e-01, 1.35666369e+00, 0.00000000e+00, 1.10768659e-01,
#  1.84335631e+00, 0.00000000e+00, 0.00000000e+00, 5.76040973e-02,
#  1.01501682e-01, 3.25504161e-01, 2.48075871e-01, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 3.72267627e+00, 3.04756245e+00,
#  2.74127699e+00, 1.03596655e-01, 7.39833565e-02, 3.05910628e-01,
#  4.30024834e-01, 6.05503944e-01, 4.40850228e-01, 0.00000000e+00,
#  1.21560865e-01, 4.07041003e+00, 0.00000000e+00, 4.13340567e+00,
#  0.00000000e+00, 0.00000000e+00, 3.54435967e+00, 0.00000000e+00,
#  3.10172933e+00, 3.10633143e-01, 2.96328874e-01, 5.05740161e-01,
#  5.55645130e-01, 6.47881969e-01, 7.84777271e-01, 6.13398332e-01,
#  0.00000000e+00, 1.13628599e-02, 3.68561508e+00, 0.00000000e+00,
#  4.14767340e+00, 0.00000000e+00, 4.46660295e+00, 0.00000000e+00,
#  4.48932153e+00, 0.00000000e+00, 0.00000000e+00, 3.48926000e-01,
#  9.19211850e-01, 7.88109971e-01, 4.59300082e-01, 3.13928527e-01,
#  4.06891652e-01, 2.78028698e-01, 0.00000000e+00, 0.00000000e+00,
#  1.18014295e-01, 4.76290965e+00, 0.00000000e+00, 4.68832833e+00,
#  0.00000000e+00, 2.71044693e-02, 6.94162254e-01, 1.72569951e+00,
#  0.00000000e+00, 1.45173219e+00, 5.23016323e-01, 2.33086084e-01,
#  1.41951698e-01, 6.30095242e-02, 0.00000000e+00, 4.84888689e+00,
#  0.00000000e+00, 4.44474741e+00, 0.00000000e+00, 1.12586248e-01,
#  1.18302538e-01, 5.14821002e-01, 9.43697491e-01, 7.28141822e-01,
#  4.01453854e-01, 2.72993412e-01, 6.46446979e-02, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.47184194e-01,
#  2.62879926e-01, 6.30377477e-01, 9.82486778e-01, 8.09651766e-01,
#  4.88570445e-01, 2.87191506e-01, 1.71603330e-01, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 3.47953024e+00, 2.95317239e+00,
#  2.16756388e+00]
# c = [9.09119011e-01, 2.81034815e+00, 4.50089228e+00, 4.76683390e+00,
#  4.50349678e+00, 2.42162276e+00, 0.00000000e+00, 0.00000000e+00,
#  9.54266688e-01, 0.00000000e+00, 4.99077934e+00, 4.94967016e+00,
#  2.71371141e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 3.98544709e+00, 4.95664760e+00,
#  5.14616271e+00, 0.00000000e+00, 6.30400205e-01, 9.75492352e-01,
#  9.37720003e-01, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 1.29216128e+00, 0.00000000e+00, 2.69872975e+00,
#  2.87164868e+00, 3.40114048e+00, 3.84245604e+00, 4.01457463e+00,
#  0.00000000e+00, 3.45324555e-01, 1.07983685e-01, 1.46331681e-01,
#  0.00000000e+00, 6.81965425e-02, 8.26581222e-02, 0.00000000e+00,
#  2.59699920e+00, 0.00000000e+00, 3.46968574e+00, 0.00000000e+00,
#  3.61823205e+00, 0.00000000e+00, 3.27509174e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 9.60053090e-03, 1.41893279e-01,
#  4.24751496e-01, 3.14388708e-01, 2.86703335e-01, 5.20024157e-01,
#  5.19111787e-01, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 6.04733794e-02, 1.30819869e-01, 1.19907499e-01,
#  0.00000000e+00, 0.00000000e+00, 5.87781896e-01, 2.88756678e-01,
#  6.26044132e-01, 8.18162715e-01, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 5.30309216e-02, 1.50128323e-01, 2.85731429e-01,
#  2.80389823e-01, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  3.10008343e-02, 7.07747742e-01, 6.43695351e-01, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.59745693e-01,
#  1.09659934e-01, 0.00000000e+00, 6.80993786e-02, 1.67187009e-01,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 2.12087878e-02,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  9.69389926e-02, 6.53105838e-02, 1.61858404e-01, 1.80883410e-01,
#  3.90601607e-01, 2.32237312e-01, 0.00000000e+00, 2.34781096e-01,
#  6.23644101e-02, 0.00000000e+00, 0.00000000e+00, 1.87087490e-01,
#  1.26262096e-01, 1.60920489e-01, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 1.29132836e+00, 0.00000000e+00,
#  2.61473488e-01, 3.22252226e-01, 5.17409791e-02, 4.45801436e-01,
#  0.00000000e+00, 1.35200818e-02, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 4.92447861e-02, 1.43387138e+00, 0.00000000e+00,
#  3.53819694e-01, 0.00000000e+00, 0.00000000e+00, 2.84119528e-01,
#  0.00000000e+00, 9.12469983e-02, 3.99392189e-01, 0.00000000e+00,
#  1.31456324e-02, 0.00000000e+00, 0.00000000e+00, 1.65531706e-01,
#  0.00000000e+00, 0.00000000e+00, 4.17078808e-03, 0.00000000e+00,
#  0.00000000e+00, 3.32223476e-02, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 4.16052710e-03,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 9.40574978e-02, 0.00000000e+00,
#  0.00000000e+00, 6.82292139e-02, 0.00000000e+00, 9.73254025e-01,
#  1.03420858e+00, 0.00000000e+00, 2.45265880e+00, 0.00000000e+00,
#  1.16761900e+00, 5.86429324e-02, 0.00000000e+00, 0.00000000e+00,
#  1.18709914e+00, 0.00000000e+00, 4.63759482e+00, 4.74609654e+00,
#  3.28937240e+00, 3.35567055e+00, 0.00000000e+00, 2.35295243e+00,
#  1.90870698e+00, 0.00000000e+00, 9.08177177e-02, 0.00000000e+00,
#  5.25866369e-02, 1.09594065e-01, 3.36836928e-01, 4.48531119e-01,
#  3.53941176e-01, 4.61321258e+00, 0.00000000e+00, 4.70999043e+00,
#  4.18257461e+00, 2.33445817e+00, 0.00000000e+00, 0.00000000e+00,
#  9.86397243e-02, 1.50625970e-01, 3.99317746e-01, 5.53442680e-01,
#  4.08579907e-02, 3.11055982e+00, 0.00000000e+00, 4.00965082e+00,
#  4.84111185e+00, 4.90532376e+00, 4.05642867e+00, 2.18554057e-01,
#  3.01449039e+00, 1.96916680e+00, 0.00000000e+00, 5.47620561e-02,
#  2.38315317e-01, 3.03441584e-01, 4.65310497e-01, 6.77004688e-01,
#  2.32481160e-02, 5.39628321e+00, 3.62303134e+00, 3.46084179e+00,
#  2.48864597e+00, 0.00000000e+00, 0.00000000e+00, 6.19083705e-01,
#  6.84209972e-01, 1.37256759e-01, 1.04294195e+00, 1.62874978e-01,
#  1.62145186e-01, 4.69057527e+00, 0.00000000e+00, 2.72397522e+00,
#  0.00000000e+00, 0.00000000e+00, 3.38440379e+00, 0.00000000e+00,
#  3.14327870e-01, 7.16798006e-02, 0.00000000e+00, 0.00000000e+00,
#  1.05273653e+00, 5.33125408e-01, 2.27795830e-01, 1.11181130e-01,
#  5.02303648e-01, 4.06917450e-01, 1.14494952e-01, 1.67478359e-01,
#  2.51550845e-01, 1.38163141e-01, 0.00000000e+00, 0.00000000e+00,
#  1.35255140e-01, 1.10145972e-01, 4.54773176e-02, 0.00000000e+00,
#  3.57071548e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#  6.62287914e-02, 2.30835833e-01, 2.92822079e-01, 1.68380595e-01,
#  5.49928907e-02, 0.00000000e+00, 7.30114953e-02, 3.16909259e-01,
#  4.49517807e-01, 1.09080071e-01, 0.00000000e+00, 1.08552300e+00,
#  0.00000000e+00, 3.80893752e+00, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 1.29761403e-01, 3.37713544e-01, 2.59896604e-01,
#  1.97248535e-01, 0.00000000e+00, 1.07018960e-01, 1.05629750e-01,
#  1.12720888e+00, 1.04456081e+00, 0.00000000e+00, 1.37109748e+00,
#  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 3.52437720e-01,
#  1.30019950e-02, 8.46961859e-02, 1.26009758e+00, 1.27413971e+00,
#  4.66872822e-02, 8.51807397e-02, 9.83692251e-02, 0.00000000e+00,
#  1.21122358e-01, 2.18160143e-01, 3.00343202e-01, 3.77350630e-01,
#  1.69128944e-02, 4.73204284e-01, 1.43301103e-01, 5.05909651e-01,
#  2.73780807e-01, 2.02077450e-01, 0.00000000e+00, 0.00000000e+00,
#  0.00000000e+00, 0.00000000e+00, 5.09071457e-02, 3.30031170e-01,
#  5.94668568e-01, 3.38140843e-01, 1.23550900e-01, 8.09028308e-02,
#  3.39544747e-01, 2.81068388e-01, 2.65712547e-01, 1.19863744e-01,
#  4.42503761e-02, 7.84622859e-02, 2.64211878e-02, 1.16452356e-01,
#  7.36968673e-01, 5.40410592e-01, 4.49256817e-01, 9.85532897e-02,
#  1.26849933e-01, 1.88096545e-01, 2.82811107e-02, 8.17466254e-02,
#  2.96177352e-01, 8.20500133e-02, 1.83268661e-03, 1.96958953e-01]
# aa = np.array(a)
# aaa = np.percentile(aa, 95)
# bb = np.array(b)
# bbb = np.percentile(bb, 95)
# cc = np.array(c)
# ccc = np.percentile(cc, 95)
# # c = np.percentile(a[a>4], 95)
# print(f'a: {aaa}')
# print(f'b: {bbb}')
# print(f'c: {ccc}')
# quit()


import os
import json
import math
import time
from datetime import datetime

from osgeo import ogr, osr


driver_gpkg = ogr.GetDriverByName('GPKG')

dict_nombres_variables_dasometricas = {
    'Volumen de madera (fustes)': 'VCC',
    'Diámetro medio (cuadrático)': 'DCM',
    'Número de pies por hectárea (densidad)': 'Npies',
    'Área basimétrica': 'Abas',
    'Crecimiento anual en volumen': 'IAVC',
    'Biomasa aérea': 'BA',
    'Volumen de leñas': 'VLE',
    'Altura dominante lidar (es una métrica lidar)': 'Hdom',
}
dict_nombres_variables_dasometricas_inverso = {}
for key, variable_dasometrica in dict_nombres_variables_dasometricas.items():
    dict_nombres_variables_dasometricas_inverso[variable_dasometrica] = key
dict_capas_variables_dasometricas = {
    'VolumenMadera_m3_ha': 'VCC',
    'DiamMed_cm': 'DCM',
    'NumPies_ha': 'Npies',
    'AreaBasimetrica_m2_ha': 'Abas',
    'CrecimientoVolumenMadera_m3_ha.año': 'IAVC',
    'BiomasaAerea_t_ha': 'BA',
    'VolumenLeñas_m3_ha': 'VLE',
    'AlturaDominanteLidar_m': 'alt95',
}
dict_capas_variables_dasometricas_inverso = {}
for key, variable_dasometrica in dict_capas_variables_dasometricas.items():
    dict_capas_variables_dasometricas_inverso[variable_dasometrica] = key
dict_capas_metricas_lidar = {
    'AlturaDominanteLidar_m': 'alt95',
    'Cob5m_PRT_PNOA2': 'cob5m',
    'Cob3m_PRT_PNOA2': 'cob3m',
    'CobEstr_MidHD_TopHD_TLR_PNOA2': 'c_sup',
    'CobEstr_200cm_MidHD_TLR_PNOA2': 'c_med',
    'CobEstr_050cm_200cm_TLR_PNOA2': 'c_inf',
    'CobEstrDe0025a0150cm_TLR_PNOA2': 'c_st1',
    'CobEstrDe0150a0250cm_TLR_PNOA2': 'c_st2',
    'CobEstrDe0250a0500cm_TLR_PNOA2': 'c_st3',
}
dict_capas_metricas_lidar_inverso = {}
for key, variable_dasometrica in dict_capas_metricas_lidar.items():
    dict_capas_metricas_lidar_inverso[variable_dasometrica] = key


def codifica_variable_dasometrica(variable_aportada):
    if variable_aportada in dict_nombres_variables_dasometricas:
        cod_variable_dasometrica = dict_nombres_variables_dasometricas[variable_aportada]
    elif variable_aportada in dict_capas_variables_dasometricas:
        cod_variable_dasometrica = dict_capas_variables_dasometricas[variable_aportada]
    elif variable_aportada in dict_capas_metricas_lidar:
        cod_variable_dasometrica = dict_capas_metricas_lidar[variable_aportada]
    else:
        cod_variable_dasometrica = variable_aportada
    return cod_variable_dasometrica


def componer_geodata(
        usuario_actual,
        tipo_consulta,
        x_consulta,
        y_consulta,
        parcela_circular,
        radio_parcela,
        rodal_hectareas,
        layer_raster_XXX_name_txt,
        medicion_dasolidar,
        datos_recibidos='',
        obs_txt_multi_linea_etiquetado='',
        obs_txt_multi_linea_sinretornos='',
        obs_lista_lineas_sinetiquetar=[],  #  No lo uso
    ):
    hoy_AAAAMMDD = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
    ahora_HHMMSS = datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')
    [especie_aportada, variable_aportada, medicion_aportada, unidad_aportada, publicar_datos, fiabilidad_datos] = datos_recibidos

    cod_variable_dasometrica = codifica_variable_dasometrica(variable_aportada)

    if not obs_txt_multi_linea_sinretornos:
        obs_txt_multi_linea_sinretornos = ''
        for num_linea, mi_linea in enumerate(obs_txt_multi_linea_etiquetado):
            # list_linea = str(mi_linea.split(';')[2:])
            # txt_linea = ''
            # for t_linea in list_linea:
            #     txt_linea += t_linea.replace('\r\n', ' ').replace('\n', ' ')
            if len(mi_linea) > 5 and mi_linea[5] == ';':
                txt_linea = mi_linea[6:].replace('\r\n', ' -/- ').replace('\n', ' -/- ')
            elif len(mi_linea) > 7:
                txt_linea = mi_linea[7:].replace('\r\n', ' -/- ').replace('\n', ' -/- ')
            else:
                txt_linea = mi_linea.replace('\r\n', ' -/- ').replace('\n', ' -/- ')
            if ' -/- ' in txt_linea:
                obs_txt_multi_linea_sinretornos += txt_linea
            else:
                obs_txt_multi_linea_sinretornos += f'{txt_linea} -/- '
        obs_txt_multi_linea_sinretornos = obs_txt_multi_linea_sinretornos.replace('\r\n', ' -/- ').replace('\n', ' -/- ')

    dict_geodata = {
        'x_parcela': float(x_consulta),
        'y_parcela': float(y_consulta),
        'Usuario332': usuario_actual,
        'FechaEntrada_AAAAMMDD': hoy_AAAAMMDD,
        'VariableAportada': cod_variable_dasometrica,
        'UnidadAportada': unidad_aportada,
        'EspecieAportada': especie_aportada[-3:-1],
        'CapaDasolidar': layer_raster_XXX_name_txt,
        'MedicionDasolidar': float(medicion_dasolidar),
        'fiabilidad_datos': int(fiabilidad_datos),
        'Observaciones': obs_txt_multi_linea_sinretornos,
    }
    # if medicion_aportada.isdigit(): -> no conisdera digit el . y ,
    # En origen es texto; admito decimales con '.' y con ',' 
    medicion_aportada = medicion_aportada.replace(',', '.')
    try:
        dict_geodata['MedicionAportada'] = float(medicion_aportada)
    except:
        dict_geodata['MedicionAportada'] = 0.0

    if tipo_consulta == 'parcela':
        if parcela_circular == 'False':
            dict_geodata['tipo_recinto'] = 'parcelaCuadrada'
        else:
            dict_geodata['tipo_recinto'] = 'parcelaCircular'
        try:
            dict_geodata['RadioParcela'] = float(radio_parcela)
        except:
            dict_geodata['RadioParcela'] = 15.0
        dict_geodata['SuperficieRodal_ha'] = 0.0
    elif tipo_consulta == 'rodal':
        dict_geodata['tipo_recinto'] = 'rodal'
        dict_geodata['RadioParcela'] = 0.0
        try:
            dict_geodata['SuperficieRodal_ha'] = float(rodal_hectareas)
        except:
            dict_geodata['SuperficieRodal_ha'] = 0
    return dict_geodata

def crear_circulo(x, y, radio, num_puntos=100):
    puntos = []
    for i in range(num_puntos):
        angulo = 2 * math.pi * i / num_puntos  # Dividir el círculo en segmentos
        punto_x = x + radio * math.cos(angulo)
        punto_y = y + radio * math.sin(angulo)
        puntos.append((punto_x, punto_y))
    return puntos

def crear_cuadrado(x, y, lado):
    half_side = lado / 2
    puntos = [
        (x - half_side, y - half_side),  # Esquina inferior izquierda
        (x + half_side, y - half_side),  # Esquina inferior derecha
        (x + half_side, y + half_side),  # Esquina superior derecha
        (x - half_side, y + half_side),  # Esquina superior izquierda
        (x - half_side, y - half_side)   # Cerrar el cuadrado
    ]
    return puntos

def guardar_parcela_en_gpkg(
        geopackage_filepath_all,
        tipo_geodata='parcela',
        dicts_geodata=[{}],
        geojson_path=None,
        # publicar_datos=False,
    ):
    # if tipo_geodata == 'parcela':
    #     layer_name = 'parcelas'
    # elif tipo_geodata == 'rodal':
    #     layer_name = 'rodales'

    geopackage_filepath_ok = []
    for num_geopack, mi_geopackage_filepath in enumerate(geopackage_filepath_all):
        if os.path.exists(mi_geopackage_filepath):
            geopackage_filepath_ok.append(mi_geopackage_filepath)
    geodata_source_all = [None] * len(geopackage_filepath_ok)
    for num_geopack, mi_geopackage_filepath in enumerate(geopackage_filepath_ok):
        try:
            geodata_source_all[num_geopack] = driver_gpkg.Open(mi_geopackage_filepath, 1)  # 1 significa que abrimos en modo de escritura
        except:
            print(f'Error al abrir el GeoPackage {mi_geopackage_filepath}')
            continue
        if geodata_source_all[num_geopack] is None:
            print(f'No se pudo abrir el GeoPackage {mi_geopackage_filepath}')
            continue

    if any(x is not None for x in geodata_source_all):
        for num_geosource, geodata_source_ in enumerate(geodata_source_all):
            if geodata_source_ is None:
                continue
            mi_geopackage_filepath = geopackage_filepath_ok[num_geosource]
            # Obtener la capa existente -------> Capa de puntos
            layer_name1 = 'parcelas'
            layer_name2 = 'parcela'
            mi_layer = geodata_source_.GetLayer(layer_name1)
            if mi_layer is None:
                mi_layer = geodata_source_.GetLayer(layer_name2)
                layer_name = layer_name2
            else:
                layer_name = layer_name1
            if mi_layer is None:
                print(f'El gpkg {mi_geopackage_filepath} no tiene la capa {layer_name1} ni {layer_name2}')
                geodata_source_ = None
            else:
                for mi_parcela_rodal in dicts_geodata:
                    # Guardo el punto
                    punto = ogr.Geometry(ogr.wkbPoint)
                    punto.AddPoint(mi_parcela_rodal['x_parcela'], mi_parcela_rodal['y_parcela'])
                    new_feature = ogr.Feature(mi_layer.GetLayerDefn())
                    new_feature.SetGeometry(punto)
                    lista_campos = list(mi_parcela_rodal.keys())
                    try:
                        lista_campos.remove('x_parcela')
                        lista_campos.remove('y_parcela')
                        # lista_campos.remove('RadioParcela')
                        # lista_campos.remove('SuperficieRodal_ha')
                    except ValueError as e:
                        print(f"Error al eliminar claves: {e}")
                    try:
                        for mi_campo in lista_campos:
                            campo_index = new_feature.GetFieldIndex(mi_campo)
                            if campo_index != -1:
                                # if mi_campo == 'tipo_recinto':
                                #     if tipo_geodata == 'parcela':
                                #         if mi_parcela_rodal['tipo_recinto'] == 'parcelaCircular':
                                #             new_feature.SetField('tipo_recinto', 'parcelaCircular')
                                #         else:
                                #             new_feature.SetField('tipo_recinto', 'parcelaCuadrada')
                                #     else:
                                #         new_feature.SetField('tipo_recinto', tipo_geodata)
                                #     continue
                                #     # new_feature.SetField('tipo_recinto', tipo_geodata)
                                new_feature.SetField(mi_campo, mi_parcela_rodal[mi_campo])
                                # print(f"Campo '{mi_campo}' encontrado en la posición {campo_index}.")
                            else:
                                print(f'El campo "{mi_campo}" no existe en la capa {layer_name}.')
                    except ValueError as e:
                        print(f"Error al guardar campos en la capa {layer_name}: {e}")
                    # Añadir la característica a la capa
                    try:
                        mi_layer.CreateFeature(new_feature)
                    except ValueError as e:
                        print(f"Error al crear el nuevo registro de punto en la capa {layer_name}: {e}")
                    # Limpiar la característica
                    new_feature = None

            # Obtener la capa existente -------> Capa de poligonos
            layer_name1 = 'rodal'
            layer_name2 = 'rodales'
            mi_layer = geodata_source_.GetLayer(layer_name1)
            if mi_layer is None:
                mi_layer = geodata_source_.GetLayer(layer_name2)
                layer_name = layer_name2
            else:
                layer_name = layer_name1
            if mi_layer is None:
                print(f'El gpkg {mi_geopackage_filepath} no tiene la capa {layer_name1} ni {layer_name2}')
                geodata_source_ = None
                continue
            for mi_parcela_rodal in dicts_geodata:
                # Guardo la parcela
                if tipo_geodata == 'parcela':
                    if mi_parcela_rodal['tipo_recinto'] == 'parcelaCircular':
                        # Crear los puntos del círculo
                        puntos_parcela = crear_circulo(
                            mi_parcela_rodal['x_parcela'],
                            mi_parcela_rodal['y_parcela'],
                            mi_parcela_rodal['RadioParcela'],
                        )
                    else:
                        # Crear un cuadrado
                        puntos_parcela = crear_cuadrado(
                            mi_parcela_rodal['x_parcela'],
                            mi_parcela_rodal['y_parcela'],
                            mi_parcela_rodal['RadioParcela'] * 2  # Usar el radio como la mitad del lado
                        )

                    # Crear la geometría del polígono
                    ring = ogr.Geometry(ogr.wkbLinearRing)
                    for punto in puntos_parcela:
                        ring.AddPoint(punto[0], punto[1])
                    ring.CloseRings()
                    poligono = ogr.Geometry(ogr.wkbPolygon)
                    poligono.AddGeometry(ring)
                    multipoligono = ogr.Geometry(ogr.wkbMultiPolygon)
                    multipoligono.AddGeometry(poligono)
                    # Crear una nueva característica (feature)
                    new_feature = ogr.Feature(mi_layer.GetLayerDefn())
                    new_feature.SetGeometry(multipoligono)

                    lista_campos = list(mi_parcela_rodal.keys())
                    try:
                        lista_campos.remove('x_parcela')
                        lista_campos.remove('y_parcela')
                        # lista_campos.remove('RadioParcela')
                        # lista_campos.remove('SuperficieRodal_ha')
                    except ValueError as e:
                        print(f"Error al eliminar claves: {e}")
                    try:
                        for mi_campo in lista_campos:
                            campo_index = new_feature.GetFieldIndex(mi_campo)
                            if campo_index != -1:
                                # if mi_campo == 'tipo_recinto':
                                #     if mi_parcela_rodal['tipo_recinto'] == 'parcelaCircular':
                                #         new_feature.SetField('tipo_recinto', 'parcelaCircular')
                                #     else:
                                #         new_feature.SetField('tipo_recinto', 'parcelaCuadrada')
                                #     continue
                                new_feature.SetField(mi_campo, mi_parcela_rodal[mi_campo])
                                # print(f"Campo '{mi_campo}' encontrado en la posición {campo_index}.")
                            else:
                                print(f'El campo "{mi_campo}" no existe en la capa {layer_name}.')
                    except ValueError as e:
                        print(f"Error al guardar campos en la capa {layer_name}: {e}")
                    # Añadir la característica a la capa
                    try:
                        mi_layer.CreateFeature(new_feature)
                    except ValueError as e:
                        print(f"Error al crear el nuevo registro de poligono en la capa {layer_name}: {e}")
                    # Limpiar la característica
                    new_feature = None

                elif tipo_geodata == 'rodal':
                    # Abrir el archivo GeoJSON
                    if geojson_path is None or not geojson_path:
                        print('No hay fichero adjunto. Tipo de dato aportado: {tipo_geodata}.')
                        geojson_data_source = None
                    else:
                        # Esto no corrije el mensaje de "ERROR 1: PROJ: proj_create: no database context specified"
                        manipular_crs = False
                        quitar_doble_dos_puntos = False
                        quitar_crs = False
                        asignar_crs_EPSG25830 = False
                        if manipular_crs:
                            # Verificar el CRS en el archivo GeoJSON
                            with open(geojson_path, 'r', encoding='utf-8') as f:
                                geojson_content = json.load(f)
                            # Ubicación de mi proj: C:\conda\py39\envs\clid2023\Library\share\proj
                            # Comprobar y corregir el CRS
                            if 'crs' in geojson_content:
                                if quitar_doble_dos_puntos:
                                    crs = geojson_content['crs']
                                    if 'properties' in crs and 'name' in crs['properties']:
                                        crs_name = crs['properties']['name']
                                        if '::' in crs_name:
                                            print(f'CRS encontrado con doble dos puntos: {crs_name}')
                                            crs_name = crs_name.replace('::', ':')
                                            print(f'CRS corregido: {crs_name}')
                                            # Actualizar el CRS en el contenido
                                            crs['properties']['name'] = crs_name
                                # Elimino la clave 'crs'
                                if quitar_crs:
                                    if 'crs' in geojson_content:
                                        del geojson_content['crs']
                                        print("Sección 'crs' eliminada del GeoJSON.")
                                if asignar_crs_EPSG25830:
                                    # Asignar el nuevo CRS (EPSG:25830)
                                    geojson_content['crs'] = {
                                        "type": "name",
                                        "properties": {
                                            "name": "urn:ogc:def:crs:EPSG:25830"
                                        }
                                    }
                            # Guardo el GeoJSON corregido
                            with open(geojson_path, 'w', encoding='utf-8') as f:
                                json.dump(geojson_content, f, indent=4)  # Usar indent=4 para una mejor legibilidad

                        geojson_driver = ogr.GetDriverByName('GeoJSON')
                        geojson_data_source = geojson_driver.Open(geojson_path, 0)  # 0 significa que abro en modo de solo lectura

                    if geojson_data_source is None:
                        print('No se pudo abrir el archivo GeoJSON {geojson_path}.')
                    else:
                        # Obtener la capa del GeoJSON
                        geojson_layer = geojson_data_source.GetLayer()

                        # # Iterar sobre las características del GeoJSON y añadirlas a la capa del GeoPackage
                        for mi_feature in geojson_layer:
                            # Crear una nueva característica (feature) para la capa del GeoPackage
                            new_feature = ogr.Feature(mi_layer.GetLayerDefn())
                            new_feature.SetGeometry(mi_feature.GetGeometryRef())

                            # # Podría copiar los campos adicionales que llegan en el GeoJSON, pero son variados
                            for campo_origen in mi_feature.keys():
                                if campo_origen == 'C_MON_ID' or campo_origen == 'MONT' or campo_origen == 'MONTE_LD':
                                    # Numero de monte en las capas:
                                    # mup_ex_etrs89         -> MONT
                                    # montes_ordenados_CyL  -> MONT y MONTE_LD
                                    # RODAL                 -> C_MON_ID
                                    campo_destino = 'C_MON_ID'
                                    campo_index = new_feature.GetFieldIndex(campo_destino)
                                    if campo_index != -1:
                                        new_feature.SetField(campo_destino, mi_feature.GetField(campo_origen))
                                else:
                                    pass
                            if False:
                                target_srs = osr.SpatialReference()
                                target_srs.ImportFromEPSG(25830)
                                # Obtener la geometría del GeoJSON
                                geom = mi_feature.GetGeometryRef()
                                # Obtener el sistema de referencia de la geometría
                                source_srs = geom.GetSpatialReference()
                                # Transformar la geometría al CRS de la capa del GeoPackage si es necesario
                                if source_srs is not None and not source_srs.IsSame(target_srs):
                                    transform = osr.CoordinateTransformation(source_srs, target_srs)
                                    geom.Transform(transform)  # Transformar la geometría
                                # Establecer la geometría transformada en la nueva característica
                                new_feature.SetGeometry(geom)

                            lista_campos = list(mi_parcela_rodal.keys())
                            try:
                                lista_campos.remove('x_parcela')
                                lista_campos.remove('y_parcela')
                                # lista_campos.remove('RadioParcela')
                                # lista_campos.remove('SuperficieRodal_ha')
                            except ValueError as e:
                                print(f"Error al eliminar claves: {e}")
                                geodata_source_ = None
                                return
                            try:
                                for mi_campo in lista_campos:
                                    campo_index = new_feature.GetFieldIndex(mi_campo)
                                    if campo_index != -1:
                                        # if mi_campo == 'tipo_recinto':
                                        #     new_feature.SetField('tipo_recinto', tipo_geodata)
                                        #     continue
                                        new_feature.SetField(mi_campo, mi_parcela_rodal[mi_campo])
                                        # print(f"Campo '{mi_campo}' encontrado en la posición {campo_index}.")
                                    else:
                                        print(f'El campo "{mi_campo}" no existe en la capa {layer_name}.')
                            except ValueError as e:
                                print(f"Error al guardar campos en la capa {layer_name}: {e}")
                            # Añadir la característica a la capa
                            mi_layer.CreateFeature(new_feature)
                            # Limpiar la característica
                            new_feature = None

            # Cerrar el GeoPackage
            geodata_source_ = None
            print(f'Datos de parcela añadidos correctamente a {os.path.basename(mi_geopackage_filepath)} ({num_geosource + 1} de {len(geodata_source_all)})')
