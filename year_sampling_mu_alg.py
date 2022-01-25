import math
import random

import matplotlib.pyplot as plt
import numpy as np

#############################################YEARLY PROFILES%###########################################################
#######################################profil parameters ###############################################################
from functions import EXAMINE_EVERY_HOUR

NUMBER_OF_SAMPLING = 24
NUMBER_OF_WEEKS_IN_SEASON_SUMMER = 13
NUMBER_OF_WEEKS_IN_SEASON_FALL = 13
NUMBER_OF_WEEKS_IN_SEASON_SPRING = 13
NUMBER_OF_WEEKS_IN_SEASON_WINTER = 13

MU_START_SUMMER = 50
MU_START_FALL = 50
MU_START_SPRING = 50
MU_START_WINTER = 50

mu_step = 9

##################################commercial profile ###############################################################

SAMPLES_24_HOURS_WEEKDAY_SUMMER_COMMERCIAL = [0.573033836636817, 0.532584389344807, 0.525842814796138, 0.51910124024747,
                                              0.51910124024747,
                                              0.525842814796138, 0.532584389344807, 0.714606902158854,
                                              0.903370989521571, 1.05168562959228,
                                              1.11910137507896, 1.18651712056565, 1.19325869511431, 1.20000026966298,
                                              1.19325869511431,
                                              1.18651712056565, 1.15955082237097, 1.11910137507896, 1.09213507688429,
                                              1.04494405504361,
                                              0.997753033202929, 0.910112564070239, 0.808988945840213, 0.64719115667217]

SAMPLES_24_HOURS_FRIDAY_SUMMER_COMMERCIAL = [0.620224858477496, 0.573033836636817, 0.552809112990812, 0.532584389344807,
                                             0.532584389344807,
                                             0.552809112990812, 0.620224858477496, 0.714606902158854, 0.856179967680892,
                                             0.997753033202929,
                                             1.06516877868961, 1.09213507688429, 1.09213507688429, 1.07865192778695,
                                             1.0044946077516,
                                             0.95056201136225, 0.808988945840213, 0.714606902158854, 0.701123753061518,
                                             0.694382178512849,
                                             0.694382178512849, 0.707865327610186, 0.633708007574833, 0.620224858477496]

SAMPLES_24_HOURS_SATURDAY_SUMMER_COMMERCIAL = [0.552809112990812, 0.532584389344807, 0.532584389344807,
                                               0.51910124024747, 0.51910124024747,
                                               0.512359665698801, 0.498876516601464, 0.51910124024747,
                                               0.525842814796138,
                                               0.573033836636817, 0.620224858477496, 0.64719115667217,
                                               0.674157454866844,
                                               0.701123753061518, 0.701123753061518, 0.701123753061518,
                                               0.701123753061518,
                                               0.701123753061518, 0.701123753061518, 0.707865327610186,
                                               0.714606902158854,
                                               0.755056349450865, 0.714606902158854, 0.633708007574833]

SAMPLES_24_HOURS_WEEKDAY_FALL_COMMERCIAL = [0.498876516601464, 0.485393367504127, 0.451685494760785, 0.444943920212117,
                                            0.444943920212117,
                                            0.471910218406791, 0.620224858477496, 0.755056349450865, 0.86292154222956,
                                            0.943820436813581,
                                            0.99101145865426, 0.997753033202929, 1.0044946077516, 0.997753033202929,
                                            0.984269884105592,
                                            0.957303585910918, 0.957303585910918, 0.964045160459587, 0.903370989521571,
                                            0.856179967680892,
                                            0.782022647645539, 0.667415880318175, 0.579775411185486, 0.525842814796138]

