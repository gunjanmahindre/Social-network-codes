# Social network codes

This has all the codes used in Social Network paper.
Working with undirected networks. D is symmetric.
Bounds for the missing entries are also calculated using observed entries.
The computed lower and upper bounds help Low-rank Matrix Completion (LMC) to estimate within the given range instead of -inf to +inf.
Missing entries in the matrix are recovered using Low-rank Matrix Completion.Results are compared for with and without bounds scenario.


## Approach
**D** >> **VC** >> delete a percentage of entries >> Recover **VC **    
Where     
**D**: complete distance matrix    
**VC**: Virtual coordinate matrix = Only a few columns are selected from the NxN distance matrix    
Percentage deletion: 20, 40, 60, 80, 90% of entries are deleted from the VC matrix    
We use Low-rank Matrix Completion integrated with bounds for missing entries to estimate missing node pair distances.    


## Performance evaluation metrics:
1. Absolute hop distance error
2. Mean error
3. Count of non exact entries in the predicted distance matrix
4. Clustering coefficient (after recovery)
5. Average node degree (after recovery)


## Data used
Undirected social networks were used:    
1. Facebook (file name: Original_Dist_nw1)
2. Collaboration (file name: Original_Dist_nw2)
3. Enron Email (file name: Original_Dist_nw3)
Distance matrices of these networks are given in this repository.
