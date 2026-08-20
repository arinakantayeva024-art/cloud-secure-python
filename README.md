
# 🌾 Crop Yield Prediction using Machine Learning

🚀 [Live Demo](https://crop-yield-prediction1.streamlit.app/)  
📂 [Dataset]([(https://drive.google.com/file/d/1a7paF89c9I5ChaL4SCW_vNlIPAWU6bZl/view
]).

---

## 📌 Project Overview

This project predicts **crop yield (in kg/acre)** based on key farm attributes using a machine learning model. It provides an easy-to-use web dashboard where farmers, agronomists, or researchers can input soil and environmental conditions to estimate expected crop yield.

---

## 🎯 Why This Project?

- 🌾 Helps **farmers** make data-driven decisions for crop planning.
- 📉 Reduces risk by estimating **yield before harvest**.
- 🧠 Demonstrates practical application of **ML in agriculture**.
- 💻 Built with an intuitive **Streamlit interface** for non-technical users.

---

## 🧪 Features

- 🔍 Predicts yield based on:
  - Temperature (°C)
  - Rainfall (mm/year)
  - Pesticide usage (tonnes)
  - Soil Type (Sandy, Clay, Loamy, Silt)
  - Nutrient levels: Nitrogen, Phosphorus, Potassium (%)
- 📦 Trained model stored securely in **Google Drive** and auto-downloaded on demand.
- 📊 Displays model performance (R² score and accuracy).
- 🌐 Deployed publicly using **Streamlit Cloud**.

---

## 📸 App Screenshot

![image](https://github.com/user-attachments/assets/015dfc1a-0fe6-48b7-ae18-0ed584781d87)


---

## 🧠 Tech Stack

| Technology       | Purpose                         |
|------------------|----------------------------------|
| Python           | Core programming language       |
| Streamlit        | Web UI / Dashboard              |
| Scikit-learn     | Machine learning model          |
| Pandas, NumPy    | Data preprocessing              |
| Joblib, Gdown    | Model loading from Google Drive |
| Google Drive     | Hosting the `.pkl` model file   |

---

## 📊 Model Performance

| Metric       | Value |
|--------------|-------|
| R² Score     | 0.87  |
| Accuracy     | 82%   |

- Trained using `RandomForestRegressor`
- Dataset size: _(custom / real-world based)_

---

## 🗃 Dataset

Custom dataset containing:
- Temperature
- Rainfall
- Pesticide usage
- Soil Type (Categorical)
- Nitrogen, Phosphorus, Potassium
- Target: Yield (in hectograms/hectare, later converted to kg/acre)

Stored locally in: `yield_df.csv`

---


### ✅ Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

### ▶️ Run the app

```bash
streamlit run app.py
```

> The model will automatically download from Google Drive if not found locally.

---

## 🌐 Deployment

Deployed using **Streamlit Cloud**  
🔗 [Live Demo](https://crop-yield-prediction1.streamlit.app/)

---

## 📁 Project Structure

```
crop-yield-prediction/
├── app.py                  # Streamlit web app
├── crop_yield_model.pkl    # (Ignored in GitHub, loaded from Drive)
├── requirements.txt
├── README.md
├── notebooks/              # Model training notebooks
├── data/                   # Dataset files
```

---

## 🙋‍♂️ Author

**Maila Sai Vamshi**  
📫 [LinkedIn](https://www.linkedin.com/in/sai-vamshi23/).

---

