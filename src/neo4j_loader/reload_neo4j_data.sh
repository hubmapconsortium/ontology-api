cd /var/lib/neo4j
sudo neo4j stop
sudo rm -rf data/databases/*
sudo rm -rf data/transactions/*
sudo rm import/*
sudo cp ~/umls_data/export/* import
sudo cp ~/umls_data/jonathan_revised_files/NDC* import
sudo chown neo4j:adm import/*
sudo neo4j-admin import --nodes=Semantic="import/TUIs.csv" --nodes=Concept="import/CUIs.csv" --nodes=Code="import/CODEs.csv" --nodes=Term="import/SUIs.csv" --nodes=Definition="import/DEFs.csv" --nodes=NDC="import/NDCs.csv" --relationships=ISA_STY="import/TUIrel.csv" --relationships=STY="import/CUI-TUIs.csv" --relationships="import/CUI-CUIs.csv" --relationships=CODE="import/CUI-CODEs.csv" --relationships="import/CODE-SUIs.csv" --relationships=PREF_TERM="import/CUI-SUIs.csv" --relationships=DEF="import/DEFrel.csv" --relationships=NDC="import/NDCrel.csv" --skip-bad-relationships --skip-duplicate-nodes
sudo neo4j start

