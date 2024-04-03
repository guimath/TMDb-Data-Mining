import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def onehotencode(dataset,col):
    _df = pd.DataFrame()
    _df[col] = dataset[col].str.split('|')
    one_hot_encoded = pd.get_dummies(_df[col].apply(pd.Series).stack()).groupby(level=0).sum()
    return one_hot_encoded

def make_gexf(csv_file, gexf_file= 'actors_graph.gexf', color_by_category='genres'): # color_by_category='production_companies'
    with open(csv_file, encoding='utf-8') as f:
        df1 = pd.read_csv(f) # CSV not in utf8 ?
    df = df1[['revenue', 'cast', 'original_title', 'director', color_by_category]]
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
    OHE_cat  = onehotencode(df, color_by_category)
    cats = OHE_cat.columns
    num = np.zeros(len(cats))
    for i, cat in enumerate(cats) : 
        num[i] = OHE_cat[cat].sum()

    idx = np.argsort(num,axis=0)
    big_cat = cats[idx[-6:]]
    OHE_cat = OHE_cat[big_cat]

    COLOR = {
        big_cat[0] : {"r": 88, "g": 58, "b": 113},
        big_cat[1] : {"r": 97, "g": 132, "b": 216},
        big_cat[2] : {"r": 80, "g": 197, "b": 183},
        big_cat[3] : {"r": 156, "g": 236, "b": 91},
        big_cat[4] : {"r": 240, "g": 244, "b": 101},
        big_cat[5] : {"r": 233, "g": 40, "b": 40},
        'Other'     : {"r": 200, "g": 200, "b": 200},
    }
    
    
    # only keep actors with at least 3 movies
    distinct = []
    for i, act in enumerate(OHE_cast.columns) : 
        if OHE_cast[act].sum()>2:
            distinct.append(act)
    
    # only keep actors with at least 2 connections
    OHE_cast= OHE_cast[distinct]
    OHE_cast_n = OHE_cast.to_numpy()
    distinct = []
    for i, act in enumerate(OHE_cast.columns) : 
        link_num = np.sum([OHE_cast_n[:,i]&OHE_cast_n[:,j] for j in range(len(OHE_cast.columns)) if i != j])
        if link_num>5 :
            distinct.append(act)
    OHE_cast = OHE_cast[distinct]

    # creating nodes and compute size & color
    category, size = [], []
    for i, act in enumerate(OHE_cast.columns) : 
        graph.add_node(act)
        _d = OHE_cat.iloc[np.where(OHE_cast[act]!=0)].sum()
        if _d.max() < 1:
            cat = 'Other'
        else:
            cat = _d.idxmax()
        category.append(cat)
        size.append(df['revenue'].values[np.where(OHE_cast[act] !=0)].mean())

    # size norm between 20 and 420
    size = np.array(size)
    min_r, max_r = size.min(), size.max()
    size = (((size-min_r)/(max_r - min_r)) * 400) + 20

    # adding size & color attributes to nodes
    for i, name in enumerate(graph.nodes.keys()):
        graph.nodes[name]["viz"] = {
            'size': int(size[i]),
            'color': COLOR[category[i]]                  
        }

    # Edges computing
    OHE_cast_n = OHE_cast.to_numpy()
    for i in range(len(distinct)):
        for j in range(i+1, len(distinct)):
            combined = OHE_cast_n[:,i]& OHE_cast_n[:,j]
            weight = combined.sum()
            if weight > 0 : 
                # edge label is list of all shared movies
                label = str(movies[np.where(combined==1)].tolist()).replace('[', '').replace(']', '').replace('\'', '').replace('"', '') 
                # print(f'{distinct[i]:23s} -> {distinct[j]:23s} ({label}) {weight}')
                graph.add_edge(distinct[i], distinct[j], weight=int(3**(weight-1)), label=label)
    
    # save as gexf for gephi processing
    nx.write_gexf(graph, gexf_file)
    print(f'{gexf_file} saved')

    # save legend
    big_cat = list(big_cat)
    big_cat.append('Other')
    clrs = []
    for cat in big_cat: 
        clrs.append((COLOR[cat]['r']/255, COLOR[cat]['g']/255, COLOR[cat]['b']/255))#

    # code taken from https://stackoverflow.com/questions/4534480/get-legend-as-a-separate-picture-in-matplotlib    
    f = lambda m,c: plt.plot([],[],marker=m, color=c, ls="none")[0]

    handles = [f("s", clrs[i]) for i in range(len(big_cat))]
    legend = plt.legend(handles, big_cat, loc=3, framealpha=1, frameon=False)
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    fig.savefig('legend', dpi=1000, bbox_inches=bbox)

if __name__ == '__main__':
    make_gexf('data/TMBD Movie Dataset.csv')
