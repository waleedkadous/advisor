

# Approximate pi using random sampling. Generate x and y randomly between 0 and 1. 
#  if x^2 + y^2 < 1 it's inside the quarter circle. x 4 to get pi. 
import ray
from random import random

# Let's start Ray
ray.init()

#To trigger too many tasks: 10/10000/10000
#To not trigger too many tasks
#  10/1/1000000
SAMPLES = 10; 
MINIBATCHES = 1; 
BATCHES = 10000000;
# By adding the `@ray.remote` decorator, a regular Python function
# becomes a Ray remote function.
@ray.remote
def pi4_sample():
    in_count = 0
    for _ in range(SAMPLES):
        x, y = random(), random()
        if x*x + y*y <= 1:
            in_count += 1
    return in_count

@ray.remote
def pi4_minibatch(): 
    results = [] 
    for _ in range(MINIBATCHES):
        results.append(pi4_sample.remote())
    output = ray.get(results)
    return sum(output)
        
    

# To invoke this remote function, use the `remote` method.
# This will immediately return an object ref (a future) and then create
# a task that will be executed on a worker process. Get retreives the result. 
future = pi4_sample.remote()
pi = ray.get(future) * 4.0 / SAMPLES
print(f'{pi} is an approximation of pi') 

# With regular python this would take 11 hours
# Ray on a modern laptop, roughly 2 hours
# On a 10-node Ray cluster, roughly 10 minutes 
results = [] 
for _ in range(BATCHES):
    results.append(pi4_minibatch.remote())
output = ray.get(results)
pi = sum(output) * 4.0 / BATCHES / SAMPLES / MINIBATCHES
print(f'{pi} is a way better approximation of pi') 

