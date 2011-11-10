"""
    MoinMoin - Python Source Parser
"""

# Imports
import cgi, string, sys, cStringIO
import keyword, token, tokenize


#############################################################################
### Python Source Parser (does Hilighting)
#############################################################################

RealClasses = [ 'Point','FreePoint','Centroid',
'OrthoCenter', 'InCenter', 'ExCenter', 'CircumCenter',
'TetraCenter', 'PlaneLineIntersect', 'LinesIntersect',
'PlanesIntersect', 'Circle_AntiPodal', 'Sphere_AntiPodal',
'SpherePole', 'CirclePole', 'CircleInversion', 'SphereInversion',
'PlaneReflection', 'LineReflection', 'LineSlider', 'PlaneSlider',
'CircleSlider', 'SphereSlider', 'PlaneFoot', 'LineFoot',
'LineDivider', 'LineCut', 'CrossPoint', 'Harmonic',
'SegPoint', 'CircumPoint',
'CirclingPoint', 'SlidingPoint', 'LineFromPoints', 'PlanePerp',
'PlanesLine', 'ParaLine', 'Transversal',
'CircleChord', 'SphereChord', 'TangChord', 'BiChord',
'TangPlanes', 'PlaneFromPoints', 'ParaPlane', 'PerpPlane',
'PlaneFromNormal', 'PolarPlane', 'CircleOnPlane',
'CircumCircle', 'CenterCircle','InscribedCircle',
'ExscribedCircle', 'OrthoCircle','SphereCircle', 'SpheresIntersect',
'CenterSphere', 'OrthoSphere', 'CircumSphere',
'Triangle', 'FreeVector', 'CrossVector','SegmentPencil', 'CirclingPencil',
'CirclePoints', 'Conic', 'ArrayIntersect', 'Bezier', 'PcCurve',
'CirclingLines', 'Regulus', 'PointMap', 'ArrayMap', 'PlanesPencilIntersect',
'Lines', 'PlaneArray', 'CirclePencil', 'CentralProjection', 'Reflect_in_Plane']

ComplexClasses = ['rPoint', 'R_FreePosition', 'rPole', 'rLine', 'Sphere_Point', 'uPolarPoint',
 'z_to_uPoint', 'uAntiPodal', 'uInversePoint', 'uCirclingPoint','uSpiral',
 'uSphereSlider', 'uCircleSlider', 'uCircumCircle', 'z_to_uCircle',
 'uCircleFromNormal','uPolarCircle', 'uSphereSlices', 'z_to_uCirclePencil',
 'zFixedPoint', 'zFreePoint', 'zPolarPoint', 'zOrthoPoint', 'zConjugate', 'R_tozPoint',
 'zInversePoint', 'zPowerPoint', 'zRotation','R_Rotation', 'zCircumPoint',
 'zHarmonic', 'zCircleSlider', 'zSlidingPoint', 'zCirclingPoint', 'zLineFromPoints',
 'zBiChord','zCircleFromPoints', 'zCircumCircle', 'zOrthoCircle',
 'zOrthoCircle_Circum', 'zInverseCircle', 'u_to_zCircle', 'zFundamentalCircle',
 'zCirclePencil', 'u_to_zCirclePencil','Z_Plane', 'Unit_Circle', 'uSphere','K_Sphere']


AbstractClasses = ['Element', '_Point', '_Line', '_zPoint', '_Plane',
'_Circle', '_zCircle', 'SegPoint', '_Sphere',
'_PointArray', '_Curve', '_LineArray', '_PlaneArray',
'_CirclePencil',  'zCirclePencil', '_Transformation','_zLine']


RealDefs = ['Center', 'Intersect', 'AntiPodal', 'Pole','Reflection',
'Slider', 'Foot', 'Divider', 'AniPoint', 'Line', 'Chord', 'Plane',
'Circle', 'Sphere', 'PointArray', 'Curve', 'LineArray', 'Transform']

ComplexDefs = ['uPoint', 'uAniPoint', 'uSlider', 'uCircle', 'U_Pencil', 'zPoint', 'zAniPoint', 'zLine',
 'zCircle', 'zPencil']

ElementKeys = ['color','initcolor','trace','level','texture','extend','povout','label'
'linewidth','style','density','precision','density','scale',
'drawradius','drawpoints', 'pointsize','density', 'fixed',
'seg','opposite', 'circle_type','show_normal','normal_width','tracewidth',
'tracecolor','maxtrace','mintrace',  'fontsize','fontcolor',
'fontXofffset','fontYofffset', 'linewidth','label_ratio','angle','rate',
'drawlen']

SceneKeys = ['width','height','background','scale','title','center','panel','instruction',
 'explanation','reference','trace_on','observe_on','test_real','view_drag','panel_x',
'panel_y','scene_x','scene_y','axis','povout','frames','delay','pov_name','pov_directory',
'camera_vector']