SAMPLES_24_HOURS_FRIDAY_FALL_COMMERCIAL = [0.552809112990812, 0.525842814796138, 0.512359665698801, 0.512359665698801,
                                           0.525842814796138,
                                           0.552809112990812, 0.626966433026165, 0.755056349450865, 0.842696818583555,
                                           0.916854138618908,
                                           0.943820436813581, 0.930337287716244, 0.903370989521571, 0.849438393132223,
                                           0.741573200353528,
                                           0.620224858477496, 0.586516985734154, 0.620224858477496, 0.613483283928828,
                                           0.593258560282823,
                                           0.573033836636817, 0.539325963893475, 0.525842814796138, 0.512359665698801]

SAMPLES_24_HOURS_SATURDAY_FALL_COMMERCIAL = [0.498876516601464, 0.485393367504127, 0.451685494760785, 0.444943920212117,
                                             0.444943920212117,
                                             0.43146077111478, 0.43146077111478, 0.444943920212117, 0.485393367504127,
                                             0.512359665698801,
                                             0.525842814796138, 0.539325963893475, 0.552809112990812, 0.552809112990812,
                                             0.546067538442144,
                                             0.532584389344807, 0.573033836636817, 0.620224858477496, 0.687640603964181,
                                             0.674157454866844,
                                             0.633708007574833, 0.620224858477496, 0.525842814796138, 0.512359665698801]

SAMPLES_24_HOURS_WEEKDAY_SPRING_COMMERCIAL = [0.458427069309454, 0.444943920212117, 0.43146077111478, 0.43146077111478,
                                              0.43146077111478,
                                              0.43146077111478, 0.451685494760785, 0.552809112990812, 0.714606902158854,
                                              0.808988945840213,
                                              0.856179967680892, 0.903370989521571, 0.910112564070239,
                                              0.910112564070239, 0.903370989521571,
                                              0.896629414972902, 0.876404691326897, 0.856179967680892,
                                              0.842696818583555, 0.822472094937549,
                                              0.808988945840213, 0.714606902158854, 0.633708007574833,
                                              0.532584389344807]

SAMPLES_24_HOURS_FRIDAY_SPRING_COMMERCIAL = [0.498876516601464, 0.485393367504127, 0.43146077111478, 0.43146077111478,
                                             0.438202345663448,
                                             0.438202345663448, 0.512359665698801, 0.552809112990812, 0.633708007574833,
                                             0.714606902158854,
                                             0.808988945840213, 0.815730520388881, 0.822472094937549, 0.808988945840213,
                                             0.755056349450865,
                                             0.714606902158854, 0.620224858477496, 0.525842814796138, 0.525842814796138,
                                             0.525842814796138,
                                             0.532584389344807, 0.525842814796138, 0.512359665698801, 0.525842814796138]

SAMPLES_24_HOURS_SATURDAY_SPRING_COMMERCIAL = [0.43146077111478, 0.43146077111478, 0.43146077111478, 0.43146077111478,
                                               0.424719196566112,
                                               0.411236047468775, 0.411236047468775, 0.411236047468775,
                                               0.43146077111478, 0.444943920212117,
                                               0.485393367504127, 0.525842814796138, 0.525842814796138,
                                               0.525842814796138,
                                               0.525842814796138, 0.525842814796138, 0.525842814796138,
                                               0.525842814796138,
                                               0.532584389344807, 0.55955068753948, 0.620224858477496,
                                               0.620224858477496, 0.620224858477496,
                                               0.471910218406791]

SAMPLES_24_HOURS_WEEKDAY_WINTER_COMMERCIAL = [0.438202345663448, 0.43146077111478, 0.417977622017443, 0.404494472920106,
                                              0.404494472920106,
                                              0.417977622017443, 0.43146077111478, 0.552809112990812, 0.633708007574833,
                                              0.728090051256191,
                                              0.755056349450865, 0.808988945840213, 0.808988945840213,
                                              0.808988945840213, 0.795505796742876,
                                              0.782022647645539, 0.808988945840213, 0.802247371291544,
                                              0.782022647645539, 0.728090051256191,
                                              0.701123753061518, 0.593258560282823, 0.525842814796138, 0.43146077111478]

