
# Respiratory Sound Analysis

Exploratory data analysis of respiratory sound recordings, patient demographics, diagnoses and annotated breathing cycles.

## Project Overview

This project explores a respiratory sound dataset to understand patient characteristics, respiratory diagnoses and abnormal breathing sounds.

The analysis combines patient-level information, breathing-cycle annotations and audio visualisations to investigate patterns across the dataset.

## Key Analyses

- **Patient demographics:** Age and sex distributions across respiratory diagnoses.
- **Respiratory diagnoses:** Patient counts and demographic differences.
- **Sound annotations:** Breathing-cycle durations and the occurrence of crackles, wheezes, both sounds or neither.
- **Relationships:** Sound types across diagnoses, age groups and chest recording locations.
- **Audio exploration:** Waveforms, spectrograms and Mel spectrograms of representative respiratory recordings.

## Tools and Techniques

Python, Pandas, NumPy, Matplotlib, Seaborn and Librosa.

Techniques include exploratory data analysis, data quality checks, dataset merging, distribution analysis and audio signal visualisation.

## Dataset

The analysis uses the Respiratory Sound Database, including audio recordings (`.wav`), breathing-cycle annotations (`.txt`), patient diagnoses and demographic information.

**Kaggle reference:** [Lung Disease Detection using Respiratory Sound](https://www.kaggle.com/code/anasnafisalmustofa/lung-disease-detection-using-respiratory-sound)

The linked Kaggle resource is a notebook referencing the respiratory sound data, rather than a direct dataset download page.

The dataset is not included in this repository. Download the data separately and update `DATASET_PATH`, `DEMOGRAPHIC_PATH` and `DIAGNOSIS_PATH` in the notebook to match your local or Google Drive directory.

## Notebook

[respiratory_sound_analysis.ipynb](respiratory_sound_analysis.ipynb)

The notebook contains the complete exploratory analysis, visualisations and audio signal comparisons.

**Note:** This project focuses on exploratory analysis rather than training or evaluating a respiratory disease classification model.
