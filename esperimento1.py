from tensorflow import keras
import matplotlib
from keras.preprocessing import sequence
import matplotlib.pyplot as plt
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Conv1D, MaxPool1D, Dropout, BatchNormalization,Embedding,LSTM, Bidirectional
from sklearn.decomposition import PCA
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Reshape
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import classifier_manager.model_interface.dataset_provider as dp
from keras.datasets import imdb
from keras.utils import to_categorical

def split_set(dataset, test_length):
    indexes = []
    test =  []
    train = []
    for i in range(test_length):
        new = False
        while(not new):
            r = random.randint(0, len(dataset))
            if r not in indexes:
                new = True
                indexes.append(r)
    for i in range(len(dataset)):
        if i in indexes:
            test.append(dataset[i])
        else:
            train.append(dataset[i])
    if len(test) == 0:
        test.append(train.pop(0))
    return test,train

desc, labels = dp.read_xlsx( path='LDC.xlsx', sheet_name = 'LDC', level=1)

# fashion_mnist = keras.datasets.fashion_mnist
# (X_trn, y_trn), (X_tst, y_tst) = fashion_mnist.load_data()
(X_trn, y_trn), (X_tst, y_tst) = imdb.load_data(num_words=5000)
y_names = list(set(labels))
y_names.sort()
y_values = dict([(l,i) for i,l in enumerate(y_names)])
# labels = [target_values[l] for l in labels]
test, train = split_set(list(zip(desc,labels)), (len(desc) // 10) * 2 )
vectorizer = TfidfVectorizer(max_features=500)

X_train = vectorizer.fit_transform([t[0] for t in train]).toarray()
y_train = to_categorical(np.array([y_values[t[1]] for t in train]))
X_test = vectorizer.fit_transform([t[0] for t in test]).toarray()
y_test = to_categorical(np.array([y_values[t[1]] for t in test]))

print(X_train[1])
print(f'input shape: {X_train.shape}')
eta = 0.01
alpha = 0.9
batch_size = 64

epochs = 20  # Numero alto, per rendere più probabile l'early stopping
patience = 5
model = Sequential()
model.add(Embedding(500, 64))
model.add(Bidirectional(LSTM(64)))
model.add(Dropout(0.5))
# model.add(Dense(64, activation= 'relu'))
# model.add(Dense(64, activation= 'relu'))
model.add(Dense(7, activation = 'softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['acc'])
# model = Sequential([
#     Reshape(target_shape=(12803, 1)),
#     # Blocco convolutivo (Conv + ReLU + MaxPool)
#     Conv1D(16, 3, strides=1, padding='valid', activation='relu'),
#     MaxPool1D(pool_size=2, strides=2, padding='valid'),
#     Flatten(),
#     # Fully Connected (Dense + ReLU)
#     Dense(64, activation='relu'),
#     # Strato di output (Dense + Softmax)
#     Dense(len(y_names), activation='softmax')
# ])


# Parametri per l'apprendimento
# model.compile(optimizer=SGD(learning_rate=eta, momentum=alpha),
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

# Apprendimento (il criterio di terminazione sarà early stopping o il numero di epoche)
history = model.fit(X_train, y_train, verbose=1,
                    epochs=epochs,
                    batch_size=batch_size,
                    callbacks=[EarlyStopping(monitor='val_acc', patience=patience, restore_best_weights=True)],
                    validation_split=0.1)

# Tengo memoria degli errori
errors = []

print('\nDone!')

train_loss, train_accuracy = model.evaluate(X_train, y_train, verbose=0)
print(f'\nTraining error is {train_loss:.4f}')
print(f'Training accuracy is {100*train_accuracy:.2f}%')

# best_epoch = np.argmin(history.history['val_loss'])
best_epoch = np.argmax(history.history['val_acc'])
print(f'\nValidation error is {history.history["val_loss"][best_epoch]:.4f}')
print(f'Validation accuracy is {100*history.history["val_acc"][best_epoch]:.2f}%')

plt.title('Cross-Entropy Loss')
plt.plot(history.history['loss'], label='Training')
plt.plot(history.history['val_loss'], label='Validation', ls='--')
plt.xlabel('t')
plt.ylabel('L(ỹ, y)')
plt.legend()
plt.show()

plt.title('Accuracy')
plt.plot(history.history['accuracy'], label='Training')
plt.plot(history.history['val_acc'], label='Validation', ls='--')
plt.xlabel('t')
plt.ylabel('accuracy')
plt.legend()
plt.show()

_, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Test accuracy is {100*test_accuracy:.2f}%')