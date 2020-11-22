ALTER TABLE codes ADD INDEX codes_codeid_idx (codeid(50));
ALTER TABLE codes ADD INDEX codes_code_idx (code(50));
ALTER TABLE codes ADD INDEX codes_sab_idx (sab(20));

ALTER TABLE cuis ADD UNIQUE INDEX cuis_cui_idx (cui(20));

ALTER TABLE defs ADD UNIQUE INDEX defs_atui_idx (atui(20));
ALTER TABLE defs ADD INDEX defs_sab_idx (sab(20));

ALTER TABLE suis ADD INDEX suis_sui_idx (sui(100));
ALTER TABLE suis ADD INDEX suis_name_idx (name(500));

ALTER TABLE edge_list ADD INDEX edge_list_subject_idx (subject(50));
ALTER TABLE edge_list ADD INDEX edge_list_predicate_idx (predicate(100));
ALTER TABLE edge_list ADD INDEX edge_list_object_idx (object(100));
ALTER TABLE edge_list ADD INDEX edge_list_sab_idx (sab(50));

ALTER TABLE ontology_dbxref ADD INDEX ontology_dbxref_ontology_uri_idx (ontology_uri(50));
ALTER TABLE ontology_dbxref ADD FULLTEXT INDEX ontology_dbxref_dbxrefs_idx (dbxrefs(700));

ALTER TABLE node_metadata ADD INDEX node_metadata_node_id_idx (node_id(50));
ALTER TABLE node_metadata ADD INDEX node_metadata_node_label_idx (node_label(500));
ALTER TABLE node_metadata ADD INDEX node_metadata_node_definition_idx (node_definition(500));
ALTER TABLE node_metadata ADD INDEX node_metadata_sab_idx (sab(50));

ALTER TABLE relations ADD INDEX relations_relation_id_idx (relation_id(100));
ALTER TABLE relations ADD INDEX relations_relation_label_idx (relation_label(50));

ALTER TABLE tui_rel ADD INDEX tui_rel_start_id_idx (start_id(100));
ALTER TABLE tui_rel ADD INDEX tui_rel_end_id_idx (end_id(100));
ALTER TABLE tui_rel ADD INDEX tui_rel_type_idx (type(100));
ALTER TABLE tui_rel ADD INDEX tui_rel_sab_idx (sab(20));

ALTER TABLE def_rel ADD INDEX def_rel_start_id_idx (start_id(100));
ALTER TABLE def_rel ADD INDEX def_rel_end_id_idx (end_id(100));
ALTER TABLE def_rel ADD INDEX def_rel_type_idx (type(100));
ALTER TABLE def_rel ADD INDEX def_rel_sab_idx (sab(20));

ALTER TABLE cui_tuis ADD INDEX cui_tuis_start_id_idx (start_id(100));
ALTER TABLE cui_tuis ADD INDEX cui_tuis_end_id_idx (end_id(100));
ALTER TABLE cui_tuis ADD INDEX cui_tuis_type_idx (type(100));
ALTER TABLE cui_tuis ADD INDEX cui_tuis_sab_idx (sab(20));

ALTER TABLE cui_cuis ADD INDEX cui_cuis_start_id_idx (start_id(100));
ALTER TABLE cui_cuis ADD INDEX cui_cuis_end_id_idx (end_id(100));
ALTER TABLE cui_cuis ADD INDEX cui_cuis_type_idx (type(100));
ALTER TABLE cui_cuis ADD INDEX cui_cuis_sab_idx (sab(20));

ALTER TABLE cui_codes ADD INDEX cui_codes_start_id_idx (start_id(100));
ALTER TABLE cui_codes ADD INDEX cui_codes_end_id_idx (end_id(100));

ALTER TABLE code_suis ADD INDEX code_suis_start_id_idx (start_id(100));
ALTER TABLE code_suis ADD INDEX code_suis_end_id_idx (end_id(100));
ALTER TABLE code_suis ADD INDEX code_suis_type_idx (type(100));
ALTER TABLE code_suis ADD INDEX code_suis_cui_idx (cui(100));

ALTER TABLE cui_suis ADD INDEX cui_suis_start_id_idx (start_id(100));
ALTER TABLE cui_suis ADD INDEX cui_suis_end_id_idx (end_id(100));
ALTER TABLE cui_suis ADD INDEX cui_suis_type_idx (type(100));
ALTER TABLE cui_suis ADD INDEX cui_suis_sab_idx (sab(20));

ALTER TABLE dbxrefs ADD INDEX dbxrefs_ontology_uri_idx(ontology_uri(50));
ALTER TABLE dbxrefs ADD INDEX dbxrefs_xref_idx(xref(150));

ALTER TABLE suis_updated ADD INDEX suis_updated_sui_idx (sui(100));
ALTER TABLE suis_updated ADD INDEX suis_updated_name_idx (name(500));

ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_start_id_idx (start_id(100));
ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_end_id_idx (end_id(100));
ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_type_idx (type(100));
ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_cui_idx (cui(100));




