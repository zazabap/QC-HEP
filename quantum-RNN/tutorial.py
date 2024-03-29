# Import numpy,paddle and paddle_quantum
import numpy as np
import paddle
import paddle_quantum

# To construct quantum circuit
from paddle_quantum.ansatz import Circuit

# Some functions
from numpy import pi as PI
from paddle import matmul, transpose, reshape  # paddle matrix multiplication and transpose
from paddle_quantum.qinfo import pauli_str_to_matrix # N qubits Pauli matrix
from paddle_quantum.linalg import dagger  # complex conjugate

# Plot figures, calculate the run time
from matplotlib import pyplot as plt
import time

# Parameters for generating the data set
Ntrain = 200        # Specify the training set size
Ntest = 100         # Specify the test set size
boundary_gap = 0.5  # Set the width of the decision boundary
seed_data = 2       # Fixed random seed required to generate the data set
# Parameters for training
N = 4               # Number of qubits required
DEPTH = 1           # Circuit depth
BATCH = 20          # Batch size during training
EPOCH = int(200 * BATCH / Ntrain)
                    # Number of training epochs, the total iteration number "EPOCH * (Ntrain / BATCH)" is chosen to be about 200
LR = 0.01           # Set the learning rate
seed_paras = 19     # Set random seed to initialize various parameters

# Generate a binary classification data set with circular decision boundary
def circle_data_point_generator(Ntrain, Ntest, boundary_gap, seed_data):
    """
    :param Ntrain: number of training samples
    :param Ntest: number of test samples
    :param boundary_gap: value in (0, 0.5), means the gap between two labels
    :param seed_data: random seed
    :return: 'Ntrain' samples for training and
             'Ntest' samples for testing
    """
    # Generate "Ntrain + Ntest" pairs of data, x for 2-dim data points, y for labels.
    # The first "Ntrain" pairs are used as training set, the last "Ntest" pairs are used as testing set
    train_x, train_y = [], []
    num_samples, seed_para = 0, 0
    while num_samples < Ntrain + Ntest:
        np.random.seed((seed_data + 10) * 1000 + seed_para + num_samples)
        data_point = np.random.rand(2) * 2 - 1  # 2-dim vector in range [-1, 1]

        # If the modulus of the data point is less than (0.7 - gap), mark it as 0
        if np.linalg.norm(data_point) < 0.7-boundary_gap / 2:
            train_x.append(data_point)
            train_y.append(0.)
            num_samples += 1

        # If the modulus of the data point is greater than (0.7 + gap), mark it as 1
        elif np.linalg.norm(data_point) > 0.7 + boundary_gap / 2:
            train_x.append(data_point)
            train_y.append(1.)
            num_samples += 1
        else:
            seed_para += 1

    train_x = np.array(train_x).astype("float64")
    train_y = np.array([train_y]).astype("float64").T

    print("The dimensions of the training set x {} and y {}".format(np.shape(train_x[0:Ntrain]), np.shape(train_y[0:Ntrain])))
    print("The dimensions of the test set x {} and y {}".format(np.shape(train_x[Ntrain:]), np.shape(train_y[Ntrain:])), "\n")

    return train_x[0:Ntrain], train_y[0:Ntrain], train_x[Ntrain:], train_y[Ntrain:]

def data_point_plot(data, label):
    """
    :param data: shape [M, 2], means M 2-D data points
    :param label: value 0 or 1
    :return: plot these data points
    """
    dim_samples, dim_useless = np.shape(data)
    plt.figure(1)
    for i in range(dim_samples):
        if label[i] == 0:
            plt.plot(data[i][0], data[i][1], color="r", marker="o")
        elif label[i] == 1:
            plt.plot(data[i][0], data[i][1], color="b", marker="o")
    plt.show()

# Generate data set
train_x, train_y, test_x, test_y = circle_data_point_generator(
        Ntrain, Ntest, boundary_gap, seed_data)

