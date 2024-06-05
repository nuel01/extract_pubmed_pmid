
import pandas as pd
from itertools import product
from Bio import Entrez
import time

count = 0
def search_pubmed(term):
    Entrez.email = 'your@email.com'
    handle = Entrez.esearch(db="pubmed", term=term, retmax=10000)  # Adjust retmax as needed
    record = Entrez.read(handle)
    return set(record['IdList'])

def compare_search_terms(term1):
    # Search for the first term
    pmids_term1 = search_pubmed(term1)
    if not pmids_term1:
        #print(f"No PMIDs found for the term: {term1}")
        return []
    else:
        return pmids_term1


def compare_search_terms2(term2):
    # Search for the second term within the PMIDs found from the first search
    pmids_term2 = search_pubmed(term2)
    if not pmids_term2:
        #print(f"No PMIDs found for the term: {term2}")
        return []
    else:
        return pmids_term2
check = False
data = pd.read_csv('all_fusion_protein_names_with_synonyms_2.tsv', sep='\t',names=['gene','syn1','syn2'], header=None, index_col=False)

#ftd_data = data[~data['gene'].str.contains(' ')]#drug = pd.read_csv('drugbank.tsv', sep='\t')
#druglist = [x for x in drug['Name']]
#data['syn1'][0] = data['syn1'][0].strip("'")
with open("all_fusion_pmid_11.tsv", 'w') as file:
    for rows in range(len(data)):
        gene = data['gene'][rows]
        print(gene)
        gene_syn1 = data['syn1'][rows].split(',')
        gene_syn2 = data['syn2'][rows].split(',')

        gene_syn1 = [s for s in gene_syn1 if ' ' not in s]
        gene_syn2 = [s for s in gene_syn2 if ' ' not in s]

        for syn1, syn2 in product(gene_syn1, gene_syn2):
            #pubmed_ids = []
            query = f'{syn1} {syn2}'
            #print(query)
            if check == False:
                if query == 'PUMB1 EAP':
                    check = True
            else:
                #print(gene)
                count += 1
                if count % 600 == 0:
                    time.sleep(50)
                res = search_pubmed(query)
                if res:
                #temp_list.extend(res)                
                #for pmid in res:                
                    for pmid in res:
                        file.write(f"{str(pmid)}\t{query}\n")
                    #print('done')
                    # temp_dict = {'PMID':pmid, 'Gene': query, 'Drug': drg}
                    # pubmed_ids.append(temp_dict)
                    


# Compare the search terms and retrieve common PMIDs
# common_pmids = compare_search_terms(term1, term2)
# if common_pmids:
#     print(f"Common PMIDs found: {common_pmids}")
# else:
#     print("No common PMIDs found.")

