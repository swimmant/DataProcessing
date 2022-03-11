import os, csv


f = open('./xRay/test.csv', 'w', newline='')
images = os.listdir('./xRay/test/')
csv_writer = csv.writer(f)

for i in images:
    # print(i)
    name = os.path.splitext(i)[0]
    csv_writer.writerow([name, 1, 1, 1, 1, "umbrella"])
    print(name)

f.close()