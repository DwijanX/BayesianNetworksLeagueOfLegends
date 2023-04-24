import os
os.environ['MKL_THREADING_LAYER'] = 'GNU'

import multiprocessing
print(f"Number of CPU cores: {multiprocessing.cpu_count()}")
os.environ['MKL_NUM_THREADS'] = '12'
os.environ['OPENBLAS_NUM_THREADS'] = '12'
os.environ['OMP_NUM_THREADS'] = '12'

import theano
theano.config.gcc.cxxflags = "-Wno-c++11-narrowing"
theano.config.mode = 'FAST_RUN'

import pymc3 as pm
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
np.seterr(all='ignore')


X = pd.read_csv('XValuesDataSet.csv')
Y = pd.read_csv('YValuesDataSet.csv')


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.5)

# Normalizar variables de entrada
X_train = (X_train - X_train.mean()) / X_train.std()

# calcula las medias y desviaciones estándar de cada columna
media = X_train.mean()
desviacion = X_train.std()



with pm.Model() as model:
    # crea variables aleatorias normales para cada columna
    betas = pm.Normal('betas', mu=media, sd=desviacion, shape=X_train.shape[1])
    
    # Probabilidad de éxito
    p = pm.math.sigmoid(pm.math.dot(X_train, betas))
    # Variable objetivo
    Y_train = pm.Bernoulli('y', p=p, observed=Y)
    
    # Inferencia de parámetros
    trace = pm.sample(100, tune=100, cores=12)


# Crear lista vacía para guardar predicciones
predictions = []

# Loop sobre los valores de X_test y Y_test
for i in range(len(X_test)):
    # Obtener valor de X_test e Y_test para esta iteración
    x = X_test.iloc[[i]]
    y = Y_test.iloc[[i]]

    # Calcular probabilidad de éxito con el modelo
    with model:
        p = pm.math.sigmoid(pm.math.dot(x, betas))

    result_str = str(p)
    result_char = result_str[-1]
    result_float = float(result_char)

    # Obtener predicción como 1 o 0 según la probabilidad
    prediction = 1 if result_float > 0.5 else 0

    # Añadir predicción a la lista
    predictions.append(prediction)

# Comparar predicciones con valores reales
correct = 0
for i in range(len(Y_test)):
    if predictions[i] == Y_test.iloc[i, 0]:
        correct += 1

# Calcular accuracy
accuracy = correct / len(Y_test)
print(f"Accuracy: {accuracy}")