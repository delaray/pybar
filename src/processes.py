#********************************************************************
# MULTIPROCESSING MODULE
#
#********************************************************************

# Python multithreading for whatever reason seems to require that the
# workers be in a different module.

import src.database as db
import src.clustering as cs

#------------------------------------------------------------------------------

def neighbor_worker (topic, tables, procnum, return_dict):
    results = db.find_wiki_in_neighbors (topic, tables)
    return_dict[procnum] = results

#------------------------------------------------------------------------------

# This used the dsitance matrix

def pdm_worker (l1, l2, procnum, return_dict):
    conn = ensure_connection()
    m = cs.generate_distance_matrix (l1, l2, conn)
    return_dict[procnum] = m

#------------------------------------------------------------------------------
# End of File
#------------------------------------------------------------------------------
