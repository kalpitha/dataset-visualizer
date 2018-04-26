A dataset visualizer that lets you upload a dataset and parse through the contents without having to go through all the lines. This can be used as a data preprocessor in order to understand the contents of a dataset without having to actually write huge chunks of code. 
## Dependencies - 
* snips-nlu - 
Refer to snips-nlu documentation [here](http://snips-nlu.readthedocs.io/en/latest/installation.html)
* pandas - 
Refer to pandas documentation [here](https://pandas.pydata.org/pandas-docs/stable/install.html)
* spacy - 
Refer to pandas documentation [here](https://spacy.io/usage/)
* word2number - 
Refer to documentation [here](https://pypi.org/project/word2number/)
* scipy - 
Refer to documentation [here](https://pypi.org/project/scipy/)
* django - 
Refer to documentation [here](https://docs.djangoproject.com/en/2.0/intro/install/)
## Example usage - 
First run the django project in localhost or server as python3 manage.py runserver 0.0.0.0:8990
- Input - Show me one hundred datapoints with names.
  - Output - 100 datapoints with names


- Input - Show me all names in the dataset
  - Output - Potential names in the dataset
  
- Input - Visualize the dataset with respect to names and places as a bar graph
  - Output - A bar graph is plotted containing number of datapoints with names and number of datapoints with places
