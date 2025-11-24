# Project Statement  
## Stress Level Prediction System

### Introduction  
This project focuses on designing a simple and interpretable system that predicts the stress level of a person using basic lifestyle-related features. The goal is to apply object-oriented programming concepts while demonstrating a clear and explainable prediction model.

### Objective  
- To estimate an individual's stress level using measurable factors such as heart rate, sleep duration, and work hours.  
- To implement a readable, maintainable, and modular Python program using OOP principles.  
- To display predictions in a clean, user-friendly format.

### Problem Description  
Stress is influenced by both physiological and behavioral factors. High work hours, low sleep, and elevated heart rate often correlate with increased stress. This project uses these three parameters to produce a stress score within a 0–100 range and categorize the result as **Low**, **Moderate**, or **High** stress.

### Approach  
1. Data for each individual is stored in a `Person` class containing:  
   - Name  
   - Average heart rate  
   - Daily sleep duration  
   - Weekly work hours  

2. A `StressPredictor` class computes the stress score using a linear equation with fixed weights.  
3. The output includes both the numerical score and a risk category.  
4. The program supports sample data, manual user input, and CSV-based input.

### Scope  
The project includes:  
- OOP-based data representation  
- A simple linear prediction model  
- Risk classification  
- Interactive and CSV-based input options  
- Clean tabular output  
- Optional CSV export of results  

### Conclusion  
The Stress Level Prediction System provides a clear demonstration of OOP concepts, simple mathematical modeling, and user-friendly program design. Although not a medical diagnostic tool, it effectively illustrates how basic data can be used to estimate stress levels in an understandable way.
