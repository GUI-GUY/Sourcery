from multiprocessing import Process, Queue, Pipe, Semaphore
from threading import Thread
import logging as log
from sourcery import do_sourcery
import global_variables as gv

class Processing():
    """Includes methods for the sourcing process"""
    def __init__(self, parent):
        self.parent = parent
        self.process = Process()
        self.comm_q = Queue() # Queue for 'Remaining searches'
        self.comm_img_q = Queue() # Queue for 'Currently Sourcing'
        self.comm_stop_q = Queue() # Queue for stop signal
        self.comm_error_q = Queue() # Queue for error messages
        self.img_data_q = Queue() # Queue for ImageData information
        self.duplicate_p_pipe, self.duplicate_c_pipe = Pipe()
        self.terminate_p_pipe, self.terminate_c_pipe = Pipe()

    def magic(self):
        """
        Starts second process which searches for images and downloads them.
        """
        self.parent.do_sourcery_btn.configure(state='disabled')
        self.parent.load_from_ref_btn.configure(state='disabled')
        gv.Files.Log.write_to_log('Starting second process for sourcing images', log.INFO)
        self.parent.input_lock.acquire()
        self.process = Process(target=do_sourcery, args=(gv.cwd, self.parent.input_images_array, {"saucenao_key":gv.config['SauceNAO']['api_key'], "gelbooru_api_key":gv.config['Gelbooru']['api_key'], "gelbooru_user_id":gv.config['Gelbooru']['user_id']}, gv.config['SauceNAO']['minsim'], gv.input_dir, self.comm_q, self.comm_img_q, self.comm_stop_q, self.comm_error_q, self.img_data_q, self.duplicate_c_pipe, self.terminate_c_pipe, ))
        self.process.start()
        self.parent.input_lock.release()

    def duplicate_loop(self):
        """
        Looks if a requested image has already been sourced with the same options and notifies the magic process
        """
        def run():
            while True:
                if self.duplicate_p_pipe.poll():
                    dup_dict = self.duplicate_p_pipe.recv()
                    if dup_dict[0] == 'DATA':
                        is_dup = False
                        for data in gv.img_data_array: # {'img_name': img, 'minsim': minsim, 'rename_pixiv': gv.config['Pixiv']['rename'], 'rename_danbooru': gv.config['Danbooru']['rename']}
                            if str(dup_dict[1]['img_name']) == data.sub_dill.name and str(dup_dict[1]['minsim']) == str(data.sub_dill.minsim):
                                is_dup = True
                                break
                        self.duplicate_p_pipe.send(is_dup)
                    elif dup_dict[0] == 'REF':
                        self.duplicate_p_pipe.send(gv.Files.Ref.new_reference(*dup_dict[1]))
        Thread(target=run, daemon=True, name="duplicate_loop").start()

    def terminate_loop(self):
        """
        Terminates second process on signal receive from terminate pipe
        """
        def run():
            while True:
                if self.terminate_p_pipe.poll():
                    if self.terminate_p_pipe.recv():
                        try:
                            self.process.terminate()
                        except Exception as e:
                            print('ERROR [0063] ' + str(e))
                            gv.Files.Log.write_to_log('ERROR [0063] ' + str(e), log.ERROR)
                            self.terminate_p_pipe.send(False)
                            #mb.showerror("ERROR [0063]", "ERROR CODE [0063]\nSomething went wrong while accessing a the 'Input' folder, please restart Sourcery.")
        Thread(target=run, daemon=True, name="terminate_loop").start()
        
    def stop(self):
        """
        Stop further search for images and halt the magic process.
        """
        if self.process.is_alive():
            gv.Files.Log.write_to_log('Stopping sourcing process...', log.INFO)
            self.comm_stop_q.put("Stopped")
            self.parent.stop_btn.configure(state='disabled')
        #currently_sourcing_img_lbl.configure(text="Stopped")
