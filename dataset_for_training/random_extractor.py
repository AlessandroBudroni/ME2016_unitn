#script used to extract values from the dataset

import re
import random

dataset = 'posts.txt'

def main():

    with open(dataset) as f:
        lines = f.readlines()
    f.close()

    lines.pop(0)

# Extract fake and real tweet id

    fake_id = []
    real_id = []
    fake_images = []
    real_images = []


    for line in lines:
        spl_line = re.split('\t',line)
        image_ids = re.split(',', spl_line[3])

        if "real" in spl_line[6]:
            real_id.append(spl_line[0]+"\n")
            for image_id in image_ids:
                 real_images.append(image_id+"\n")
        elif "fake" in spl_line[6]:
            fake_id.append(spl_line[0]+"\n")
            for image_id in image_ids:
                fake_images.append(image_id+"\n")

    fake_images = sorted(list(set(fake_images)))
    real_images = sorted(list(set(real_images)))

    fake_id = random.sample(fake_id,len(real_id))
    real_images = random.sample(real_images,len(fake_images))

    file_fake_tweet_id = open("fake_tweet_id.data",'w')
    file_fake_tweet_id.writelines(fake_id)

    file_real_tweet_id = open("real_tweet_id.data", 'w')
    file_real_tweet_id.writelines(real_id)

    file_fake_image_id = open("fake_image_id.data",'w')
    file_fake_image_id.writelines(fake_images)

    file_real_image_id = open("real_image_id.data",'w')
    file_real_image_id.writelines(real_images)




if __name__ == '__main__':
    main()
