# TMDb-Data-Mining
Data mining project for class CS5228, School of Computing, NUS.

CSV source is not included in this github so first you need to download it.
- With kaggle API token simply run [start.py](start.py) (see the [API documentation](https://technowhisp.com/kaggle-api-python-documentation/) for more info)
- directly from the [kaggle page for TMDb](https://www.kaggle.com/datasets/successikuku/tmbd-movie-dataset)

All python libs used are in [requirements.txt](requirements.txt).

## Files

|File name| Description|
|-|-|
| TMDB Movie Dataset.csv  | Processed data set |
| Movie_analysis.ipynb | Preprocessing, data visualisation & regression notebook |
| preprocess_and_split_dataset.ipynb | Simplified version of notebook Movie_analysis.ipynb to automatically split the dataset while respecting the release date for a chosen train/testratio |
| dataset_train*.csv | Training dataset for a given ratio built using the notebook preprocess_and_split_dataset.ipynb |
| dataset_train*.csv | Test dataset for a given ratio built using the notebook preprocess_and_split_dataset.ipynb |
| regression_classification.ipynb | K-means++ clustering, regression, prediction, feature importance analysis and split ratio influence evaluation with a comparative study between different models |
| saved_models/{Type of regressor} {target feature}.pkl | Optimal model of type {Type of regressor} obtained thourgh gridsearch using notebook regression_classification.ipynb for the target feature {target feature}.|
| actors_graph.py | Graph structure extraction |
| start.py | Download dataset from kaggle |


For more information about the project see the [project report](Data_mining_project.pdf)

