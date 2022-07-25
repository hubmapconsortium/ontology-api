# SimpleKnowledge to OWLNETS converter

Uses the input spreadsheet for the SimpleKnowledge Editor to generate a set of text files that comply with the OWLNETS format, as described in [https://github.com/callahantiff/PheKnowLator/blob/master/notebooks/OWLNETS_Example_Application.ipynb].

User guide to build the SimpleKnowledge Editor spreadsheet: [https://docs.google.com/document/d/1wjsOzJYRV2FRehX7NQI74ZKRXvH45l0QmClBBF_VypM/edit?usp=sharing]

## Assumption
The script expects a file in the application directory named SimpleKnowledgeHuBMAP.xlsx.

## Format of SimpleKnowledge Editor spreadsheet

- Column A: term
- Column B: concept code in local ontology
- Column C: definition
- Column D: pipe-delimited list of synonyms
- Column E: pipe-delimited list of references to other ontologies. Format of each list element is *<ontology SAB>*:*<concept code>*

Columns after F describe relationships. Column F corresponds to *isa*; the column headers for columns after F contain the relationship URI.

Each cell in a relationship column contains a comma-delimited list of object concepts that relate.

The script loops through each relationship cell in a row and creates a set of subject-predicate-object relationships between the concepts in the cell and the subject concept in column B.