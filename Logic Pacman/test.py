from spade import pyxf
myXsb=  pyxf.xsb("/Users/muthukumarsuresh/Downloads/XSB/bin/xsb")
myXsb.load('program.P')
myXsb.load('program2.P')
result = myXsb.query('q(X)')
print(result)