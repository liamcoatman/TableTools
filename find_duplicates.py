def find_duplicates(ra, dec, index):
    
    import pandas as pd
    from astropy.coordinates import SkyCoord
    from astropy import units as u
    import numpy as np 
    
    """
    Returns duplicates in list of coordinates
    RA and DEC should be in degrees 
    """

    df = pd.DataFrame(data=np.array([ra, dec]).T, columns=['RA', 'DEC'], index=index)

    catalog = SkyCoord(ra=df.RA*u.degree, dec=df.DEC*u.degree) 
    idxc, idxcatalog, d2d, d3d = catalog.search_around_sky(catalog, 5*u.arcsec)
    df_matches = pd.DataFrame(data=np.array([df.ix[idxcatalog].index.values, df.ix[idxc].index.values]).T, 
                              columns=['m1', 'm2'])

    # drop where element is matched to itself 
    df_matches = df_matches[df_matches.m1 != df_matches.m2]

    # re-order  
    mask = df_matches['m1'] < df_matches['m2']
    df_matches['first'] = df_matches['m1'].where(mask, df_matches['m2'])
    df_matches['second'] = df_matches['m2'].where(mask, df_matches['m1'])

    df_matches = df_matches.drop_duplicates(subset=['first', 'second'])
    df_matches = df_matches[['m1', 'm2']]

    # can remove m1 or m2 
    duplicates = df_matches.m2 

    # if we had multiple matches then there could be duplicates in this 
    duplicates.drop_duplicates(inplace=True)

    return duplicates.values 

if __name__ == '__main__':
    
    df = pd.read_csv('temp.dat', index_col='ID') 
    index = find_duplicates(df.RA, df.DEC, df.index)
    df.drop(index, inplace=True)
