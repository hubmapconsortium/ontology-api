cd ~/umls_data/ontology_files_orig
head -1 PheKnowLator_Subclass_OWLNETS_Ontology_DbXRef_16OCT2020.txt > /home/chb69/umls_data/ontology_files/cl_dbxref.txt
grep "^http://purl.obolibrary.org/obo/CL_" PheKnowLator_Subclass_OWLNETS_Ontology_DbXRef_16OCT2020.txt >> /home/chb69/umls_data/ontology_files/cl_dbxref.txt
head -1 PheKnowLator_Subclass_OWLNETS_Ontology_DbXRef_16OCT2020.txt > /home/chb69/umls_data/ontology_files/uberon_dbxref.txt
grep "^http://purl.obolibrary.org/obo/UBERON_" PheKnowLator_Subclass_OWLNETS_Ontology_DbXRef_16OCT2020.txt >> /home/chb69/umls_data/ontology_files/uberon_dbxref.txt
head -1 PheKnowLator_Subclass_OWLNETS_edge_list_16OCT2020.txt > /home/chb69/umls_data/ontology_files/cl_edge_list.txt
grep "^http://purl.obolibrary.org/obo/CL_" PheKnowLator_Subclass_OWLNETS_edge_list_16OCT2020.txt >> /home/chb69/umls_data/ontology_files/cl_edge_list.txt
head -1 PheKnowLator_Subclass_OWLNETS_edge_list_16OCT2020.txt > /home/chb69/umls_data/ontology_files/uberon_edge_list.txt
grep "^http://purl.obolibrary.org/obo/UBERON_" PheKnowLator_Subclass_OWLNETS_edge_list_16OCT2020.txt >> /home/chb69/umls_data/ontology_files/uberon_edge_list.txt
head -1 PheKnowLator_Subclass_OWLNETS_NodeMetadata_16OCT2020.txt > /home/chb69/umls_data/ontology_files/cl_node_metadata.txt
grep "^http://purl.obolibrary.org/obo/CL_" PheKnowLator_Subclass_OWLNETS_NodeMetadata_16OCT2020.txt >> /home/chb69/umls_data/ontology_files/cl_node_metadata.txt
head -1 PheKnowLator_Subclass_OWLNETS_NodeMetadata_16OCT2020.txt > /home/chb69/umls_data/ontology_files/uberon_node_metadata.txt
grep "^http://purl.obolibrary.org/obo/UBERON_" PheKnowLator_Subclass_OWLNETS_NodeMetadata_16OCT2020.txt >> /home/chb69/umls_data/ontology_files/uberon_node_metadata.txt


