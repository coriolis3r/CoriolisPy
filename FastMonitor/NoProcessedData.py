
# save numpy array as npy file
from numpy import asarray
from numpy import save
from numpy import load
# define data
data = asarray([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]])
arr=[['a',123],[1,2]]

# save to npy file
save('data.npy', arr)
# load array
data = load('data.npy')
# print the array
print(data)