# Visualization
print("Visualization of {} data points in the training set: ".format(Ntrain))
# data_point_plot(train_x, train_y)
print("Visualization of {} data points in the test set: ".format(Ntest))
# data_point_plot(test_x, test_y)
print("\n You may wish to adjust the parameter settings to generate your own data set!")

# Gate: rotate around Y-axis, Z-axis with angle theta
def Ry(theta):
    """
    :param theta: parameter
    :return: Y rotation matrix
    """
    return np.array([[np.cos(theta / 2), -np.sin(theta / 2)],
                     [np.sin(theta / 2), np.cos(theta / 2)]])

def Rz(theta):
    """
    :param theta: parameter
    :return: Z rotation matrix
    """
    return np.array([[np.cos(theta / 2) - np.sin(theta / 2) * 1j, 0],
                     [0, np.cos(theta / 2) + np.sin(theta / 2) * 1j]])

# Classical -> Quantum Data Encoder
def datapoints_transform_to_state(data, n_qubits):
    """
    :param data: shape [-1, 2]
    :param n_qubits: the number of qubits to which
    the data transformed
    :return: shape [-1, 1, 2 ^ n_qubits]
        the first parameter -1 in this shape means can be arbitrary. In this tutorial, it equals to BATCH.
    """
    # print(data)
    dim1, dim2 = data.shape
    # print("The dimension for the data: ")
    # print(dim1)
    res = []
    for sam in range(dim1):
        res_state = 1.
        zero_state = np.array([[1, 0]])
        # Angle Encoding
        for i in range(n_qubits):
            # For even number qubits, perform Rz(arccos(x0^2)) Ry(arcsin(x0))
            if i % 2 == 0:
                state_tmp=np.dot(zero_state, Ry(np.arcsin(data[sam][0])).T)
                state_tmp=np.dot(state_tmp, Rz(np.arccos(data[sam][0] ** 2)).T)
                res_state=np.kron(res_state, state_tmp)
            # For odd number qubits, perform Rz(arccos(x1^2)) Ry(arcsin(x1))
            elif i% 2 == 1:
                state_tmp=np.dot(zero_state, Ry(np.arcsin(data[sam][1])).T)
                state_tmp=np.dot(state_tmp, Rz(np.arccos(data[sam][1] ** 2)).T)
                res_state=np.kron(res_state, state_tmp)
        res.append(res_state)
    res = np.array(res, dtype=paddle_quantum.get_dtype())

    # print("The state after angle encoding: ")
    # print(res)
    
    return res

print("As a test, we enter the classical information:")
print("(x_0, x_1) = (1, 0)")
print("The 2-qubit quantum state output after encoding is:")
print(datapoints_transform_to_state(np.array([[1, 0]]), n_qubits=2))

# Generate Pauli Z operator that only acts on the first qubit
# Act the identity matrix on rest of the qubits
def Observable(n):
    r"""
    :param n: number of qubits
    :return: local observable: Z \otimes I \otimes ...\otimes I
    """
    Ob = pauli_str_to_matrix([[1.0, 'z0']], n)

    return Ob

