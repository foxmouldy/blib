from tasks import *
from taskinit import *
import casac

import sys
from optparse import OptionParser
import pylab as pl

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

# O1 for Option

parser.add_option("--ra", type='string', dest='ra', default='10h00m00.0s', 
		help="Right Ascension of Target [10h00m00.0s]")

parser.add_option("--dec", type='string', dest='dec', default='-30d00m00.0s', 
		help="Declination of Target [-30d00m00.0s]")

parser.add_option("-f", type='string', dest='f', default="noise", 
		help = "Name for output files [noise]")

(options, args) = parser.parse_args();

direction = "J2000 "+options.ra+" "+options.dec;

cl.done()
cl.addcomponent(dir=direction, flux=0.0, fluxunit='Jy', freq='1.420GHz',
		shape="point")

ia.fromshape(options.f+".im",[8192,8192,1,1],overwrite=True)

noise = pl.randn(8192,8192,1,1);

ia.fromarray(options.f+".im", pixels=noise, overwrite=True)
cs=ia.coordsys()
cs.setunits(['rad','rad','','Hz'])
cell_rad=qa.convert(qa.quantity("1arcsec"),"rad")['value']
cs.setincrement([-cell_rad,cell_rad],'direction')
cs.setreferencevalue([qa.convert(options.ra,'rad')['value'],qa.convert(options.dec,'rad')['value']],type="direction")
cs.setreferencevalue("1.0GHz",'spectral')
cs.setincrement('50kHz','spectral')
ia.setcoordsys(cs.torecord())
ia.setbrightnessunit("Jy/pixel")
ia.modify(cl.torecord(),subtract=False)
exportfits(imagename=options.f+'.im',fitsimage=options.f+'.fits',overwrite=True)
