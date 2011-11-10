
PyGeoConstants = ['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'DARKGRAY',
'LIGHTGRAY', 'BROWN', 'ORANGE', 'PINK', 'PURPLE', 'VERYLIGHT', 'WHITE',
'GeoLEFT', 'GeoCENTER', 'GeoRIGHT', 'GeoTOP', 'GeoBOTTOM',
'TINYFONT', 'SMALLFONT', 'NORMALFONT', 'LARGEFONT', 'VERYLARGEFONT',
'LINES', 'FILL', 'OUTLINE', 'POINTS', 'IMAGE',
 'BEGIN', 'END',
'CENTER', 'CIRCUMCIRCLE', 'CIRCUM', 'CIRCUM_CIRCLE',
'INSCRIBED', 'EXSCRIBED', 'ORTHO', 'ORTHOCENTER',
'ORTHO_CENTER', 'INCENTER', 'IN_CENTER', 'EXCENTER',
'EX_CENTER', 'CIRCUMCENTER', 'CIRCUM_CENTER', 'CENTROID',
'INVERSE', 'FUNDAMENTAL', 'ZPOINT', 'POLAR', 'CONJUGATE','PLANE','TRIANGLE','ALPHABET','alphabet',
'POV_INCLUDE','TRANSLATE','MULTIPLY']




__all__=PyGeoConstants

#color constants
BLACK=(0.0,0.0,0.0)
RED=(1.0,0.0,0.0)
GREEN=(0.0,1.0,0.0)
YELLOW=(1.0,1.0,0.0)
BLUE=(0.0,0.0,1.0)
MAGENTA=(1.0,0.0,1.0)
CYAN=(0.0,1.0,1.0)
DARKGRAY=(0.25,0.25,0.25)
LIGHTGRAY=(0.75,0.75,0.75)
BROWN=(0.6,0.4,0.12)
ORANGE=(0.98,0.625,0.12)
PINK=(0.98,0.04,0.7)
PURPLE=(0.60,0.40,0.70)
VERYLIGHT=(0.97,0.97,0.97)
WHITE=(1.0,1.0,1.0)


#font alignment constants
GeoLEFT=1
GeoCENTER=2
GeoRIGHT=3
GeoTOP=4
GeoBOTTOM=5

#font sizes
TINYFONT  =10
SMALLFONT=15
NORMALFONT=20
LARGEFONT=25
VERYLARGEFONT=30

#draw style constants
LINES=1
FILL=2
OUTLINE=3
POINTS=4
IMAGE=5



#maximum coordinate value

#for SegPoints
BEGIN=0
END=1
#for circles
CENTER=0
CIRCUMCIRCLE=CIRCUM=CIRCUM_CIRCLE=1
INSCRIBED=2
EXSCRIBED=3

#for 3 points
ORTHO          =1
ORTHOCENTER    =1
ORTHO_CENTER   =1
INCENTER       =2
IN_CENTER      =2
EXCENTER       =3
EX_CENTER      =3
CIRCUMCENTER   =4
CIRCUM_CENTER  =4
CENTROID       =5

#for planes:

PLANE = 0
TRIANGLE       =1

#for 2 zCircles

INVERSE = 1
FUNDAMENTAL=2

#for mobTransforms
TRANSLATE=1
MULTIPLY=2

#for zPoints

ZPOINT =2
POLAR = 3
CONJUGATE = 4

alphabet=['a','b','c','d','e','f',
          'g','h','i','j','k','l',
          'm','n','o','p','q','r',
          's','t','u','v','w','x',
          'y','z']

ALPHABET=['A','B','C','D','E','F',
          'G','H','I','J','K','L',
          'M','N','O','P','Q','R',
          'S','T','U','V','W','X',
          'Y','Z']
POV_INCLUDE = ['colors.inc', 'textures.inc', 'stones.inc', 'metals.inc','glass.inc']
