import numpy as np
import pdb

pre = np.loadtxt('./APRE')
post = np.loadtxt('./DESIREDA')

possible_mins = np.arange(-110,10)

f_pre = pre[0:9]
f_post = post[0:9]

all_ys = []
'''
def span_map(possible_min):
  spans = []
  for i, source in enumerate(f_pre):
    valid_span = 255/ f_post[i] * (source - possible_min)
    spans.append(valid_span)
  return spans

for possible_min in possible_mins:
  spans = span_map(possible_min)
  #pdb.set_trace()
  norm_spans = spans / np.sum(spans)
  all_ys.append(np.sum([ np.abs(elem / norm_spans[0]) - 1 for elem in norm_spans ]) )

a = np.min(np.abs(all_ys))
vals = [ i for i, elem in enumerate(all_ys) if elem == a ] 
pdb.set_trace()
    
'''
print([-(f_post[i] / 25.5 - f_pre[i]) for i,post in enumerate(f_post)] )
pdb.set_trace()
#f_post * 25.5 - f_pre =

#f_post * 25.5= f_pre - x 



'''
post = (pre - min) / span  * 255
post / 255= (pre-min) / span
255 / post = span / (pre - min)
span = 255/post * (pre-min) 

[min, max]
[0, max - min]
[0, span/ (max-min)]
[0, span/ (max-min)]
[0, span/ (max-min) * 255]
'''
