# Author: Shiwen An 
# Date: 2022.08.04 
# Purpose: Try to make some Testing Neural Network and its Circuit. 
from cProfile import label
from errno import EPERM
import time
import matplotlib
import numpy as np
import paddle

from numpy import pi as PI
from matplotlib import pyplot as plt

from paddle import matmul, transpose, reshape
from paddle_quantum.ansatz import Circuit
from paddle_quantum.gate import BasisEncoding, AmplitudeEncoding, AngleEncoding, IQPEncoding
from paddle_quantum.gate import IQPEncoding

from paddle_quantum.qinfo import pauli_str_to_matrix # N qubits Pauli matrix
from paddle_quantum.linalg import dagger  # complex conjugate
import paddle_quantum

import sklearn
from sklearn import svm
from sklearn.datasets import fetch_openml, make_moons, make_circles
from sklearn.model_selection import train_test_split
import pandas as pd

from IPython.display import clear_output
from tqdm import tqdm

# import tutorial


def data():
  # class label, lepton 1 pT, lepton 1 eta, lepton 1 phi, lepton 2 pT, 
  # lepton 2 eta, lepton 2 phi, missing energy magnitude, missing energy phi, 
  # MET_rel, axial MET, M_R, M_TR_2, R, MT2, S_R, M_Delta_R, dPhi_r_b, cos(theta_r1)
  df = pd.read_csv("../data/HIGGS_10K.csv",names=('isSignal',
      'lep1_pt','lep1_eta','lep1_phi','miss_ene' ,'miss_ene_phi', 
      'jet_1_pt', 'jet_1_eta', 'jet_1_phi', 'jet_1_b_tag',
      'jet_2_pt', 'jet_2_eta', 'jet_2_phi', 'jet_2_b_tag',
      'jet_3_pt', 'jet_3_eta', 'jet_3_phi', 'jet_3_b_tag',
      'jet_4_pt', 'jet_4_eta', 'jet_4_phi', 'jet_4_b_tag',
      'm_jj', 'm_jjj', 'm_lv', 'm_jlv', 'm_bb', 'm_wbb', 'm_wwbb' ))
  
  df_test = pd.read_csv("../data/HIGGS_1K.csv",names=('isSignal',
      'lep1_pt','lep1_eta','lep1_phi','miss_ene' ,'miss_ene_phi', 
      'jet_1_pt', 'jet_1_eta', 'jet_1_phi', 'jet_1_b_tag',
      'jet_2_pt', 'jet_2_eta', 'jet_2_phi', 'jet_2_b_tag',
      'jet_3_pt', 'jet_3_eta', 'jet_3_phi', 'jet_3_b_tag',
      'jet_4_pt', 'jet_4_eta', 'jet_4_phi', 'jet_4_b_tag',
      'm_jj', 'm_jjj', 'm_lv', 'm_jlv', 'm_bb', 'm_wbb', 'm_wwbb' ))

  feature_dim = 3  # dimension of each data point
  # the feature could also be divided into 3 5 7
  if feature_dim == 3:
      SelectedFeatures = ['isSignal', 'lep1_pt', 'jet_1_pt', 'miss_ene']
  elif feature_dim == 5:
      SelectedFeatures = ['isSignal', 'jet_1_pt','jet_2_pt','miss_ene','jet_3_pt','jet_4_pt']
  elif feature_dim == 7:
      SelectedFeatures = ['isSignal', 'lep1_pt','lep1_eta','lep2_pt','lep2_eta','miss_ene','M_TR_2','M_Delta_R']

  print("Original Dataframe:")
  print(df)

  X = df[['lep1_pt', 'jet_1_pt', 'miss_ene']] 
  y = df[['isSignal']]

  X_test = df_test[['lep1_pt', 'jet_1_pt', 'miss_ene']] 
  y_test = df_test[['isSignal']]
  X_test = X_test.to_numpy()
  y_test = y_test.to_numpy()
  # X_test = X_test[0:20]
  # y_test = y_test[0:20]

  print(X)
  print(y)

  # Train Test split
  df_sig =  df[SelectedFeatures]
  df_bkg =  df[SelectedFeatures]


  df_sig = df_sig[df['isSignal'] == 1.0]
  df_bkg = df_bkg[df['isSignal'] == 0.0]

  print(df_sig)
  print(df_bkg)


  X = X.to_numpy()
  y = y.to_numpy()


  return X, y, X_test, y_test



# Test datapoint function


# Nice gate to look at
def Ry(theta):
    """
    :param theta: parameter
    :return: Y rotation matrix
    """
    return np.array([[np.cos(theta / 2), -np.sin(theta / 2)],
                     [np.sin(theta / 2), np.cos(theta / 2)]])

# Another nice gate to look at
def Rz(theta):
    """
    :param theta: parameter
    :return: Z rotation matrix
    """
    return np.array([[np.cos(theta / 2) - np.sin(theta / 2) * 1j, 0],
                     [0, np.cos(theta / 2) + np.sin(theta / 2) * 1j]])