PyGeoConstants = ['BLACK', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'DARKGRAY',
'LIGHTGRAY', 'BROWN', 'ORANGE', 'PINK', 'PURPLE', 'VERYLIGHT', 'WHITE',
'GeoLEFT', 'GeoCENTER', 'GeoRIGHT', 'GeoTOP', 'GeoBOTTOM',
'TINYFONT', 'SMALLFONT', 'NORMALFONT', 'LARGEFONT', 'VERYLARGEFONT',
'LINES', 'FILL', 'OUTLINE', 'POINTS', 'IMAGE',
'MAX', 'BEGIN', 'END',
'CENTER', 'CIRCUMCIRCLE', 'CIRCUM', 'CIRCUM_CIRCLE',
'INSCRIBED', 'EXSCRIBED', 'ORTHO', 'ORTHOCENTER',
'ORTHO_CENTER', 'INCENTER', 'IN_CENTER', 'EXCENTER',
'EX_CENTER', 'CIRCUMCENTER', 'CIRCUM_CENTER', 'CENTROID',
'INVERSE', 'FUNDAMENTAL', 'zFixedPoint', 'POLAR', 'CONJUGATE',
'POV_INCLUDE']


PyGeoClasses=RealClasses+ComplexClasses+AbstractClasses
PyGeoKeys=ElementKeys+SceneKeys
PyGeoDefs=RealDefs + ComplexDefs




_KEYWORD = token.NT_OFFSET + 1
_TEXT    = token.NT_OFFSET + 2
_PYGEO_ELEMENT = token.NT_OFFSET + 3
_PYGEO_KW  = token.NT_OFFSET + 4
_PYGEO_CONSTANTS  = token.NT_OFFSET + 5
_PYGEO_DEFS  = token.NT_OFFSET + 6


_colors = {
    token.NUMBER:       '#0080C0',
    token.OP:           '#0000C0',
    token.STRING:       '#FF4080',
    tokenize.COMMENT:   '#008000',
    token.NAME:         '#000000',
    token.ERRORTOKEN:   '#FF8080',
    _KEYWORD:           '#C00000',
    _PYGEO_ELEMENT:      '#06aa62',
    _PYGEO_KW:           '#474782',
    _PYGEO_CONSTANTS:    '#f86882',
    _PYGEO_DEFS:        '#3a27c6',
    _TEXT:              '#000000',
}



class Parser:
    """ Send colored python source.
    """

    def __init__(self, raw, out = sys.stdout,name=None):
        """ Store the source text.
        """
        self.raw = string.strip(string.expandtabs(raw))
        self.out = out

        header =      '<html> \n <head> <title>%s' %name + '</title>' +\
        '<link rel="stylesheet" href="../geostyle.css" type="text/css" />' +\
        '<body> \n' +\
        '<table class = "TopIndex"> <tr> <td> \n' +\
        '<h1 align="center">' + name + '</h1> \n'

        self.out.write(header)
        self.format()
        self.out.write('\n </td> </tr> </table> </body> \n </html>')


    def format(self):#, formatter, form):
        """ Parse and send the colored source.
        """
        # store line offsets in self.lines
        self.lines = [0, 0]
        pos = 0
        while 1:
            pos = string.find(self.raw, '\n', pos) + 1
            if not pos: break
            self.lines.append(pos)
        self.lines.append(len(self.raw))

        # parse the source and write it
        self.pos = 0
        text = cStringIO.StringIO(self.raw)
        self.out.write('<pre><font face="Lucida,Courier New">')
        try:
            tokenize.tokenize(text.readline, self)
        except tokenize.TokenError, ex:
            msg = ex[0]
            line = ex[1][0]
            self.out.write("<h3>ERROR: %s</h3>%s\n" % (
                msg, self.raw[self.lines[line]:]))
        self.out.write('</font></pre>')

    def __call__(self, toktype, toktext, (srow,scol), (erow,ecol), line):
        """ Token handler.
        """
        if 0:
            print "type", toktype, token.tok_name[toktype], "text", toktext,
            print "start", srow,scol, "end", erow,ecol, "<br>"

        # calculate new positions
        oldpos = self.pos
        newpos = self.lines[srow] + scol
        self.pos = newpos + len(toktext)

        # handle newlines
        if toktype in [token.NEWLINE, tokenize.NL]:
            self.out.write('\n')
            return

        # send the original whitespace, if needed
        if newpos > oldpos:
            self.out.write(self.raw[oldpos:newpos])

        # skip indenting tokens
        if toktype in [token.INDENT, token.DEDENT]:
            self.pos = newpos
            return

        # map token type to a color group
        if token.LPAR <= toktype and toktype <= token.OP:
            toktype = token.OP
        elif toktype == token.NAME:
           if keyword.iskeyword(toktext):
              toktype = _KEYWORD
           if toktext in PyGeoClasses:
              toktype = _PYGEO_ELEMENT
           if toktext in PyGeoKeys:
              toktype = _PYGEO_KW
           if toktext in PyGeoConstants:
              toktype = _PYGEO_CONSTANTS
           if toktext in PyGeoDefs:
              toktype = _PYGEO_DEFS

        color = _colors.get(toktype, _colors[_TEXT])

        style = ''
        if toktype == token.ERRORTOKEN:
            style = ' style="border: solid 1.5pt #FF0000;"'

        # send text
        self.out.write('<font color="%s"%s>' % (color, style))
        self.out.write(cgi.escape(toktext))
        self.out.write('</font>')


def colorize(argv):
      import os,sys,string
      print argv[1]
      source = open(argv[1]).read()
      base= string.split(argv[1],".")
      name= string.split(argv[1],'\\')
      out=base[-2] + ".html"
      print base[-2]
      file=open(out,'w')
      Parser(source,file,name=name[-1])
      if len(argv)==3:
         if argv[2]=='show':  # load HTML page into browser
            if os.name == "nt":
                os.system("explorer %s" %out)
            else:
                os.system("netscape out &")

if __name__ == "__main__":
    colorize(sys.argv)
