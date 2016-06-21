SIMPLE TEXT RETRIEVAL PYTHON

This is a simple python script to search related images of other images saved in a directory /dataset trough google image.

To make it run from bash go in the Text Retrieval folder and run: python text_extraction.py

Te formats supported are:

* gif
* tif
* png
* jpg
* jpeg


= Data of the task has been ready =

1. Create the csv file storing all details of development set (modify the parameters if needed)
	$ python text_extraction_from_media.py /mediaeval2016/devset/Medieval2016_DevSet_Images

2. Moving *.csv to appropriate folder and rename it, in my case: 'dataset/devset/multimedia_dev_details.csv'

3. Run text_extraction_from_media.py to crawl text from websites. All data will be stored in SQLite DB file "dev.db". At the present, I create the new DB file whenever I run the program, and also design a simple "resume" function using 2 flags "running_from" and "running_to"