# Start Creating Circuit and work on the function
def create_circuit(num_qubits, depth):
    # step 1.1: Create an N qubit circuit
    circuit = paddle_quantum.ansatz.Circuit(num_qubits)
    # step 1.2: Add gates to each layer
    for _ in range(0, depth):
        circuit.rx('full')
        circuit.rz('full')
        circuit.ry('full')
        circuit.cnot('linear')
    return circuit

def example():
  psi_target = np.kron(
    np.kron(np.array([1, 0]), np.array([0, 1])),
    np.array([1/np.sqrt(2), 1/np.sqrt(2)])
  )  # <01+|
  psi_target = paddle_quantum.state.to_state(paddle.to_tensor(psi_target), dtype=paddle_quantum.get_dtype())
  fid_func = paddle_quantum.loss.StateFidelity(psi_target)


# Write a new encoding for the data:
def built_in_angle_encoding(x_y_z):
  # Number of qubits
  n = 3 
  # x = paddle.to_tensor([np.pi, np.pi, np.pi], 'float64')
  x = paddle.to_tensor(x_y_z[0], 'float64')

  built_in_angle_enc = AngleEncoding(num_qubits=n, encoding_gate="ry", feature=x)
  # Classical information x should be of type Tensor
  # x = paddle.to_tensor([np.pi, np.pi, np.pi], 'float64')
  init_state = paddle_quantum.state.zero_state(n)
  state = built_in_angle_enc(state=init_state)
  # print(x)
  # print(init_state)
  # print("With Angle Encoding, the built in initial state is:")
  # print([np.round(i, 2) for i in state.data.numpy()])

  # Amplitude encoding is quite hard to realize
  # initially people use amplitude ...

  # Quantum computer is hard to realize the normalization
  # Angle encoding is relatively simpler

  print("[Now Encode all the states]")
  res = []
  for j in range(len(x_y_z)):
      # print(x_y_z[j])
      x = paddle.to_tensor(x_y_z[j], 'float64')

      built_in_angle_enc = AngleEncoding(num_qubits=n, encoding_gate="ry", feature=x)
      state = built_in_angle_enc(state=init_state)
      # print([np.round(i, 2) for i in state.data.numpy()])
      res.append([state.data.numpy()])
  
  return res


def Observable(n):
    r"""
    :param n: number of qubits
    :return: local observable: Z \otimes I \otimes ...\otimes I
    """
    Ob = pauli_str_to_matrix([[1.0, 'z0']], n)

    return Ob

# Define optimal classifier
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
        # ================ Model ===================
        for d in range(3, depth + 3):
            # The entanglement layer
            for i in range(n-1):
                self.circuit.cnot(qubits_idx=[i, i + 1])
            self.circuit.cnot(qubits_idx=[n-1, 0])
            # Add Ry to each qubit
            for i in range(n):
                self.circuit.ry(qubits_idx=i)
        # =========== Tutorial Example =============
        # 1. Hardware efficient =======
        # 2. ???? 

        print("Circuit obtained after initial optimization:")
        print(self.circuit)
        print("fi")

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


# Here just works for simplest 3 qubits case
if __name__ == '__main__' :
  df1, df2, X_test, y_test= data()
  print(df1)

  # This comes to real application case
  x_y_z = np.array(df1).reshape(-1, 3).astype("float64")
  t = np.array(df2)

  # 1 depth 3 qubit circuit
  myLayer = Opt_Classifier(n=3, depth=1)  # initialize quantum circuit
  LR = 0.01 # which is the learning rate
  opt = paddle.optimizer.Adam(learning_rate=LR, parameters=myLayer.parameters())

  Ntrain = len(df1)
  print("The Number of Training Set: ", Ntrain)
  BATCH = 20
  print("The Batch Size: ", BATCH)
  i = 0
  # Start of iteration
  EPOCH = int(BATCH/2)

  for ep in range(EPOCH):
    for itr in range( Ntrain // BATCH):
      input_state = []
      input_state = built_in_angle_encoding(x_y_z[itr*BATCH:(itr+1)*BATCH] )
      input_state = paddle.to_tensor(input_state)

      loss, train_acc, unused, cir \
        = myLayer(state_in = input_state, label=t[itr*BATCH:(itr+1)*BATCH])
      # Does my layer give any error from this function?
      # print(input_state)
      if i% 20 == 5 :
        print("[Should work]", int(i/20))
        
        input_state_test = paddle.to_tensor(built_in_angle_encoding(X_test))
        loss_useless, test_acc, state_predict_useless, t_cir \
                    = myLayer(state_in=input_state_test,label=y_test)
        print("epoch:", ep, 
              "iter:", itr,
              "loss: %.4f" % loss.numpy(),
              "train acc: %.4f" % train_acc,
              "test acc: %.4f" % test_acc)

      # Run back propagation to minimize the loss function
      loss.backward()
      opt.minimize(loss)
      opt.clear_grad()
      i += 1 

  num_qubits = 3
  depth = 1
  # cir = create_circuit(num_qubits, depth)
  # print(cir)