SAMPLES_24_HOURS_FRIDAY_WINTER_COMMERCIAL = [0.478651792955459, 0.438202345663448, 0.43146077111478, 0.424719196566112,
                                             0.424719196566112,
                                             0.43146077111478, 0.485393367504127, 0.552809112990812, 0.620224858477496,
                                             0.714606902158854,
                                             0.728090051256191, 0.73483162580486, 0.728090051256191, 0.714606902158854,
                                             0.660674305769507,
                                             0.512359665698801, 0.525842814796138, 0.525842814796138, 0.525842814796138,
                                             0.525842814796138,
                                             0.498876516601464, 0.471910218406791, 0.438202345663448, 0.43146077111478]

SAMPLES_24_HOURS_SATURDAY_WINTER_COMMERCIAL = [0.43146077111478, 0.424719196566112, 0.417977622017443,
                                               0.404494472920106,
                                               0.404494472920106, 0.404494472920106, 0.404494472920106,
                                               0.411236047468775,
                                               0.417977622017443, 0.424719196566112, 0.43146077111478, 0.43146077111478,
                                               0.444943920212117,
                                               0.444943920212117, 0.444943920212117, 0.444943920212117,
                                               0.525842814796138,
                                               0.579775411185486, 0.620224858477496, 0.606741709380159,
                                               0.566292262088149,
                                               0.532584389344807, 0.485393367504127, 0.43146077111478]

################################## appartments profile ###############################################################

SAMPLES_24_HOURS_WEEKDAY_SUMMER_APPARTMENTS = [0.75, 0.65, 0.6, 0.58, 0.55, 0.55, 0.56, 0.57, 0.56, 0.57, 0.59, 0.61,
                                               0.65, 0.7, 0.8, 0.86,
                                               0.88, 0.9, 0.89, 0.89, 0.95, 1, 0.99, 0.87]

SAMPLES_24_HOURS_FRIDAY_SUMMER_APPARTMENTS = [0.74, 0.65, 0.6, 0.58, 0.55, 0.55, 0.54, 0.57, 0.6, 0.65, 0.7, 0.79, 0.84,
                                              0.92, 1.01, 1.08,
                                              1.1, 1.1, 1.09, 1.04, 1.03, 1.01, 0.99, 0.9]

SAMPLES_24_HOURS_SATURDAY_SUMMER_APPARTMENTS = [0.84, 0.75, 0.69, 0.65, 0.61, 0.6, 0.6, 0.61, 0.65, 0.71, 0.8, 0.9,
                                                0.98, 1.01, 1.05, 1.09,
                                                1.11, 1.19, 1.18, 1.18, 1.14, 1.1, 1.06, 0.95]

SAMPLES_24_HOURS_WEEKDAY_FALL_APPARTMENTS = [0.43, 0.38, 0.34, 0.32, 0.32, 0.36, 0.4, 0.46, 0.41, 0.4, 0.39, 0.4, 0.4,
                                             0.41, 0.46, 0.47, 0.48,
                                             0.52, 0.6, 0.63, 0.66, 0.66, 0.6, 0.51]

SAMPLES_24_HOURS_FRIDAY_FALL_APPARTMENTS = [0.48, 0.41, 0.39, 0.36, 0.36, 0.38, 0.4, 0.46, 0.46, 0.48, 0.5, 0.52, 0.57,
                                            0.62, 0.7, 0.7,
                                            0.79, 0.81, 0.86, 0.81, 0.78, 0.71, 0.68, 0.6]

SAMPLES_24_HOURS_SATURDAY_FALL_APPARTMENTS = [0.52, 0.46, 0.42, 0.4, 0.4, 0.41, 0.4, 0.46, 0.47, 0.52, 0.58, 0.61, 0.63,
                                              0.64, 0.62, 0.63,
                                              0.64, 0.69, 0.74, 0.72, 0.71, 0.69, 0.6, 0.58]

