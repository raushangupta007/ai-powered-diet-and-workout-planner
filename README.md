# 🏋️‍♂️ AI-Powered Diet & Workout Planner

An automated, data-driven Health & Fitness web application built using **Python** and **Streamlit**. The system serves as a personalized AI coach that calculates daily caloric and macronutrient targets using scientific metabolic equations, dynamically filters nutritional food sources, and structures customizable workout routines tailored to individual user profiles.

---
---

## 🚀 Production Deployment
🌍 **Live Application:** [Live](https://ai-powered-diet-and-workout-planner-1.onrender.com/)

---



## 🚀 Features

- **Personalized Metabolic Profiling:** Implements the *Mifflin-St Jeor Equation* to accurately calculate Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE).
- **Macro-Nutrient Goal Structuring:** Automatically distributes target grams for Proteins, Carbs, and Fats based on chosen goals (*Weight Loss, Muscle Gain, or Maintenance*).
- **AI Diet Recommendation Engine:** Computes a specialized "Protein Density Score" to extract and rank optimal food sources from a database of over several hundred items.
- **Content-Based Workout Generator:** Filters a comprehensive catalog of exercises by experience level (*Beginner, Intermediate, Expert*) and dynamically compiles schedules for target muscle groups.
- **Modern Responsive Dashboard UI:** Built with custom-engineered styling components, clean data visualization metrics, and interactive multi-select filters.

---

## 📊 Dataset Requirements

The application utilizes two crucial underlying CSV files which must be placed in the root directory:
1. `megaGymDataset.csv` - Contains comprehensive multi-level columns including: `Title`, `Desc`, `Type`, `BodyPart`, `Equipment`, `Level`, and `Rating`.
2. `nutrients_csvfile.csv` - Contains detailed nutritional breakdowns including: `Food`, `Measure`, `Calories`, `Protein`, `Fat`, `Carbs`, and `Category`.

ct directory using the change directory (`cd`) command:
```bash
cd path/to/your/project-folder
