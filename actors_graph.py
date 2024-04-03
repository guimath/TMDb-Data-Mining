import networkx as nx
# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def onehotencode(dataset,col):
    _df = pd.DataFrame()
    _df[col] = dataset[col].str.split('|')
    one_hot_encoded = pd.get_dummies(_df[col].apply(pd.Series).stack()).groupby(level=0).sum()
    return one_hot_encoded

def make_gexf(csv_file, gexf_file= 'actors_graph.gexf'):
    with open(csv_file, encoding='utf-8') as f:
        df1 = pd.read_csv(f) # CSV not in utf8 ?
    df = df1[['revenue', 'cast', 'original_title', 'director', 'production_companies']]
    df = df.loc[df['revenue']>1e7]
    n_movie= df.shape[0]

    # CAST 
    OHE_cast = onehotencode(df,"cast") 
    OHE_cast_n = OHE_cast.to_numpy()
    # directors =  df['director'].values
    movies = df['original_title'].values
    revenue = df['revenue'].values
    graph = nx.Graph()

    # GETTING BIGGEST COMPANIES
    OHE_comp  = onehotencode(df, 'production_companies')
    comps = OHE_comp.columns
    num = np.zeros(len(comps))
    for i, comp in enumerate(comps) : 
        num[i] = OHE_comp[comp].sum()

    idx = np.argsort(num,axis=0)
    big_comp = comps[idx[-6:]]
    OHE_comp = OHE_comp[big_comp]

    print(list(zip(big_comp, ['Violet', 'blue', 'cyan', 'green', 'yellow', 'red'])))
    print('(Other, grey)')
    COLOR = {
        big_comp[0] : {"r": 88, "g": 58, "b": 113},
        big_comp[1] : {"r": 97, "g": 132, "b": 216},
        big_comp[2] : {"r": 80, "g": 197, "b": 183},
        big_comp[3] : {"r": 156, "g": 236, "b": 91},
        big_comp[4] : {"r": 240, "g": 244, "b": 101},
        big_comp[5] : {"r": 233, "g": 40, "b": 40},
        'Other'     : {"r": 200, "g": 200, "b": 200},
    }
    colors, size = [], []

    OHE_cast_n = OHE_cast.to_numpy()
    distinct = []
    for i, act in enumerate(OHE_cast.columns) : 
        link_num = np.sum([OHE_cast_n[:,i]&OHE_cast_n[:,j] for j in range(len(OHE_cast.columns)) if i != j])
        if link_num>5 and OHE_cast[act].sum()>2:
            distinct.append(act)
            graph.add_node(act)

            _d = OHE_comp.iloc[np.where(OHE_cast[act]!=0)].sum()
            if _d.max() < 1:
                cat_comp = 'Other'
            else:
                cat_comp = _d.idxmax()
            colors.append(cat_comp)
            size.append(df['revenue'].values[np.where(OHE_cast[act] !=0)].mean())
        else :
            OHE_cast_n[:,i] =OHE_cast_n[:,i]*0 
    OHE_cast = OHE_cast[distinct]
    OHE_cast_n = OHE_cast.to_numpy()

    size = np.array(size)
    min_r, max_r = size.min(), size.max()
    delta = max_r - min_r
    size = (((size-min_r)/delta) * 400) +20
    for i, name in enumerate(graph.nodes.keys()):
        graph.nodes[name]["viz"] = {
            'size': int(size[i]),
            'color': COLOR[colors[i]]                  
        }

    # Edges computing
    for i in range(len(distinct)):
        for j in range(i+1, len(distinct)):
            combined = OHE_cast_n[:,i]& OHE_cast_n[:,j]
            weight = combined.sum()
            if weight > 0 : 
                # edge label is list of all shared movies 
                label = str(movies[np.where(combined==1)].tolist()).replace('[', '').replace(']', '').replace('\'', '') 
                # print(f'{distinct[i]:23s} -> {distinct[j]:23s} ({label}) {weight}')
                graph.add_edge(distinct[i], distinct[j], weight=int(3**(weight-1)), label=label)
    
    # save as gexf for gephi processing
    nx.write_gexf(graph, gexf_file)
    print(f'{gexf_file} saved')

if __name__ == '__main__':
    make_gexf('data/TMBD Movie Dataset.csv')