# Quantum Circuit Learning
# https://arxiv.org/pdf/1803.00745.pdf
# Build the computational graph
class Opt_Classifier(paddle_quantum.gate.Gate):
    """
    Construct the model net
    """
    def __init__(self, n, depth, seed_paras=1):
        # Initialization, use n, depth give the initial PQC
        super(Opt_Classifier, self).__init__()
        self.n = n
        self.depth = depth
        # Initialize bias
        self.bias = self.create_parameter(
            shape=[1],
            default_initializer=paddle.nn.initializer.Normal(std=0.01),
            dtype='float32',
            is_bias=False)
        
        self.circuit = Circuit(n)
        # Build a generalized rotation layer
        for i in range(n):
            self.circuit.rz(qubits_idx=i)
            self.circuit.ry(qubits_idx=i)
            self.circuit.rz(qubits_idx=i)

        # The default depth is depth = 1
        # Build the entangleed layer and Ry rotation layer
        for d in range(3, depth + 3):
            # The entanglement layer
            for i in range(n-1):
                self.circuit.cnot(qubits_idx=[i, i + 1])
            self.circuit.cnot(qubits_idx=[n-1, 0])
            # Add Ry to each qubit
            for i in range(n):
                self.circuit.ry(qubits_idx=i)

    # Define forward propagation mechanism, and then calculate loss function and cross-validation accuracy
    def forward(self, state_in, label):
        """
        Args:
            state_in: The input quantum state, shape [-1, 1, 2^n] -- in this tutorial: [BATCH, 1, 2^n]
            label: label for the input state, shape [-1, 1]
        Returns:
            The loss:
                L = 1/BATCH * ((<Z> + 1)/2 + bias - label)^2
        """
        # Convert Numpy array to tensor
        Ob = paddle.to_tensor(Observable(self.n))
        label_pp = reshape(paddle.to_tensor(label), [-1, 1])

        # Build the quantum circuit
        Utheta = self.circuit.unitary_matrix()

        # Because Utheta is achieved by learning, we compute with row vectors to speed up without affecting the training effect
        state_out = matmul(state_in, Utheta)  # shape:[-1, 1, 2 ** n], the first parameter is BATCH in this tutorial

        # Measure the expectation value of Pauli Z operator <Z> -- shape [-1,1,1]
        E_Z = matmul(matmul(state_out, Ob), transpose(paddle.conj(state_out), perm=[0, 2, 1]))

        # Mapping <Z> to the estimated value of the label
        state_predict = paddle.real(E_Z)[:, 0] * 0.5 + 0.5 + self.bias  # |y^{i,k} - \tilde{y}^{i,k}|^2
        loss = paddle.mean((state_predict - label_pp) ** 2)  # Get average for "BATCH" |y^{i,k} - \tilde{y}^{i,k}|^2: L_i：shape:[1,1]

        # Calculate the accuracy of cross-validation
        is_correct = (paddle.abs(state_predict - label_pp) < 0.5).nonzero().shape[0]
        acc = is_correct / label.shape[0]
        # print(self.circuit)

        return loss, acc, state_predict.numpy(), self.circuit


