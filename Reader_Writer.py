# Reader Writer Problem Implementation
# Multiple readers can read simultaneously
# Writers require exclusive access to write

# Visual Representation:
# ┌─────────────────────────────────────────────────┐
# │                 SHARED RESOURCE                 │
# │            (Database/File/Memory)               │
# └─────────────────────────────────────────────────┘
#           ▲                           ▲
#           │                           │
#    ┌──────┴──────┐             ┌─────┴─────┐
#    │   READERS   │             │  WRITERS  │
#    │ (Multiple   │             │ (Single   │
#    │ Concurrent) │             │ Exclusive)│
#    │   R1 R2 R3  │             │     W1    │
#    └─────────────┘             └───────────┘
#
# Synchronization:
# - read_count: tracks active readers
# - read_count_mutex: protects read_count
# - write_lock: ensures exclusive writer access

# -------------------------------------------------Solution-------------------------------------------------
# use read_count variable to track number of readers
# use mutex to (increment/decrement) read_count safely
# use write_lock to ensure exclusive access for writers
#-------------------------------------------------------------------------------------------------------------

import threading
import time
import random


read_count = 0
read_count_mutex = threading.Semaphore(1) #Binary Semaphore for read_count access 
write_lock = threading.Semaphore(1) # Semaphore for writers


def reader(reader_id):
    global read_count
    while True:
        time.sleep(random.random()) # Simulate time before trying to read

        read_count_mutex.acquire() # Enter critical section to update read_count
        read_count += 1
        if read_count == 1:
            write_lock.acquire() # First reader locks the writer
        read_count_mutex.release() # Leave critical section
        # Reading section
        print(f'Reader {reader_id} is reading.')
        time.sleep(random.random()) # Simulate reading time
        print(f'Reader {reader_id} has finished reading.')
        read_count_mutex.acquire() # Enter critical section to update read_count
        read_count -= 1
        if read_count == 0:
            write_lock.release() # Last reader unlocks the writer
        read_count_mutex.release() # Leave critical section

def writer(writer_id):
    while True:
        time.sleep(random.random()) # Simulate time before trying to write

        write_lock.acquire() # Acquire lock for writing
        # Writing section
        print(f'Writer {writer_id} is writing.')
        time.sleep(random.random()) # Simulate writing time
        print(f'Writer {writer_id} has finished writing.')
        write_lock.release() # Release lock after writing


def main():
    readers = [threading.Thread(target=reader, args=(i,)) for i in range(3)]
    writers = [threading.Thread(target=writer, args=(i,)) for i in range(2)]

    for r in readers:
        r.start()
    for w in writers:
        w.start()

    for r in readers:
        r.join()
    for w in writers:
        w.join()

if __name__ == "__main__":
    main()                        
        
            
    
            






