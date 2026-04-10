# PROGRAM START
print("PROGRAM START")

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
try:
    print("Loading data...")

    # 👉 Full path use (safe)
    data = pd.read_csv(r"C:\Users\findd\Desktop\cooling_tower_ai\cooling_data.csv")

    print("DATA LOADED SUCCESS")
    print(data.head())

    # 👉 Features & Target
    X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
    y = data['Temperature']

    # 👉 Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # 👉 Model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 👉 Prediction
    pred = model.predict(X_test)

    print("Prediction:", pred)

except Exception as e:
    print("ERROR:", e)

    import matplotlib.pyplot as plt

plt.scatter(y_test, pred)
plt.xlabel("Actual Temperature")
plt.ylabel("Predicted Temperature")
plt.title("Actual vs Predicted")
plt.show()