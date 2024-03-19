import os



def main():
    if not os.path.exists('data/TMDB_movie_dataset_v11.csv'):
        import kaggle
        print('no csv found, downloading...', end='\r')
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files('asaniczka/tmdb-movies-dataset-2023-930k-movies', path='data', unzip=True)
        print('Done downloading TMDB_movie_dataset_v11.csv')

if __name__ == '__main__':
    main()
