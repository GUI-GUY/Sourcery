#import global_variables as gv
from time import sleep

def preload_main(sem, id, img_data_array):
    sem.acquire()
    while True:
        print("preloader " + str(id))
        #print(img_data_array)
        if len(img_data_array) < id+1:
            sleep(10)
            continue
        
        ImgData = img_data_array[id]
        ImgData.load()
        return
    #while(True):
        #get semaphore
        #get ImgData
        #ImgData.load()