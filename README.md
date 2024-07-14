# Text classifier for lawyers disciplinary actions: A large-scale empirical analysis
**Authors**: Michael Etienne Van Huffel, Anton Hul

## Project structure
- ``data/raw`` - Raw data obtained through public sources.
- ``data/csv_files`` - Separate csv files containing the preprocessed data for each state.
- ``corpus_preprocessing/preprocess_"state`` - Separate script for each state that preprocess the dataset.
- ``model/logreg`` - Logistic regression model training for 2 tasks of the project.
- ``model/fine-tuned bert`` - Fine-tuning BERT model training for 2 tasks of the project.
- ``model/pretrained bert`` - Pretrained BERT model training for 2 tasks of the project.
- ``⁠utils⁠`` - Contains utility scripts e.g., lemmatization function.

## Installation
To reproduce the analysis environment, you will need Python 3.9 or later. Please install the required Python packages listed in `requirements.txt`.

```bash
git clone git@github.com:majkevh/misconduct-lawyers.git
cd misconduct-lawyers
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.