# producer consumer problem (Semaphores and Mutex )

# Visual Representation:
# ┌──────────┐    ┌─────────────────────────────┐    ┌──────────┐
# │ PRODUCER │───▶│          BUFFER             │◀───│ CONSUMER │
# │    P1    │    │  [item1][item2][item3][ ][ ]│    │    C1    │
# └──────────┘    │     Size: 5 (Fixed)         │    └──────────┘
#                 └─────────────────────────────┘
#                            ▲
#                            │
#                    Synchronization:
#                    - mutex: buffer access
#                    - empty: available slots
#                    - full: filled slots
#
# Producer Consumer Problem
# Producer must not add data into the buffer if it's full
# Consumer must not remove data from the buffer if it's empty
# Producer and Consumer must not access the buffer at the same time

# -------------------------------------------------Solution-------------------------------------------------
# use semaphore for empty and full slots
# use mutex for critical section
#-------------------------------------------------------------------------------------------------------------

import threading
import time
import random

buffer = []
buffer_size = 5
mutex = threading.Semaphore(1) # Binary Semaphore for mutual exclusion
empty = threading.Semaphore(buffer_size) # Counting Semaphore for empty slots
full = threading.Semaphore(0) # Counting Semaphore for full slots


def producer():
    global buffer
    while True:
        item = random.randint(1, 100) # Produce an item
        empty.acquire() # Decrease empty count
        mutex.acquire() # Enter critical section

        buffer.append(item) # Add item to buffer
        print(f'Produced: {item}, Buffer: {buffer}')

        mutex.release() # Leave critical section
        full.release() # Increase full count
        time.sleep(random.random()) # Simulate time taken to produce an item
        
def consumer():
    global buffer
    while True:
        full.acquire() # Decrease full count
        mutex.acquire() # Enter critical section

        item = buffer.pop(0) # Remove item from buffer
        print(f'Consumed: {item}, Buffer: {buffer}')

        mutex.release() # Leave critical section
        empty.release() # Increase empty count
        time.sleep(random.random()) # Simulate time taken to consume an item        

def main():
    prod_thread = threading.Thread(target=producer)
    cons_thread = threading.Thread(target=consumer)

    prod_thread.start()
    cons_thread.start()

    prod_thread.join()
    cons_thread.join()

if __name__ == "__main__":
    main()        
