from tqdm import tqdm
import threading
from bs4 import BeautifulSoup
import urllib.request
from crawling.extracter import extract_page
import time
from tqdm import tqdm
import argparse
import pymongo
from pymongo import MongoClient
from configs.config import logger
from decouple import config

def divide_thread(number_thread: int, end_page: int, start_page: int) -> list:
    pages_threads = []
    for i in range(0,number_thread):
        temp = range(start_page+i,end_page,number_thread)
        pages_threads.append(temp)
    return pages_threads


def thread_function(pages: list, thread_id: int, upload: pymongo.collection.Collection) -> None:
    for p in tqdm(pages,desc=f'thread_name_{thread_id}'):
        page = urllib.request.urlopen(f'https://bonbanh.com/oto/page,{p}')
        soup = BeautifulSoup(page, 'html.parser')
        try:
            all = soup.find("div", {"class":"g-box-content"})
            ul = all.find_all("ul")
            a = ul[-1].find_all("a")
            all_link = []
            for l in a:
                link = l['href']
                all_link.append(link)
        except:
            #logger.error(f'Errorr page {p}')
            pass
        for i in all_link:
            try:
                post = extract_page(i)
                time.sleep(0.01)
            except:
                #logger.error(f'Errorr page: {p}, with link: {i}')
                pass
            try:
                #pass
                upload.insert_one(post)
            except:
                pass
        time.sleep(0.05)

def main(pages_threads: list, number_thread: int, upload: pymongo.collection.Collection) -> None:
    try:
        start_time = time.time()
        # Init thread
        threads = []
        for i in range(number_thread):
            t = threading.Thread(target=thread_function, args=(pages_threads[i], i, upload))
            threads.append(t)

        # Start thread   
        for i in range(number_thread):
            threads[i].start()
            time.sleep(0.5)

        # Wait thread Done
        for i in range(number_thread):
            threads[i].join()
        logger.info(f"Done in {time.time()- start_time: 0.4f} s")
    except:
        logger.error(f"Thread error")

if __name__ =='__main__':
    # Create the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_thread', type=int, default=3)
    parser.add_argument('--start_page', type=int, default=0)
    parser.add_argument('--end_page', type=int, default=20)


    args = parser.parse_args()
    number_thread = args.num_thread
    start_page = args.start_page
    end_page = args.end_page
    MONGODB_USER = config('MONGODB_USER')
    MONGODB_PASSWORD = config('MONGODB_PASSWORD')
    DATASOURCE = config('DATASOURCE_TEST')
    MONGODB_URL = f'mongodb+srv://{MONGODB_USER}:{MONGODB_PASSWORD}@cluster0.k0hrmbm.mongodb.net/test'
    client = MongoClient(MONGODB_URL)
    db=client[DATASOURCE]
    collection_post = db.post

    # Init pages
    pages_threads = divide_thread(
            number_thread=number_thread, 
            start_page=start_page,
            end_page=end_page
        )
    main(
        pages_threads=pages_threads,
        number_thread=number_thread,
        upload=collection_post
    )