SAMPLES_24_HOURS_WEEKDAY_SPRING_APPARTMENTS = [0.41, 0.35, 0.3, 0.3, 0.3, 0.32, 0.4, 0.47, 0.45, 0.4, 0.38, 0.37, 0.37,
                                               0.37, 0.41, 0.41, 0.42,
                                               0.46, 0.52, 0.6, 0.67, 0.66, 0.6, 0.52]

SAMPLES_24_HOURS_FRIDAY_SPRING_APPARTMENTS = [0.42, 0.35, 0.3, 0.3, 0.3, 0.32, 0.36, 0.43, 0.46, 0.46, 0.46, 0.46, 0.5,
                                              0.51, 0.55, 0.56,
                                              0.58, 0.63, 0.7, 0.76, 0.71, 0.66, 0.6, 0.52]

SAMPLES_24_HOURS_SATURDAY_SPRING_APPARTMENTS = [0.47, 0.4, 0.37, 0.36, 0.35, 0.36, 0.37, 0.41, 0.44, 0.46, 0.5, 0.52,
                                                0.51, 0.51, 0.5, 0.49,
                                                0.49, 0.52, 0.56, 0.62, 0.69, 0.66, 0.6, 0.52]

SAMPLES_24_HOURS_WEEKDAY_WINTER_APPARTMENTS = [0.51, 0.41, 0.35, 0.33, 0.35, 0.4, 0.51, 0.63, 0.58, 0.5, 0.46, 0.43,
                                               0.43, 0.44, 0.48, 0.49,
                                               0.53, 0.66, 0.81, 0.9, 0.94, 0.91, 0.82, 0.68]

SAMPLES_24_HOURS_FRIDAY_WINTER_APPARTMENTS = [0.54, 0.45, 0.4, 0.36, 0.36, 0.4, 0.49, 0.58, 0.61, 0.59, 0.59, 0.59,
                                              0.59, 0.62, 0.7, 0.75,
                                              0.86, 0.9, 1.01, 0.97, 0.9, 0.86, 0.78, 0.68]

SAMPLES_24_HOURS_SATURDAY_WINTER_APPARTMENTS = [0.56, 0.5, 0.45, 0.41, 0.42, 0.45, 0.49, 0.5, 0.52, 0.6, 0.62, 0.62,
                                                0.59, 0.58, 0.57, 0.57,
                                                0.6, 0.72, 0.9, 0.96, 0.91, 0.87, 0.78, 0.68]

##################################commercial and appartments profile ###############################################################

SAMPLES_24_HOURS_WEEKDAY_SUMMER_COMMERCIAL_APPARTMENTS = [0.732046333176906, 0.676447877492584, 0.634749035729342,
                                                          0.625482626448622, 0.611583012527541,
                                                          0.620849421808262, 0.639382240369702, 0.769111970299787,
                                                          0.898841700229871, 0.986872588396714,
                                                          1.07490347656356, 1.093436295125, 1.12586872760752,
                                                          1.1629343647304, 1.20000000185328,
                                                          1.20000000185328, 1.16756756937076, 1.1629343647304,
                                                          1.14440154616896, 1.14440154616896,
                                                          1.08416988584428, 0.986872588396714, 0.898841700229871,
                                                          0.801544402782308]

SAMPLES_24_HOURS_FRIDAY_SUMMER_COMMERCIAL_APPARTMENTS = [0.750579151738346, 0.718146719255825, 0.671814672852223,
                                                         0.634749035729342,
                                                         0.634749035729342, 0.634749035729342, 0.681081082132944,
                                                         0.764478765659427,
                                                         0.898841700229871, 0.986872588396714, 1.07490347656356,
                                                         1.11196911368644, 1.1629343647304,
                                                         1.17683397865148, 1.17220077401112, 1.15366795544968,
                                                         1.01930502087924, 0.996138997677435,
                                                         0.986872588396714, 0.982239383756354, 0.935907337352753,
                                                         0.917374518791312,
                                                         0.898841700229871, 0.810810812063028]

