from mip import *

m = Model(sense=MAXIMIZE, solver_name=CBC) # use GRB for Gurobi
hostImageWidth = 500 
hostImageHeight = 1000
strLength = 4000
 
qrcodeImageWidth = m.add_var(name='qrcodeImageWidth', var_type=INTEGER, lb=0) # height of QR code image
qrcodeModule = m.add_var(name='qrcodeModule', var_type=INTEGER, lb=35, ub=40) # how many cells in a QR code TODO
qrcodeCellNum = m.add_var(name='qrcodeCellNum', var_type=INTEGER, lb=1) # how many pixels in the side of cell 
qrcodeNum = m.add_var(name='qrcodeNum', var_type=INTEGER, lb=0) # how many qr code within host image
errorLevel = m.add_var(name='errorLevel', var_type=INTEGER, lb=2, ub=4) # the error correction level of QR code TODO
qrcodeStrLength = m.add_var(name='qrcodeStrLength', var_type=INTEGER, lb=0) # the encoding string length in QR code


# m += ((qrcodeModule * 4 + 17) * qrcodeCellNum) * ((qrcodeModule * 4 + 17) * qrcodeCellNum) * qrcodeNum <= 500000
# m += qrcodeImageWidth == (qrcodeModule * 4 + 17) * qrcodeCellNum
m += qrcodeModule <= 500000
m += qrcodeStrLength >= 4000
# m += qrcodeStrLength * qrcodeNum >= 4000
m += errorLevel*qrcodeModule >= qrcodeStrLength
# m += ((errorLevel - 2) * 0.5 + 1.3) * (qrcodeModule * (qrcodeModule - 8)) >= qrcodeStrLength

m.objective = maximize(qrcodeImageWidth)

m.max_gap = 0.05
status = m.optimize(max_seconds=300)
if status == OptimizationStatus.OPTIMAL:
    print('optimal solution cost {} found'.format(m.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('solution:')
    for v in m.vars:
       if abs(v.x) > 1e-6: # only printing non-zeros
          print('{} : {}'.format(v.name, v.x))







