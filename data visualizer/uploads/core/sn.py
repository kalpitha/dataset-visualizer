# Dependencies
		# word2number

import io
import json
import spacy
from pprint import pprint
from word2number import w2n
from .main import get_

from snips_nlu import SnipsNLUEngine, load_resources
import time

load_resources(u"en")

# UNCOMMENT THE LINES BELOW WHEN RETRAINING THE SYSTEM IS REQUIRED

# with io.open("/Users/kalpitha/Dev/Project/simple/uploads/core/config_en.json") as f:
# 	config = json.load(f)

# engine = SnipsNLUEngine(config=config)
# spacy_load = spacy.load('en')

# with io.open("/Users/kalpitha/Dev/Project/simple/uploads/core/dataset.json") as f:
# 	dataset = json.load(f)

# engine.fit(dataset)

# engine_json = json.dumps(engine.to_dict())
# with io.open("trained_engine.json", mode="w") as f:
#     # f.write(engine_json.decode("utf8"))  # Python 2
#     f.write(engine_json)  # Python 3

#COMMENT THE LINES BELOW WHEN RETRAINING
with io.open("trained_engine.json") as f:
    engine_dict = json.load(f)

loaded_engine = SnipsNLUEngine.from_dict(engine_dict)





def get_values(software_data):

	vals = ""

	# print(software_data)
	for key, value in software_data.items():
		# print(item)
		if value == True:
			vals += key + ','

	vals = vals[:-2]

	return vals


def software_usecase(intent, entities, software_data, sentence):
	# Execute commands of software usecase

	software_data = software_data[intent]

	for item in entities:
		if 'slotName' in item:
			if item['slotName'] == 'entval':
				software_data['display'][item['value']['value']] = True
			elif item['slotName'] == 'numbCount':
				try:
					software_data['n_items'] = w2n.word_to_num(item['value']['value'])
				except:
					software_data['n_items'] = int(item['value']['value'])
			elif item['slotName'] == 'gtype':
				software_data['graph'] = item['value']['value']
				print(software_data['graph'])
		else:
			print("No slotName found")

	if intent == 'visualizeData' or intent == 'displayNumber':
		if entities == []:
			# {'names': True, 'places': True, 'money': False, 'time': False, 'quantity': False, 'date': False, 'event': False, 'organisation': False}
			software_data['display']['names']=software_data['display']['places']=software_data['display']['money']=software_data['display']['time']=software_data['display']['quantity']=software_data['display']['date']=software_data['display']['event']=software_data['display']['organisation']=True

	# print(software_data['display'])
	vals = get_values(software_data['display'])
	if intent == 'displayData':
		# print("Action : Displaying\n" ,software_data['display'])
		software_data['action'] = "Displaying " + vals
	elif intent == 'displayExcept':
		# print("Action : Displaying except\n", software_data['display'])
		software_data['action'] = "Displaying except " + vals
	elif intent == 'displayNumber':
		# print("Action : Displaying counts for\n", software_data['display'])
		software_data['action'] = "Displaying counts of " + vals
	elif intent == 'displayNumberData':
		# print("Action : Displaying counts and contents\n", software_data['display'])
		software_data['action'] = "Displaying counts and contents of " + vals
	elif intent == 'displayValue':
		# print("Action : Displaying values\n", software_data['display'])
		software_data['action'] = "Displaying values of " + vals
	elif intent == 'visualizeData':
		# print("Action : Visualizing data for\n", software_data['display'])
		software_data['action'] = "Visualizing values of " + vals

	software_data['intention'] = intent
	# pprint(software_data)

	data = get_(sentence, entities, software_data)
	# pprint(data, depth=3)
	return data


def hardware_usecase(sentence, intent, entities, hardware_data):
	pass


def main(text):

	t1 = time.time()
	a = loaded_engine.parse(text)

	# pprint(a)

	try:
		intent = a['intent']['intentName']
	except:
		intent = "noIntent"
	# print(a['intent']['intentName'], "\n\n")

	entities = a['slots']
	# pprint(entities)

	software_data = json.load(open('/Users/kalpitha/Dev/Project/simple/uploads/core/software.json'))
	# hardware_data = json.load(open('hardware.json'))

	if intent in software_data:
		# print(intent)
		# print(entities)
		# print("Software Usecase!")
		data = software_usecase(intent, entities, software_data, text)
	# elif intent in hardware_data:
	# 	print("Hardware Usecase")
	# 	hardware_usecase(intent, entities, hardware_data)
	else:
		print("Endpoint not configured.")

	# except Exception as e:
		# print("Exception in sninlu.py while parsing the engine output.\n", e)
	# print("Time Taken : ", time.time() - t1)
	return data

# if __name__ == "__main__":
# 	main(input("Sentence : "))