SAMPLES_24_HOURS_SATURDAY_SUMMER_COMMERCIAL_APPARTMENTS = [0.769111970299787, 0.722779923896185, 0.681081082132944,
                                                           0.648648649650423,
                                                           0.634749035729342, 0.634749035729342, 0.625482626448622,
                                                           0.634749035729342,
                                                           0.681081082132944, 0.722779923896185, 0.810810812063028,
                                                           0.85714285846663,
                                                           0.903474904870232, 0.940540541993113, 0.972972974475634,
                                                           0.977606179115994,
                                                           0.977606179115994, 0.972972974475634, 0.959073360554553,
                                                           0.986872588396714,
                                                           0.991505793037075, 0.954440155914193, 0.898841700229871,
                                                           0.810810812063028]

SAMPLES_24_HOURS_WEEKDAY_FALL_COMMERCIAL_APPARTMENTS = [0.546718147562499, 0.514285715079978, 0.467953668676376,
                                                        0.458687259395656, 0.458687259395656,
                                                        0.477220077957097, 0.546718147562499, 0.639382240369702,
                                                        0.727413128536545, 0.796911198141948,
                                                        0.824710425984109, 0.85714285846663, 0.87567567702807,
                                                        0.86177606310699, 0.898841700229871,
                                                        0.889575290949151, 0.87104247238771, 0.898841700229871,
                                                        0.935907337352753, 0.917374518791312,
                                                        0.898841700229871, 0.820077221343749, 0.727413128536545,
                                                        0.634749035729342]

SAMPLES_24_HOURS_FRIDAY_FALL_COMMERCIAL_APPARTMENTS = [0.593050193966101, 0.546718147562499, 0.523552124360698,
                                                       0.509652510439618,
                                                       0.509652510439618, 0.542084942922139, 0.551351352202859,
                                                       0.648648649650423,
                                                       0.732046333176906, 0.810810812063028, 0.86640926774735,
                                                       0.898841700229871, 0.926640928072032,
                                                       0.908108109510592, 0.898841700229871, 0.85714285846663,
                                                       0.787644788861227, 0.783011584220867,
                                                       0.820077221343749, 0.796911198141948, 0.759845561019066,
                                                       0.722779923896185,
                                                       0.694980696054024, 0.634749035729342]

SAMPLES_24_HOURS_SATURDAY_FALL_COMMERCIAL_APPARTMENTS = [0.58378378468538, 0.546718147562499, 0.523552124360698,
                                                         0.509652510439618,
                                                         0.509652510439618, 0.528185329001058, 0.518918919720338,
                                                         0.509652510439618,
                                                         0.546718147562499, 0.58378378468538, 0.620849421808262,
                                                         0.644015445010062,
                                                         0.662548263571503, 0.681081082132944, 0.671814672852223,
                                                         0.671814672852223,
                                                         0.671814672852223, 0.722779923896185, 0.773745174940147,
                                                         0.810810812063028,
                                                         0.796911198141948, 0.769111970299787, 0.713513514615465,
                                                         0.634749035729342]

SAMPLES_24_HOURS_WEEKDAY_SPRING_COMMERCIAL_APPARTMENTS = [0.528185329001058, 0.458687259395656, 0.444787645474575,
                                                          0.444787645474575, 0.444787645474575,
                                                          0.458687259395656, 0.514285715079978, 0.625482626448622,
                                                          0.704247105334745, 0.722779923896185,
                                                          0.769111970299787, 0.783011584220867, 0.801544402782308,
                                                          0.810810812063028, 0.820077221343749,
                                                          0.806177607422668, 0.806177607422668, 0.810810812063028,
                                                          0.824710425984109, 0.85714285846663,
                                                          0.86177606310699, 0.810810812063028, 0.722779923896185,
                                                          0.634749035729342]

