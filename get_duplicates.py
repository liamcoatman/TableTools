def get_duplicates(mylist):

    """
    Return dictionary of duplicates
    http://stackoverflow.com/questions/11236006/identify-duplicate-values-in-a-list-in-python 
    """

    from collections import defaultdict
    
    D = defaultdict(list)
    
    for i, item in enumerate(mylist):
        D[item].append(i)
    
    D = {k:v for k,v in D.items() if len(v)>1}

    return D
    
