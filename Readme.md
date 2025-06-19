# 🎬 Movies Recommender System

Welcome to the **Movies Recommender System**, a complete end-to-end collaborative filtering project built using Python and deployed with Streamlit. The system is designed to suggest personalized movie recommendations based on real user ratings from the [MovieLens 100K dataset](https://grouplens.org/datasets/movielens/).

> ✨ Try the Live Demo: [Cornflix App](https://movies-recommender-system-cornflix.streamlit.app/)

---

## 🌍 Overview

This project explores multiple collaborative filtering approaches, compares their performance, and delivers a functional, interactive recommendation app.

### Goals:

- Build a recommendation engine using user ratings
- Compare classic and deep learning models
- Provide a live recommendation interface with Streamlit

---

## Dataset

- **Source**: MovieLens 100K
- **Users**: 610
- **Movies**: 9,742
- **Ratings**: 100,836
- **Files Used**: `ratings.csv`, `movies.csv`, `tags.csv`, `links.csv`

---

## Models Trained

| Model          | Type                          | MAE        | Notes                                |
| -------------- | ----------------------------- | ---------- | ------------------------------------ |
| SVD (baseline) | Matrix Factorization          | 0.7600     | Fast and simple baseline             |
| KNN Item-based | Memory-based CF               | 0.7615     | Interpretable but less accurate      |
| KNN User-based | Memory-based CF               | 0.7559     | Slight improvement                   |
| NCF (baseline) | Neural CF                     | 0.7004     | Strong performance via deep learning |
| NCF (tuned)    | Neural CF + tuning            | 0.6700     | Further optimized                    |
| SVD (tuned)    | Matrix Factorization + tuning | **0.6663** | ⭐ Best overall result                |

---

## Similar Movie Feature

We compute **item-item cosine similarity** from the user-item matrix to allow users to find movies similar to any selected one. This feature is available in the dashboard.

---

## 🚀 Live App

Streamlit was used to build an intuitive interface that allows users to:

- Select a user and get personalized movie recommendations
- Search for a specific movie and find similar ones
- View predicted ratings in real-time

> 🌐 Launch here: [Cornflix on Streamlit](https://movies-recommender-system-cornflix.streamlit.app/)

### 🎞App Screenshots

#### 🔹 Home Page

[![Home Page](https://drive.google.com/uc?export=view&id=17UcG1qARFy93tzuJOB72dKOH4BqmyELk)](https://drive.google.com/file/d/17UcG1qARFy93tzuJOB72dKOH4BqmyELk/view?usp=sharing)

#### 🔹 User Profile & Recommendations

[![User Page](https://drive.google.com/uc?export=view&id=1dbpyxyuoAVMwsWfrRtQoGaqcicvtuYe0)](https://drive.google.com/file/d/1dbpyxyuoAVMwsWfrRtQoGaqcicvtuYe0/view?usp=sharing)

#### 🔹 Movie Similarity Display

[![Movie Similarity](https://drive.google.com/uc?export=view&id=1nbMRnZaV1L1hPQ3m0f8nQlR-i6UkKxJe)](https://drive.google.com/file/d/1nbMRnZaV1L1hPQ3m0f8nQlR-i6UkKxJe/view?usp=sharing)

---

## 📄 Repository Structure

```
Movies-Recommender-System/
├── data/              # MovieLens dataset
├── models/            # Saved trained models (.pkl, .h5)
├── notebooks/         # EDA, training, evaluation
├── Deployment/        # Streamlit app and utils
├── reports/           # Final model report
├── README.md          # Project summary and usage
```

---

## ✨ Future Improvements

- Add hybrid recommendation (CF + content-based)
- Improve cold-start handling for new users/items
- Include more metadata (e.g., genres, tags, timestamps)
- Containerize the app with Docker for production use

---

## Authors

- [Mennatullah Tarek](https://github.com/MennatullahTarek)
- [Mohamed Elsharkawy](https://github.com/mohamedelsharkawy-coder)
- [Hajar Elbehairy](https://github.com/HajarElbehairy)

---

## 💡 License

MIT License. Feel free to use and adapt this project.