SAMPLES_24_HOURS_FRIDAY_SPRING_COMMERCIAL_APPARTMENTS = [0.546718147562499, 0.486486487237817, 0.458687259395656,
                                                         0.444787645474575,
                                                         0.449420850114936, 0.458687259395656, 0.514285715079978,
                                                         0.593050193966101,
                                                         0.657915058931143, 0.722779923896185, 0.769111970299787,
                                                         0.783011584220867,
                                                         0.801544402782308, 0.810810812063028, 0.783011584220867,
                                                         0.732046333176906,
                                                         0.685714286773304, 0.671814672852223, 0.685714286773304,
                                                         0.722779923896185,
                                                         0.713513514615465, 0.745945947097986, 0.634749035729342,
                                                         0.5698841707643]

SAMPLES_24_HOURS_SATURDAY_SPRING_COMMERCIAL_APPARTMENTS = [0.528185329001058, 0.491119691878177, 0.458687259395656,
                                                           0.454054054755296,
                                                           0.449420850114936, 0.458687259395656, 0.458687259395656,
                                                           0.467953668676376,
                                                           0.495752896518537, 0.542084942922139, 0.56061776148358,
                                                           0.593050193966101,
                                                           0.593050193966101, 0.593050193966101, 0.58378378468538,
                                                           0.57915058004502,
                                                           0.58378378468538, 0.611583012527541, 0.634749035729342,
                                                           0.699613900694384,
                                                           0.722779923896185, 0.667181468211863, 0.708880309975105,
                                                           0.634749035729342]

SAMPLES_24_HOURS_WEEKDAY_WINTER_COMMERCIAL_APPARTMENTS = [0.546718147562499, 0.472586873316736, 0.444787645474575,
                                                          0.444787645474575, 0.444787645474575,
                                                          0.467953668676376, 0.546718147562499, 0.690347491413664,
                                                          0.722779923896185, 0.732046333176906,
                                                          0.741312742457626, 0.741312742457626, 0.741312742457626,
                                                          0.745945947097986, 0.750579151738346,
                                                          0.750579151738346, 0.750579151738346, 0.85714285846663,
                                                          0.926640928072032, 0.954440155914193,
                                                          0.945173746633473, 0.898841700229871, 0.810810812063028,
                                                          0.56525096612394]

SAMPLES_24_HOURS_FRIDAY_WINTER_COMMERCIAL_APPARTMENTS = [0.57451737540466, 0.518918919720338, 0.477220077957097,
                                                         0.458687259395656,
                                                         0.458687259395656, 0.500386101158897, 0.546718147562499,
                                                         0.644015445010062,
                                                         0.722779923896185, 0.741312742457626, 0.759845561019066,
                                                         0.769111970299787,
                                                         0.773745174940147, 0.769111970299787, 0.759845561019066,
                                                         0.750579151738346,
                                                         0.750579151738346, 0.787644788861227, 0.829343630624469,
                                                         0.810810812063028,
                                                         0.769111970299787, 0.727413128536545, 0.690347491413664,
                                                         0.56061776148358]

SAMPLES_24_HOURS_SATURDAY_WINTER_COMMERCIAL_APPARTMENTS = [0.551351352202859, 0.518918919720338, 0.481853282597457,
                                                           0.458687259395656,
                                                           0.458687259395656, 0.495752896518537, 0.495752896518537,
                                                           0.495752896518537,
                                                           0.528185329001058, 0.546718147562499, 0.593050193966101,
                                                           0.602316603246821,
                                                           0.593050193966101, 0.58378378468538, 0.57451737540466,
                                                           0.56525096612394,
                                                           0.58378378468538, 0.681081082132944, 0.810810812063028,
                                                           0.86177606310699,
                                                           0.824710425984109, 0.810810812063028, 0.732046333176906,
                                                           0.555984556843219]


