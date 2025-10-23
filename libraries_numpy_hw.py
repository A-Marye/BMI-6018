# 1. Import numpy as np and print the version number. (5 Points)
import numpy as np
print(np.__version__)

# 2. Create a 1D array of numbers from 0 to 9. Desired output: array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) (10 Points)
np_array = np.array([0,1,2,3,4,5,6,7,8,9])
print(np_array)

# 3. Import a dataset with numbers and texts keeping the text intact in python numpy. Use the iris dataset available 
# from https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.dataLinks to an external site.. (20 Points)
data_type = np.dtype([('num_1', 'f8'), ('num_2', 'f8'), ('num_3', 'f8'), ('num_4', 'f8'), ('Name', 'U15')])
iris = np.genfromtxt("iris.data.txt", dtype = data_type, encoding = None, delimiter = ",")
print(iris)

# 4. Find the position of the first occurrence of a value greater than 1.0 in petalwidth 4th column of iris dataset. 
# Use the iris dataset available from https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.dataLinks to an external site.. (20 Points)
indices = np.where(iris['num_4'] > 1.0)

if indices[0].size > 0:
    first_occurrence_index = indices[0][0]
    print(first_occurrence_index)
else:
    first_occurrence_index = "Not found"

# 5. From the array a, replace all values greater than 30 to 30 and less than 10 to 10. (20 points)
# Input:
# np.random.seed(100)
# a = np.random.uniform(1,50, 20)

np.random.seed(100)
a = np.random.uniform(1,50, 20)
print(a)

for i in range(len(a)):
    if a[i] < 10:
        a[i] = 10
    elif a[i] > 30:
        a[i] = 30
        
print(a)