
SIMPLE TEXT RETRIEVAL PYTHON

This is a simple python script to search images of Chalearn cultural events dataset.

To make it run from bash go in the Text Retrieval folder and run: python text_extraction.py

You have to set in text_extraction.py the main folder of your dataset at line 16.

It is not multi-thread so on big datasets you either implement it or use the trick of opening multiple bash and call it multiple times selecting the folder you want: text_extraction.py at lines 17-19.

If needed call format_text.py to delete spaces, puntuation  etc after you completed the dataset. 

NOTE: I developed it quickly and I noticed sometimes it gets struck so keep an eye on it while is working.

Andrea Pilzer
andrea.pilzer@studenti.unitn.it
