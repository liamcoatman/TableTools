import pyfits
import numpy as np
import math
import match_lists

"""
I did not write these
Sergei maybe?
"""

def angsep(ra1deg,dec1deg,ra2deg,dec2deg):
    """ Determine separation in degrees between two celestial objects 
        arguments are RA and Dec in decimal degrees. 
    """
    ra1rad=ra1deg*np.pi/180.0
    dec1rad=dec1deg*np.pi/180.0
    ra2rad=ra2deg*np.pi/180.0
    dec2rad=dec2deg*np.pi/180.0
    
    # calculate scalar product for determination
    # of angular separation
    
    x=np.cos(ra1rad)*np.cos(dec1rad)*np.cos(ra2rad)*np.cos(dec2rad)
    y=np.sin(ra1rad)*np.cos(dec1rad)*np.sin(ra2rad)*np.cos(dec2rad)
    z=np.sin(dec1rad)*np.sin(dec2rad)
    
    rad=np.arccos(x+y+z) # Sometimes gives warnings when coords match
    
    # use Pythargoras approximation if rad < 1 arcsec
    sep = np.choose( rad<0.000004848 , (
        np.sqrt((np.cos(dec1rad)*(ra1rad-ra2rad))**2+(dec1rad-dec2rad)**2),rad))
        
    # Angular separation
    sep=sep*180/np.pi

    return sep

def matchsorted(ra,dec,ra1,dec1,tol):
    """ Find closest ra,dec within tol to a target in an ra-sorted list of ra,dec.
        Arguments:
          ra - Right Ascension decimal degrees (numpy sorted in ascending order)
          dec - Declination decimal degrees (numpy array)
          ra1 - RA to match (scalar, decimal degrees)
          ra1 - Dec to match (scalar, decimal degrees)
          tol - Matching tolerance in decimal degrees. 
        Returns:
          ibest - index of the best match within tol; -1 if no match within tol
          sep - separation (defaults to tol if no match within tol)
    """
    i1 = np.searchsorted(ra,ra1-tol)-1
    i2 = np.searchsorted(ra,ra1+tol)+1
    if i1 < 0:
        i1 = 0
    sep = angsep(ra[i1:i2],dec[i1:i2],ra1,dec1)
    # print "tolerance ",tol
    indices=np.argsort(sep)
    # print sep
    if sep[indices[0]] > tol:
        return -1, tol
    ibest = indices[0] + i1
    return ibest, sep[indices[0]]

def matchpos(ra1,dec1,ra2,dec2,tol):
    """ Match two sets of ra,dec within a tolerance.
        Longer catalog should go first
        Arguments:
          ra1 - Right Ascension decimal degrees (numpy array)
          dec1 - Declination decimal degrees (numpy array)
          ra2 - Right Ascension decimal degrees (numpy array)
          dec2 - Declination decimal degrees (numpy array)
          tol - Matching tolerance in decimal degrees. 
        Returns:
          ibest - indices of the best matches within tol; -1 if no match within tol
          sep - separations (defaults to tol if no match within tol)
    """
    indices = np.argsort(ra1)
    rasorted = ra1[indices]
    decsorted = dec1[indices]
    ibest = []
    sep = []
    for i in range(len(ra2)):
        j,s = matchsorted(rasorted,decsorted,ra2[i],dec2[i],tol)
        if j < 0:
            ibest += [j]
        else:
            ibest += [indices[j]]
        sep += [s]
    return np.array(ibest),np.array(sep)
