Perform network randomization from an edgelist file using `nx.double_edge_swap()`. For information on the edge swap algorithm see [NetworkX](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.swap.double_edge_swap.html) documentation. Code derived from [Network_Evaluation_Tools](https://github.com/sarah-n-wright/Network_Evaluation_Tools/tree/master/neteval).

## Requires:
* `networkx`
* `pandas`

## Example Usage:
To test that network shuffling is working use `--testMode 1` to utilize only the first 1000 edges of the network
```
  python network_shuffle.py -o <output directory> --nSwaps 10 --testMode 1 --verbose 1 --node_cols 0 1 ./test_data/dip_net.txt
```

To perform a single network shuffling
```
  python network_shuffle.py -o <output directory> --nSwaps 10 --testMode 0 --verbose 1 --node_cols 0 1 ./test_data/dip_net.txt
```
To create multiple randomized networks from the same source
```
for i in {0..10}; do
  python network_shuffle.py -o <output directory>/shuff${i}_ --nSwaps 10 --testMode 0 --verbose 1 --node_cols 0 1 ./test_data/dip_net.txt
done
```
Example verbose output, where *edge similarity* is measured as the fraction of edges in the shuffled network that were edges in the original network. 
```
Namespace(datafile='./test_data/dip_net.txt', o='./test_data/shuff10_', nSwaps=10.0, testMode=False, verbose=True, node_cols=[0, 1])
Analysis of ./test_data/dip_net.txt
Network File Loaded: ./test_data/dip_net.txt
# Nodes: 3202
# Edges: 11518
Data Loaded
Edge Similarity: 0.029258551831915263 ./test_data/dip_net.txt
Network Shuffled
```
Note: this does not check the similarity between repeated runs of network shuffling for the same network.
