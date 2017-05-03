import json
from urllib import request
from urllib.error import HTTPError, URLError
import os
import socket
import time

sleep_download_time = 3
timeout = 10
socket.setdefaulttimeout(timeout)
miss = 0
miss_id_list = []


def download(id, num_id_list):
    print("id:", id, "   num_id_list:", num_id_list)
    download_url = "https://www.shapenet.org/shapenet/obj-zip/ShapeNetCore.v1/{num_id}/{id}/model.presolid.binvox"

    for backup in range(0, len(num_id_list)):
        global miss
        global miss_id_list
        time.sleep(sleep_download_time)
        try:
            request.urlretrieve(download_url.format(num_id=num_id_list[backup], id=id), id+".binvox")
            break

        except HTTPError:
            if backup is len(num_id_list)-1:
                print("\none missed!\n")
                miss = miss + 1
                miss_id_list.append(id)
            else:
                print("change num_id")
                continue

        except socket.timeout:
            # time.sleep(20)
            print("\nsocket timeout\n")
            miss += 1
            miss_id_list.append(id)
            break

        except URLError as e:
            print("\nURLError\n")
            miss += 1
            miss_id_list.append(id)
            break


url = "https://www.shapenet.org/solr/models3d/select?q={item}&wt=json&sort=&start=0&rows=300&fq=%2Bdatasets%3A%22ShapeNetCore%22++%2BhasModel%3Atrue+-modelSize%3A%5B10000000+TO+*+%5D&fl="
while True:
    search_item = input("please input the search item:\n")
    html = request.urlopen(url.format(item=search_item))
    response = json.load(html)
    numFound = response.get("response").get("numFound")
    if numFound is 0:
        print("no result found")
        continue
    else:
        break

path = os.getcwd()+"/"+search_item
if os.path.exists(path):
    pass
else:
    os.mkdir(path)
os.chdir(path)

for i in range(0, numFound):
    id = response.get("response").get("docs")[i]["id"]
    num_id_list = response.get("response").get("docs")[i].get("wnhypersynsets")
    # description = response.get("response").get("docs")[i].get("description")
    print(i + 1, " downloading    total:", numFound)
    download(id, num_id_list)

print("\ndownload done!    total miss:", miss)
if len(miss_id_list) is not 0:
    print("miss_id_list\n", miss_id_list)


# request.urlretrieve("https://www.shapenet.org/shapenet/screenshots/models/3dw/3/c/5/2/2/5f973732610664b3b9b23ddfcbc/3c5225f973732610664b3b9b23ddfcbc/3c5225f973732610664b3b9b23ddfcbc.gif", f)



