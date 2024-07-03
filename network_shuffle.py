import argparse
import networkx as nx
import os, sys
import warnings
import pandas as pd

def shuffle_network(G, n_swaps):
    """
    Shuffle the edges of a network using the double_edge_swap function from networkx
    
    Args:
        G (networkx.Graph): networkx graph object of network
        n_swaps (int): number of edge swaps to perform
        
    Returns:
        networkx.Graph: networkx graph object of shuffled network
    """
    edge_len=len(G.edges())
    G_shuff = G.copy()
    try:
        nx.double_edge_swap(G_shuff, nswap=edge_len*n_swaps, max_tries=edge_len*n_swaps*10, seed=None)
    except nx.NetworkXAlgorithmError:
        warning_string = 'Maximum number of swap attempts ('+str(edge_len*10)+') exceeded before desired swaps achieved ('+str(edge_len*n_swaps)+') for file' + G.graph['file'] +'.'
        warnings.warn(warning_string)
    except nx.NetworkXError:
        print("NETWORK ERROR:", G.graph['file'])
    shared_edges = len(set(G.edges()).intersection(set(G_shuff.edges())))
    try:
        print('Edge Similarity:', shared_edges/float(edge_len), G.graph['file'])
    except KeyError:
        print('Edge Similarity:', shared_edges/float(edge_len))

    return G_shuff

def write_shuffled_network(G, datafile, outpath):
    if outpath[-1] != "/":
        outpath += "/"
    outfile = outpath + os.path.split(datafile)[1].split(".txt")[0] + "_shuffled.txt"
    write_networkx_to_file(G, outfilepath=outfile)
    
def load_shuffled_network(datafile, outpath):
    outfile = outpath + os.path.split(datafile)[1].split(".txt")[0] + "_shuffled.txt"
    G = load_edgelist_to_networkx(outfile)
    return G

def load_edgelist_to_networkx(datafile, id_type="Entrez", testmode=False, delimiter="\t", node_cols=[0,1],
                            keep_attributes=False, verbose=False):
    """ Load an edge list file into a networkx graph
    
    Args:
        datafile (str): path to edge list file
        id_type (str): type of node ID to use for graph. If Entrez, treat as integers, otherwise treat as strings
        testmode (bool): only load first 1000 rows of file
        delimiter (str): delimiter for edge list file
        node_cols (list): list of column numbers for source and target nodes
        keep_attributes (bool): keep attributes for edges
        verbose (bool): print out number of nodes and edges in network
    
    Returns:
        networkx.Graph: networkx graph object of network
    """
    # Assumes node columns are columns 0,1
    # Do I really want it to return a graph when there is an error?
    valid_id_types = ["Entrez", "Symbol"]
    assert id_type in valid_id_types, "id_type must be one of:" + ", ".join(valid_id_types)
    if testmode:
        net_df = pd.read_csv(datafile, sep=delimiter, index_col=None, nrows=1000)
    else:    
        net_df = pd.read_csv(datafile, sep=delimiter, index_col=None)
    #has_edge_attributes = True if len(net_df.columns) > 2 else None
    source_col, target_col = [net_df.columns[i] for i in node_cols]
    if id_type == "Entrez":
        net_df[source_col] = net_df[source_col].astype(int)
        net_df[target_col] = net_df[target_col].astype(int)
    try:
        if keep_attributes:
            G = nx.from_pandas_edgelist(net_df, source=source_col, target=target_col, edge_attr=keep_attributes)
        else:
            G = nx.from_pandas_edgelist(net_df, source=source_col, target=target_col, edge_attr=None)
    except KeyError: 
        print("FILE LOAD ERROR:", datafile)
        G = nx.Graph()
    except pd.errors.EmptyDataError:
        print("EMPTY DATA ERROR:", datafile)
        G = nx.Graph()
    G.graph['file'] = datafile
    if verbose:
        print('Network File Loaded:', datafile)
        print("# Nodes:", len(G.nodes))
        print("# Edges:", len(G.edges))
    return G


def write_networkx_to_file(G, outfilepath, source="Node_A", target="Node_B"):
    """ Write a networkx graph to an edge list file
    
    Args:
        G (networkx.Graph): networkx graph object of network
        outfilepath (str): path to output file
        timer (Timer): Timer object for timing operations
        source (str): name of source node column
        target (str): name of target node column
    
    Returns:
        None
    """
    assert source != target, "Source and target columns must be different"
    net_df = nx.to_pandas_edgelist(G, source=source, target=target)
    net_df.to_csv(outfilepath, index=False, sep="\t")
    return

def parse_arguments(args):
    parser = argparse.ArgumentParser(description='Take an edgelist file and perform network randomization using double edge swaps')
    parser.add_argument('datafile', metavar='d', help='String with the full file path for the edgelist file')
    parser.add_argument('-o', metavar='outpath', required=True, help='String with the full file path to store the shuffled network. Include suffix for repeated shuffles of the same network')
    parser.add_argument('--nSwaps', default='1', type=float, help='Number of edge swaps to perform')
    parser.add_argument('--testMode', default='1', type=int, help='Only load first 1000 rows of network file')
    parser.add_argument('--verbose', default='0', type=int)
    parser.add_argument('--node_cols', default=[0,1], type=int, nargs=2, help='List of column numbers for source and target nodes')
    args = parser.parse_args(args)
    args.testMode = bool(args.testMode)
    args.verbose = bool(args.verbose)
    return args


if __name__=="__main__":
    args = parse_arguments(sys.argv[1:])
    
    #print(args.A, args.B)
    if args.verbose:
        print(args)
        print("Analysis of", args.datafile)  
    G = load_edgelist_to_networkx(args.datafile, testmode=args.testMode, node_cols=args.node_cols, verbose=args.verbose)
    if args.verbose:
        print("Data Loaded")
    if len(G.edges) > 0:
        G_shuff = shuffle_network(G, args.nSwaps)
        if args.verbose:
            print("Network Shuffled")
    # get output file name from the datafile, then append to outpath
        write_shuffled_network(G_shuff, args.datafile, args.o)
    else:
        print("NO EDGES:", args.datafile)

    