# Draw the figure of the final training classifier
def heatmap_plot(Opt_Classifier, N):
    # generate data points x_y_
    Num_points = 30
    x_y_ = []
    for row_y in np.linspace(0.9, -0.9, Num_points):
        row = []
        for row_x in np.linspace(-0.9, 0.9, Num_points):
            row.append([row_x, row_y])
        x_y_.append(row)
    x_y_ = np.array(x_y_).reshape(-1, 2).astype("float64")

    # make prediction: heat_data
    input_state_test = paddle.to_tensor(
        datapoints_transform_to_state(x_y_, N))

    label1 = x_y_[:, 0]
    print(input_state_test, label1)
    loss_useless, acc_useless, state_predict, cir = Opt_Classifier(state_in=input_state_test, label=label1 )
    heat_data = state_predict.reshape(Num_points, Num_points)

    # plot
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    x_label = np.linspace(-0.9, 0.9, 3)
    y_label = np.linspace(0.9, -0.9, 3)
    ax.set_xticks([0, Num_points // 2, Num_points - 1])
    ax.set_xticklabels(x_label)
    ax.set_yticks([0, Num_points // 2, Num_points - 1])
    ax.set_yticklabels(y_label)
    im = ax.imshow(heat_data, cmap=plt.cm.RdBu)
    plt.colorbar(im)
    plt.show()

def QClassifier(Ntrain, Ntest, gap, N, DEPTH, EPOCH, LR, BATCH, seed_paras, seed_data):
    """
    Quantum Binary Classifier
    Input:
        Ntrain         # Specify the training set size
        Ntest          # Specify the test set size
        gap            # Set the width of the decision boundary
        N              # Number of qubits required
        DEPTH          # Circuit depth
        BATCH          # Batch size during training
        EPOCH          # Number of training epochs, the total iteration number "EPOCH * (Ntrain / BATCH)" is chosen to be about 200
        LR             # Set the learning rate
        seed_paras     # Set random seed to initialize various parameters
        seed_data      # Fixed random seed required to generate the data set
        plot_heat_map  # Whether to plot heat map, default True
    """
    # Generate data set
    train_x, train_y, test_x, test_y = circle_data_point_generator(Ntrain=Ntrain, Ntest=Ntest, boundary_gap=gap, seed_data=seed_data)
    # Read the dimension of the training set
    N_train = train_x.shape[0]
    
    paddle.seed(seed_paras)
    # Initialize the registers to store the accuracy rate and other information
    summary_iter, summary_test_acc = [], []

    # Generally, we use Adam optimizer to get relatively good convergence
    # Of course, it can be changed to SGD or RMSprop
    myLayer = Opt_Classifier(n=N, depth=DEPTH)  # Initial PQC
    opt = paddle.optimizer.Adam(learning_rate=LR, parameters=myLayer.parameters())


    # Optimize iteration
    # We divide the training set into "Ntrain/BATCH" groups
    # For each group the final circuit will be used as the initial circuit for the next group
    # Use cir to record the final circuit after learning.
    i = 0  # Record the iteration number
    for ep in range(EPOCH):
        # Learn for each group
        for itr in range(N_train // BATCH):
            i += 1  # Record the iteration number
            # Encode classical data into a quantum state |psi>, dimension [BATCH, 2 ** N]
            input_state = paddle.to_tensor(datapoints_transform_to_state(train_x[itr * BATCH:(itr + 1) * BATCH], N))
            # print([np.round(i, 2) for i in input_state.data.numpy()])
            if (i == 1 and itr ==0 and ep==0):
                print("The return value of data points are",datapoints_transform_to_state(train_x[itr * BATCH:(itr + 1) * BATCH], N) )
                print("The Input State Looks like: ", input_state)
            # Run forward propagation to calculate loss function
            loss, train_acc, state_predict_useless, cir \
                = myLayer(state_in=input_state, label=train_y[itr * BATCH:(itr + 1) * BATCH])  # optimize the given PQC
            # Print the performance in iteration
            if i % 30 == 5:
                # Calculate the correct rate on the test set test_acc
                input_state_test = paddle.to_tensor(datapoints_transform_to_state(test_x, N))
                loss_useless, test_acc, state_predict_useless, t_cir \
                    = myLayer(state_in=input_state_test,label=test_y)
                print("epoch:", ep, "iter:", itr,
                      "loss: %.4f" % loss.numpy(),
                      "train acc: %.4f" % train_acc,
                      "test acc: %.4f" % test_acc)
                # Store accuracy rate and other information
                summary_iter.append(itr + ep * N_train)
                summary_test_acc.append(test_acc) 

            # Run back propagation to minimize the loss function
            loss.backward()
            opt.minimize(loss)
            opt.clear_grad()
            
    # Print the final circuit
    print("The trained circuit:")
    print(cir)
    # Draw the decision boundary represented by heatmap
    heatmap_plot(myLayer, N=N)

    return summary_test_acc

def main():
    """
    main
    """
    time_start = time.time()
    acc = QClassifier(
        Ntrain = 200,    # Specify the training set size
        Ntest = 100,     # Specify the test set size
        gap = 0.5,       # Set the width of the decision boundary
        N = 4,           # Number of qubits required
        DEPTH = 1,       # Circuit depth
        BATCH = 20,      # Batch size during training
        EPOCH = int(200 * BATCH / Ntrain),
                        # Number of training epochs, the total iteration number "EPOCH * (Ntrain / BATCH)" is chosen to be about 200
        LR = 0.01,       # Set the learning rate
        seed_paras = 19, # Set random seed to initialize various parameters
        seed_data = 2,   # Fixed random seed required to generate the data set
    )
    
    time_span = time.time()-time_start
    print('The main program finished running in ', time_span, 'seconds.')

if __name__ == '__main__':
    main()