#############################################END YEARLY PROFILES%#######################################################


def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = arr.max() - arr.min()
    for i in arr:
        temp = (((i - arr.min()) * diff) / diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr


def week(number_of_sampling, samples_day, samples_friday, samples_saturday, mu_start):
    mu_arr = np.arange(mu_start, mu_start + mu_step, 0.25)  # flexible
    loadprofile = np.zeros((7, number_of_sampling))
    loadprofile_scale = np.zeros((7, number_of_sampling))
    sevenDaysls = []

    for e in range(7):

        random_index_coise = []
        for item in range(0, len(mu_arr)):
            random_index_coise.append(item)

        index = random.choice(random_index_coise)
        while True:
            if math.isnan(mu_arr[index]):
                index = random.choice(random_index_coise)
            else:
                break

        curr_mu = mu_arr[index]
        mu_arr[index] = np.NaN
        if (e < 6):

            # TODO add rescale function
            for h in range(number_of_sampling):
                sevenDaysls.append(samples_day[h] * (1 + curr_mu * abs(samples_day[h])) / np.log(1 + curr_mu))
        if (e == 6):
            for h in range(number_of_sampling):
                sevenDaysls.append(samples_friday[h] * (1 + curr_mu * abs(samples_friday[h])) / np.log(1 + curr_mu))
        if (e == 7):
            for h in range(number_of_sampling):
                sevenDaysls.append(samples_saturday[h] * (1 + curr_mu * abs(samples_saturday[h])) / np.log(1 + curr_mu))

    sevenDays = np.array(sevenDaysls)
    sevenDaysscaled = normalize(sevenDays, min(samples_day), max(samples_day))
    return sevenDaysscaled


def season(number_of_weeks_in_season, number_of_sampling, samples_day, samples_friday, samples_saturday, mu_start):
    seasonls = []
    for i in range(number_of_weeks_in_season):
        weekdata = week(number_of_sampling, samples_day, samples_friday, samples_saturday, mu_start)
        seasonls.extend(weekdata)
        mu_start = mu_start + mu_step
    return seasonls


def year(number_of_weeks_in_season_summer, number_of_sampling, samples_day_summer, samples_friday_summer,
         samples_saterday_summer,
         mu_start_summer,
         number_of_weeks_in_season_winter, samples_day_winter, samples_friday_winter, samples_saterday_winter,
         mu_start_winter,
         number_of_weeks_in_season_fall, samples_day_fall, samples_friday_fall, samples_saterday_fall, mu_start_fall,
         number_of_weeks_in_season_spring, samples_day_spring, samples_friday_spring, samples_saterday_spring,
         mu_start_spring):
    yearls = []
    season_winter = season(number_of_weeks_in_season_winter, number_of_sampling, samples_day_winter,
                           samples_friday_winter,
                           samples_saterday_winter, mu_start_winter)
    yearls.extend(season_winter)
    season_spring = season(number_of_weeks_in_season_spring, number_of_sampling, samples_day_spring,
                           samples_friday_spring,
                           samples_saterday_spring, mu_start_spring)
    yearls.extend(season_spring)
    season_summer = season(number_of_weeks_in_season_summer, number_of_sampling, samples_day_summer,
                           samples_friday_summer,
                           samples_saterday_summer, mu_start_summer)
    yearls.extend(season_summer)
    season_fall = season(number_of_weeks_in_season_fall, number_of_sampling, samples_day_fall, samples_friday_fall,
                         samples_saterday_fall, mu_start_fall)
    yearls.extend(season_fall)
    yearls.extend(samples_day_fall)
    YEAR = yearls

    # t = [i for i in range(EXAMINE_EVERY_HOUR)]
    # d = np.array([t, YEAR])
    #
    # plt.scatter(d[0, :], d[1, :], label='original', zorder=10, linewidths=0.1)
    # plt.legend()
    #
    # plt.show()
    return yearls
