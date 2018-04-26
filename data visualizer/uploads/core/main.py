import pandas as pd
import spacy
import os
import json
import numpy as np
import scipy


class Storage(object):
	pass

class Analysis(object):
	pass

analysis = Analysis()
store = Storage()
spacy_load = spacy.load('en')

path = os.getcwd()+"/datasets/"
setattr(store,'path',path)

def load_dataset(store):
	store.path = "/Users/kalpitha/Dev/Project/simple/uploads/core/datasets/seinfeld-chronicles/"

def csv_to_dataframe(store):
	setattr(store,'df',pd.read_csv(store.path+"scripts.csv"))
	setattr(store,'df_count',store.df.count())
	setattr(store,'df_count_int',len(store.df.columns))


def split_dataframes(store,analysis):
	series_dict = {}
	for i in range(1,store.df_count_int+1):
		series_dict[store.df[store.df.columns[i-1]].head().name] = np.array(store.df[store.df.columns[i-1]].values).tolist()
	setattr(analysis,'series_dict',series_dict)

def classify_series_nums(analysis):
	nums = []
	alpha = []

	for col,vals in analysis.series_dict.items():
		for v in vals:
			if not type(v) == str:
				nums.append(col)
				break
			else:
				alpha.append(col)
				break
	setattr(analysis,'num_list',nums)
	setattr(analysis,'alpha_list',alpha)

def make_alpha_frame(store,analysis):
	analyze_dataset = {}
	analyze_dataset_index = {}
	named_ent = {'CARDINAL':[],'DATE':[],'GPE':[],'PERSON':[],'ORDINAL':[],'MONEY':[],'TIME':[],'ORG':[],'PRODUCT':[],'NORP':[],'QUANTITY':[],'EVENT':[]}
	dataframe_at_focus  = store.df[analysis.alpha_list[1]]
	for i in range(0,500):
		stage_spacy = spacy_load(dataframe_at_focus[i])
		if stage_spacy.ents:
			analyze_dataset[dataframe_at_focus[i]] = [w.label_ for w in stage_spacy.ents]
			analyze_dataset_index[dataframe_at_focus[i]] = [w for w in stage_spacy.ents]
		for w in stage_spacy.ents:
			if str(w).lower() in named_ent[w.label_]:
				pass 
			else:
				named_ent[w.label_].append(str(w).lower())
	# print(named_ent)

	setattr(analysis,'analyze_dataset',analyze_dataset)
	setattr(analysis,'analyze_dataset_index',analyze_dataset_index)
	setattr(analysis,'named_ent',named_ent)


def summation_list(analysis):
	local_dict = analysis.analyze_dataset
	local_list = []
	# print(local_dict)
	for _,ent in local_dict.items():
		for elements in ent:
			local_list.append(elements)
	setattr(analysis,'analyze_dataset_unique',list(set(local_list)))


def populate_from_list(analysis, TAGS):

	populated = {}
	populated['ALLTAGS'] = []
	for TAG in TAGS:
		count = 0
		populated[TAG] = []
		for i,j in analysis.analyze_dataset.items():
			# print(i)
			# print(j)
			if TAG in j:
				count += 1
				populated[TAG].append(i)
				populated['ALLTAGS'].append(i)

	populated['totalcount'] = 0
	populated['dataTag'] = []
	populated['countTag'] = []
	for TAG in TAGS:
		populated['count' + TAG] = len(populated[TAG])
		populated['totalcount'] = populated['totalcount']+len(populated[TAG])	
		populated['dataTag'].append(TAG)
		populated['countTag'].append(populated['count' + TAG])
	return populated


def get_tags(tags):
	existing_tags = json.load(open('/Users/kalpitha/Dev/Project/simple/uploads/core/compare.json'))
	print(get_tags)
	actual_tags = []
	for tag in tags:
		for t, items in existing_tags.items():
			if tag in items:
				actual_tags.append(t)
	# print("TAGS : ", actual_tags)
	print(actual_tags)
	return actual_tags


def get_(sentence, entities, software_data):
	load_dataset(store)
	print ("Loaded Dataset")

	csv_to_dataframe(store)
	print("Converted to dataframe")

	split_dataframes(store,analysis)
	print("Dataframes split.")

	classify_series_nums(analysis)
	print("Classified series numbers")

	make_alpha_frame(store,analysis)
	print("Made alpha frame")

	summation_list(analysis)
	print("Created summation list")

	print ("Looking in the dataset")

	print ("List of avaliable entities in Dataset...")
	a = analysis.analyze_dataset

	tags = []

	for i, j in software_data['display'].items():
		if (j and not software_data['negativity']) or (not j and software_data['negativity']):
			tags.append(i)
	# print(tags)

	tags = get_tags(tags)

	populated = populate_from_list(analysis, tags)

	software_data['populated'] = populated
	software_data['analysis'] = a
	software_data['populated']['named_tags']=tags
	software_data['populated']['named_ent']=analysis.named_ent

	return software_data
