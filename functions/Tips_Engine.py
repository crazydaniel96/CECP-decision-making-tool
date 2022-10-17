import pages
import difflib
from difflib import SequenceMatcher
from heapq import nlargest as _nlargest

#1ST METHOD

def Tips(value):
  devices=[]
  med_fields=[]
  manufacturer=[]
  dev_type=[]
  for index,item in pages.devices.iterrows():
    if value.lower() in item['name'].lower():
        devices.append(item)
    if len(devices)>5:
        break
  for item in pages.med_field:
    if value.lower() in item.lower():
      med_fields.append(item)
    if len(med_fields)>5:
      break
  for item in pages.manufacturer:
    if value.lower() in item.lower():
      manufacturer.append(item)
    if len(manufacturer)>5:
      break
  for item in pages.dev_type:
    if value.lower() in item.lower():
      dev_type.append(item)
    if len(dev_type)>5:
      break
  
  total=[]
  i=0
  while i<6 and len(total)<8:
    if len(devices)>i:
      tmp=devices[i]['name']
      total.append({
                    'label': tmp[0:30]+"..." if len(tmp)>30 else tmp,
                    'value': "id&="+str(devices[i]['device_id']),
                    'title':tmp,
                })
    if len(med_fields)>i:
      total.append({
                    'label': med_fields[i],
                    'value': "mf&="+med_fields[i],
                    'title':med_fields[i],
                })
    if len(manufacturer)>i:
      total.append({
                    'label': manufacturer[i][0:30]+"..." if len(manufacturer[i])>30 else manufacturer[i],
                    'value': "man&="+manufacturer[i],
                    'title':manufacturer[i],
                })
    if len(dev_type)>i:
      total.append({
                    'label': dev_type[i][0:30]+"..." if len(dev_type[i])>30 else dev_type[i],
                    'value': "dt&="+dev_type[i],
                    'title':dev_type[i],
                })
    i+=1
  return total


#2ND METHOD

def Tips2(value):
  devices=pages.devices.iloc[get_close_matches_indexes(value,pages.devices["name"], n=5,cutoff=0.2)]
  med_fields=difflib.get_close_matches(value,pages.med_field, n=5,cutoff=0.2)
  manufacturer=difflib.get_close_matches(value,pages.manufacturer, n=5,cutoff=0.2)
  dev_type=difflib.get_close_matches(value,pages.dev_type, n=5,cutoff=0.2)
  total=[]
  i=0
  while i<6 and len(total)<8:
    if len(devices)>i:
      tmp=devices['name'].iloc[i]
      total.append({
                    'label': tmp[0:30]+"..." if len(tmp)>30 else tmp,
                    'value': "id."+str(devices['device_id'].iloc[i]),
                    'title':tmp,
                })
    if len(med_fields)>i:
      total.append({
                    'label': med_fields[i],
                    'value': "mf."+med_fields[i],
                    'title':med_fields[i],
                })
    if len(manufacturer)>i:
      total.append({
                    'label': manufacturer[i][0:30]+"..." if len(manufacturer[i])>30 else manufacturer[i],
                    'value': "man."+manufacturer[i],
                    'title':manufacturer[i],
                })
    if len(dev_type)>i:
      total.append({
                    'label': dev_type[i],
                    'value': "dt."+dev_type[i],
                    'title':dev_type[i],
                })
    i+=1
  return total


#source code for get_close_matches, modified in order to return the indexes instead of the string values becouse of devices search
def get_close_matches_indexes(word, possibilities, n=3, cutoff=0.6):
    
    if not n >  0:
        raise ValueError("n must be > 0: %r" % (n,))  #just as exception
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))   #just as exception
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for idx, x in enumerate(possibilities):
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and \
           s.quick_ratio() >= cutoff and \
           s.ratio() >= cutoff:     # \ is used to new line 
            result.append((s.ratio(), idx))

    # Move the best scorers to head of list
    result = _nlargest(n, result)

    # Strip scores for the best n matches
    return [x for score, x in result]