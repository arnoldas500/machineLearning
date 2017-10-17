#tensorflow is matrix manipulation libraries
#a tensor is pretty much just an array of any size
#tensorflow is just functions on arrays
#first define the model in abstract terms and then you run the model and get results back

import tensorflow as tf

# creates nodes in a graph
# "construction phase"
x1 = tf.constant(5)
x2 = tf.constant(6)

#can multiply them
result = tf.mul(x1,x2)
print(result)

# defines our session and launches graph
sess = tf.Session()
# runs result
print(sess.run(result))

#can assign the output from the session to a new variable 
output = sess.run(result)
print(output)

#close the session to free up reasources
sess.close()
#or always use
'''
with tf.Session() as sess:
    output = sess.run(result)
    print(output)
'''

'''
You can also use TensorFlow on multiple devices, and even multiple distributed machines. An example for running some computations on a specific GPU would be something like:
'''
with tf.Session() as sess:
  with tf.device("/gpu:1"):
    matrix1 = tf.constant([[3., 3.]])
    matrix2 = tf.constant([[2.],[2.]])
    product = tf.matmul(matrix1, matrix2)

