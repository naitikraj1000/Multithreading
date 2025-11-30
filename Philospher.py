# Dining Philosophers Problem Implementation
# Five philosophers sit around a circular table with 5 forks
# Each philosopher alternates between thinking and eating
# To eat, a philosopher needs both left and right forks
# Only one philosopher can hold a fork at a time

# Visual Representation:
#                    Fork 0
#                      |
#               Philosopher 0
#              /             \
#          Fork 4           Fork 1
#            /                 \
#    Philosopher 4 ──── TABLE ──── Philosopher 1
#            \                 /
#          Fork 3           Fork 2
#              \             /
#               Philosopher 3
#                      |
#                   Fork 2
#
# Each philosopher needs 2 adjacent forks to eat:
# - Philosopher i needs Fork i and Fork (i+1)%5
# - Deadlock prevention: limit to 4 philosophers competing
# - Semaphores: one per fork + dining_room limiter

# -------------------------------------------------Solution-------------------------------------------------
# Use semaphores to represent forks (binary semaphores)
# Each philosopher picks up left fork first, then right fork
# To prevent deadlock, limit number of philosophers that can try to eat simultaneously
# Use a semaphore to allow only 4 philosophers to compete for forks at once
#-------------------------------------------------------------------------------------------------------------

import threading
import time
import random

NUM_PHILOSOPHERS = 5

# Create semaphores for each fork (binary semaphores)
forks = [threading.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]
# Limit philosophers to prevent deadlock - only 4 can try to eat at once
dining_room = threading.Semaphore(NUM_PHILOSOPHERS - 1)

def philosopher(philosopher_id):
    left_fork = philosopher_id
    right_fork = (philosopher_id + 1) % NUM_PHILOSOPHERS
    
    while True:
        # Thinking
        print(f'Philosopher {philosopher_id} is thinking.')
        time.sleep(random.uniform(1, 3))  # Simulate thinking time
        
        # Hungry - try to eat
        print(f'Philosopher {philosopher_id} is hungry.')
        
        dining_room.acquire()  # Enter dining room (limit concurrent philosophers)
        
        # Pick up forks
        print(f'Philosopher {philosopher_id} is trying to pick up forks.')
        forks[left_fork].acquire()   # Pick up left fork
        print(f'Philosopher {philosopher_id} picked up left fork {left_fork}.')
        
        forks[right_fork].acquire()  # Pick up right fork
        print(f'Philosopher {philosopher_id} picked up right fork {right_fork}.')
        
        # Eating
        print(f'Philosopher {philosopher_id} is eating.')
        time.sleep(random.uniform(1, 2))  # Simulate eating time
        print(f'Philosopher {philosopher_id} has finished eating.')
        
        # Put down forks
        forks[right_fork].release()  # Put down right fork
        print(f'Philosopher {philosopher_id} put down right fork {right_fork}.')
        
        forks[left_fork].release()   # Put down left fork
        print(f'Philosopher {philosopher_id} put down left fork {left_fork}.')
        
        dining_room.release()  # Leave dining room
        
        print(f'Philosopher {philosopher_id} finished dining cycle.')

def main():
    philosophers = [threading.Thread(target=philosopher, args=(i,)) for i in range(NUM_PHILOSOPHERS)]
    
    print(f"Starting {NUM_PHILOSOPHERS} philosophers around the dinner table...")
    print("Each philosopher will think, get hungry, try to eat, and repeat.")
    print("Press Ctrl+C to stop the simulation.\n")
    
    for p in philosophers:
        p.start()
    
    for p in philosophers:
        p.join()

if __name__ == "__main__":
    main()
