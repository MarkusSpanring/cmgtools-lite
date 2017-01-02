import json
import os

with open('raw.dat','rb') as FSO:
	raw_data = FSO.readlines()

if os.path.isfile('datasets.json'):
	with open('datasets.json','rb') as FSO:
		dsets = json.load(FSO)
else:
	with open('datasets.json','wb') as FSO:
		json.dump({}, FSO)
		dsets = {}

data_struct = {}
for data in raw_data:
	if not '/' in data:
		current = data.replace('\n','')
		data_struct[current] = {}
		
	else:
		if 'powheg' in data: 
			gen = '_powheg'
		elif 'madgraphMLM' in data:
			gen = '_madgraphMLM'
		elif 'nlo' in data:
			gen = '_amcatnloFXFX'
		elif 'pythia8' in data:
			gen = '_pythia8'
		else:
			gen = ''

		
		key = data.split('_13TeV')[0]
		key = key.replace('_TuneCUETP8M1','')
		key = key.replace('/','').replace('-','_').replace('\n','')
		key += gen
		if 'RunII' in data:
			prod_label = 'MC{0}'.format(data.split('RunII')[1].split('Mini')[0])
		else:
			prod_label = 'DATA'
		if 'reHLT' in data:
			prod_label += '_reHLT'

		if not key in dsets.get(current,''):

			data_struct[current][key] = {'datacard':data.replace('\n','')}
			data_struct[current][key]['step_1'] = {'status':'', 'time':''}
			data_struct[current][key]['das_url'] = ''
			data_struct[current][key]['prod_label'] = prod_label

		else:
			data_struct[current][key] = {'datacard':dsets[current][key]['datacard']}
			data_struct[current][key]['step_1'] = dsets[current][key]['step_1']
			data_struct[current][key]['das_url'] = dsets[current][key]['das_url']
			data_struct[current][key]['prod_label'] = dsets[current][key]['prod_label']

with open('datasets.json','wb') as FSO:
	json.dump(data_struct, FSO,indent=4)

