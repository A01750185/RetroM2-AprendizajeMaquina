# -*- coding: utf-8 -*-
"""MomentoRetroM2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MpjVTQvTB4YNCQ2Y0t1ih9fi7uRmaXoK

# **Momento de Retroalimentación: Módulo 2 Implementación de una técnica de aprendizaje máquina sin el uso de un framework. (Portafolio Implementación)**

**Amy Murakami Tsutsumi - A01750185**

Para este portafolio se analizarán los datos del clima en Szeged, Hungría del año 2006-2016. Este dataset se obtuvo de la siguiente liga: https://www.kaggle.com/datasets/budincsevity/szeged-weather

Únicamente se utilizarán los primeros 100 datos de las columnas de temperatura y humedad. De esta manera se podrá predecir si existe una relación entre estos valores y si se puede predecir la humedad al tener el dato de la temperatura.

### **Lectura de datos**
"""

# Commented out IPython magic to ensure Python compatibility.
"""
from google.colab import drive
drive.mount("/content/gdrive") 
# %cd "/content/gdrive/MyDrive/Séptimo Semestre/Mod2"
"""

"""Para la implementación del modelo de regresión lineal no se utilizará ninguna librería. Sin embargo, será necesario el uso de librerías para poder graficar y para realizar el subset de entrenamiento. Por lo tanto, las librerías que se utilizarán para estos procesos son:
* *pandas* : Para la creación y operaciones de dataframes.
* *matplotlib.pyplot* : Para la generación de gráficos.
* *numpy* : Para la creación de vectores y matrices.
* *sklearn.model_selection - train_test_split* : Para la división de los datos en subconjuntos de entrenamiento y prueba.



"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

"""### **Entendimiento de los datos**"""

df = pd.read_csv('weatherHist.csv') #Leer el dataset
df.head()

"""En la tabla anterior se muestran las columnas en el dataset que son la de temperatura en grados centígrados y humedad que es un valor entre 0 y 1. Ambos valores son de tipo float.
Ahora se realizará un plot para poder visualizar gráficamente de qué manera se comportan las variables. 
"""

df.plot()

temp = df['Temperature (C)'] #Variable de temperatura 
humidity = df['Humidity'] #Variable de humedad
temp.head()

"""Se realizará una matriz de correlación para determinar la relación entre ambas variables. """

# Matriz de Correlación
corr = df.corr()
corr.style.background_gradient(cmap='coolwarm')

"""Como podemos observar, la correlación entre temperatura y humedad es muy elevada.

### **Modularización del data-set**

Ahora se realizará la división de datos en subsets de entrenamiento y prueba.
"""

#Modularización del data-set
x_train, x_test, y_train, y_test = train_test_split(temp, humidity, test_size = 0.20, train_size = 0.80, random_state= 2)

"""### **Modelo de predicción**

Para realizar las predicciones se utilizará el modelo de regresión lineal. Por lo tanto, se utilizarán las siguientes fórmulas: 

$θ_0 = θ_0 - α \frac{1}{n} 
\sum_{i=1}^{n}(h_{0}(x_{i})+y_{i}) 
 $

$θ_1 = θ_1 - α \frac{1}{n} 
\sum_{i=1}^{n}(h_{0}(x_{i})+y_{i})x_i 
 $
"""

def h(temp,theta):
  # Calcular la función de hipótesis
  return theta[0] + theta[1]*temp

def regLin(temp, humidity, alpha, iter):
  # Calcular la regresión lineal
  theta = [1,1] # Valores de theta_i del modelo [theta_0, theta_1]
  n =len(temp) # Número de datos

  print("Theta inicial: ", theta)

  for idx in range(iter):
    # Listas para almacenar los valores de h, theta 0 y theta 1
    allh = []
    delta = []
    deltaX =[]

    for x_i,y_i in zip(temp,humidity):
      # Almacenar valores calculados de h, theta 0 y theta 1 de cada iteración
      allh.append(h(x_i,theta))
      delta.append(h(x_i,theta)-y_i)
      deltaX.append((h(x_i,theta)-y_i)*x_i)

    # Cálculo final del theta 0 y theta 1
    theta[0] = theta[0] - alpha/n*sum(delta) #Cálculo de theta 0
    theta[1] = theta[1] - alpha/n*sum(deltaX) #Cálculo de theta 1

  print("Theta final: ", theta)

  # Graficar la regresión lineal
  plt.title("Regresión lineal del clima en Szeged (2006-2016)", fontsize=16)
  plt.scatter(temp, humidity, marker='.', color="yellowgreen")
  #plt.plot(temp, theta0 + theta1*temp, color="mediumturquoise")
  plt.plot(temp, theta[0] + theta[1]*temp, color="mediumturquoise")
  plt.xlabel("Temperatura")
  plt.ylabel("Humedad")
  plt.show()

  return allh

def metricaDesemp (pred):
  # Obtener la métrica de desempeño de los modelos
  correlation_matrix = np.corrcoef(y_train, pred)
  correlation = correlation_matrix[0,1]
  r_squared = correlation**2
  return r_squared

"""### **Pruebas con diferentes parámetros**

Se realizarán 5 pruebas con diferentes parámetros con los datos de entrenamiento para poder elegir el modelo con mejor desempeño.
"""

predic = []
pred1 = regLin(x_train, y_train, 0.0005, 100000) 
met1 = metricaDesemp(pred1)
predic.append(met1)
print("Métrica de desempeño de la prueba 1: ", met1)

pred2 = regLin(x_train, y_train, 0.00001, 100000) 
met2 = metricaDesemp(pred2)
predic.append(met2)
print("Métrica de desempeño de la prueba 2: ", met2)

pred3 = regLin(x_train, y_train, 0.001, 10000) 
met3 = metricaDesemp(pred3)
predic.append(met3)
print("Métrica de desempeño de la prueba 3: ", met3)

pred4 = regLin(x_train, y_train, 0.005, 5500) 
met4 = metricaDesemp(pred4)
predic.append(met4)
print("Métrica de desempeño de la prueba 4: ", met4)

pred5 = regLin(x_train, y_train, 0.0015, 100000) 
met5 = metricaDesemp(pred5)
predic.append(met5)
print("Métrica de desempeño de la prueba 5: ", met5)

"""Ahora se comparará el desempeño de las cinco pruebas para poder elegir los parámetros que se utilizarán para realizar las predicciones."""

print(predic)
print(max(predic))

"""Como se puede observar los parámetros de la tercera prueba son los indicados con un alpha de 0.001 y 10000 iteraciones.

### **Predicción**
"""

predF = regLin(x_test, y_test, 0.001, 10000)

"""La siguiente tabla muestra los valores de entrada, el valor real esperado y los resultados de la predicción utilizando un alpha de 0.001 y 10000 iteraciones."""

pd.set_option('max_columns', None)
dfEntPred = pd.DataFrame()
dfEntPred["Entrada"] = x_test
dfEntPred["Valor Real Esperado"] = y_test
dfEntPred["Predicción"] = predF      
dfEntPred

"""En la tabla anterior se puede vizualizar qué tanto varía el valor real esperado con el valor que se obtuvo en la predicción. """