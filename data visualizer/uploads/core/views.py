from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .sn import main


# def index(request):

def display_data(request):
	if request.method == 'POST' and 'buhton' not in request.POST:
		# try:
		text = request.POST.get('inptext')
		print(text)
		datout = main(text)
		print(datout['populated'])
		intention = datout['intention']
		# intention, action = 'displayData',['i am a potato','i love potato','potato is life']
		# intention, action = 'displayNumber',[345]
		# intention, action = 'visualiseData',[['people','places','number'],[234,256,287],['bar']]
		intentList = ['displayData','displayExcept','displayNumberData']
		
		
		if intention in intentList:
			actionL = datout['populated']['ALLTAGS']
			mainstr = ''
			print(intention)
			for i in actionL:
				mainstr=mainstr+i+"\n"
			return render(request, 'core/data_fill.html',{
				'text': mainstr
				})


		if intention == 'displayValue':
			tags = datout['populated']['named_tags']
			data_whole = datout['populated']['named_ent']
			mstr = ''
			for k,v in data_whole.items():
				if k in tags:
					mstr = mstr + "\n" + k.upper()+"\n"
					mainstr = data_whole[k]
					for i in mainstr:
						mstr=mstr+str(i)+"\n"

			return render(request, 'core/data_fill.html',{
				'text': mstr
				})
					
			
		elif intention == 'visualizeData':
			data = datout['populated']['dataTag']
			values = datout['populated']['countTag']
			barg = ['bar graph', 'bar chart', 'histogram', 'histograms', 'bar graphs', 'bar', 'bar plot']
			# parg = ['pie graph', 'pie chart', 'pi graph', 'pi chart', 'pie', 'pi', 'pi plot', 'pie plot']
			print(data)
			print(values)
			ge = datout['graph']
			print(ge)
			if ge == "" or ge in barg:
				gtype = 'bar'
			else:
				gtype = 'pie'
			print(gtype)
			datstr=data[0]
			numstr=str(values[0])
			count = -1
			for i in range(1,len(data)):
				numstr = numstr+","+str(values[i])
				datstr = datstr+","+data[i]
			
			return render(request, 'core/form_fill.html', {
			'textval': datstr, 
			'valval': numstr,
			'gvalue': gtype
			})


		elif intention == 'displayNumber':
			disNum = datout['populated']['totalcount']
			print(intention)
			text = 'Your query returned '+str(disNum)+' entries in the dataset\n'
			return render(request, 'core/data_fill.html',{
				'text': text
				})
	# 	except:
	# 		print("except")
	# 		return render(request, 'core/simple_upload.html')
	else:
		# print("except")
		return render(request, 'core/simple_upload.html')


