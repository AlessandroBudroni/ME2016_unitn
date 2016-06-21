import sys
import csv
import os

nargv = len(sys.argv)
if not nargv == 2:
    print('not enough arguments. Please try $python media_indexing_from_dataset.py multimedia_path')
    print('for example: $python media_indexing_from_dataset.py /mediaeval2016/devset/Medieval2016_DevSet_Images')
    sys.exit(2)

argv_lst = sys.argv

multimedia_path = argv_lst[1]

print('multimedia_path = ', multimedia_path)

# save in cvs file as: mul_id type event_name abs_path
with open('multimedia_details.csv', 'w') as csvfile:
    fieldnames = ['mul_id', 'type', 'event_name', 'abs_path']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # loop over events and their multimedia content
    for root, dirs, files in os.walk(multimedia_path, topdown=True):
        mul_id = ''
        type = ''
        event_name = ''
        abs_path = ''

        for name in files:
            if name == '.DS_Store': # junk files
                continue

            abs_path = os.path.join(root,name)
            file_name, ext = os.path.splitext(abs_path)
            if ext == '.txt': # videos
                type = 'video'
                with open(abs_path,'r') as f:
                    line = f.readline()
                    line = f.readline()
                    abs_path = line[line.find('https://'):]
                    mul_id = line[:line.find('https://')]

            else: # images
                type = 'image'
                mul_id = os.path.split(file_name)[-1]

            dot_indx = mul_id.find('.')
            if dot_indx != -1:
                mul_id = mul_id[:dot_indx]


            event_name = os.path.split(root)[-1]

            if event_name == 'fakes' or event_name == 'reals':
                event_name = os.path.split(os.path.split(root)[0])[-1] # get name of parent folder

            writer.writerow({'mul_id':mul_id, 'type':type, 'event_name':event_name, 'abs_path':abs_path})

csvfile.close()