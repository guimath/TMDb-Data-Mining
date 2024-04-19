import os



def main():
    if not os.path.exists('data/TMBD Movie Dataset.csv'):
        import kaggle
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files('successikuku/tmbd-movie-dataset', path='data', quiet=False, unzip=True)

if __name__ == '__main__':
    main()
