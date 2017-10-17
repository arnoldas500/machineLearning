import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

#60k data of handwritten data samples (images of handwritten images)
mnist = input_data.read_data_sets("/tmp/data/", one_hot = True)
#dataset is 28 by 28

#one_hot parameter comes from electronics where 1 componenet will be hot and the rest are off 
#so one hot literarly means 1 is on and the rest are off

#can be useful for multi calss classification 

# 10 calsses, 0-9
'''
What 1 hot is doing
0 = [1,0,0,0,0,0,0,0,0]
1 = [0,1,0,0,0,0,0,0,0]
2 = [0,0,1,0,0,0,0,0,0]
3 = [0,0,0,1,0,0,0,0,0]
...
'''

'''
Feed forward neural network
input > weight > hidden layer 1 (activation function) > weights> hidden l 2
(activation function) > weights > output layer

compare output to inteded output with the cost or loss function (cross entropy)
then use an optimization function (optimizer) > minimize cost (AdamOptimizer...SGD, AdaGrad)

goes backeards and manipulates the weights - backpropagation 

then feed forward + backprop = epoch 
each time you do this you lower the cost every full cycle of epoch
'''


#building the model (dont have to be identical)
n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500
n_classes = 10 #0 to 9
#going to feed them to the network of batches of 100 at a time
batch_size = 100 

#x is the input data and can specify no hight by 784 pixels (since 28x28) wide
#y is the label of the data 
x = tf.placeholder('float', [None, 784])
y = tf.placeholder('float')

#the data is the raw input data
def neural_network_model(data):
    #puts your weights in one giant tensor that are random
    #biases are something that is added in after the weights so (input data * weights) + biases
    #if all of the input data is a zero then no neuron would ever fire so the bias would make it fire by adding a value to it
    #Weight - Weight is the strength of the connection. If I increase the input then how much influence does it have on the output.
    hidden_1_layer = {'weights':tf.Variable(tf.random_normal([784, n_nodes_hl1])),
                      'biases':tf.Variable(tf.random_normal([n_nodes_hl1]))}

    hidden_2_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                      'biases':tf.Variable(tf.random_normal([n_nodes_hl2]))}

    hidden_3_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                      'biases':tf.Variable(tf.random_normal([n_nodes_hl3]))}

    output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                    'biases':tf.Variable(tf.random_normal([n_classes]))}

#(input data * weights) + biases 
#matmul is matrix multi
    l1 = tf.add(tf.matmul(data,hidden_1_layer['weights']), hidden_1_layer['biases'])
    #relu is rectificed linear unit which is just your activation funciton (like threashold function)
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    output = tf.matmul(l3, output_layer['weights']) + output_layer['biases']

    return output


#specifying what we want to do with the model and how to send data through it

def train_neural_network(x):
    #the output is a one hot array (which is the prediction)
    prediction = neural_network_model(x)
    # OLD VERSION:
    #cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(prediction,y) )
    # NEW:
    #calc the difference between the prediction that we have to the known label
    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y) )
    
    #minimizng the cost (want it to be as small as possible (using adam)) learning rate default is 0.001
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    
    #cycles of feed forward + backpropagation
    hm_epochs = 10
    with tf.Session() as sess:
        # OLD:
        #sess.run(tf.initialize_all_variables())
        # NEW:
        sess.run(tf.global_variables_initializer())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            #under score ( _ ) is just basically variable we dont care about 
            #tells us how many times we need to cycle from our total number / batch size
            for _ in range(int(mnist.train.num_examples/batch_size)):
                #chuncks through dataset for you 
                epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c

            print('Epoch', epoch, 'completed out of',hm_epochs,'loss:',epoch_loss)

        #getting number of correct predictions
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float')) #casting correct to a float
        print('Accuracy:',accuracy.eval({x:mnist.test.images, y:mnist.test.labels}))

train_neural_network(x)
