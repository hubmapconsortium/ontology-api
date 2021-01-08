ALTER TABLE umls_codes ADD INDEX umls_codes_codeid_idx (codeid(50));
ALTER TABLE umls_codes ADD INDEX umls_codes_code_idx (code(50));
ALTER TABLE umls_codes ADD INDEX umls_codes_sab_idx (sab(20));

ALTER TABLE umls_cuis ADD UNIQUE INDEX umls_cuis_cui_idx (cui(20));

ALTER TABLE umls_defs ADD UNIQUE INDEX umls_defs_atui_idx (atui(20));
ALTER TABLE umls_defs ADD INDEX umls_defs_sab_idx (sab(20));

ALTER TABLE umls_suis ADD INDEX umls_suis_sui_idx (sui(100));
ALTER TABLE umls_suis ADD INDEX umls_suis_name_idx (name(500));

ALTER TABLE umls_tui_rel ADD INDEX umls_tui_rel_start_id_idx (start_id(100));
ALTER TABLE umls_tui_rel ADD INDEX umls_tui_rel_end_id_idx (end_id(100));
ALTER TABLE umls_tui_rel ADD INDEX umls_tui_rel_type_idx (type(100));
ALTER TABLE umls_tui_rel ADD INDEX umls_tui_rel_sab_idx (sab(20));

ALTER TABLE umls_def_rel ADD INDEX umls_def_rel_start_id_idx (start_id(100));
ALTER TABLE umls_def_rel ADD INDEX umls_def_rel_end_id_idx (end_id(100));
ALTER TABLE umls_def_rel ADD INDEX umls_def_rel_type_idx (type(100));
ALTER TABLE umls_def_rel ADD INDEX umls_def_rel_sab_idx (sab(20));

ALTER TABLE umls_cui_tuis ADD INDEX umls_cui_tuis_start_id_idx (start_id(100));
ALTER TABLE umls_cui_tuis ADD INDEX umls_cui_tuis_end_id_idx (end_id(100));
ALTER TABLE umls_cui_tuis ADD INDEX umls_cui_tuis_type_idx (type(100));
ALTER TABLE umls_cui_tuis ADD INDEX umls_cui_tuis_sab_idx (sab(20));

ALTER TABLE umls_cui_cuis ADD INDEX umls_cui_cuis_start_id_idx (start_id(100));
ALTER TABLE umls_cui_cuis ADD INDEX umls_cui_cuis_end_id_idx (end_id(100));
ALTER TABLE umls_cui_cuis ADD INDEX umls_cui_cuis_type_idx (type(100));
ALTER TABLE umls_cui_cuis ADD INDEX umls_cui_cuis_sab_idx (sab(20));

ALTER TABLE umls_cui_codes ADD INDEX umls_cui_codes_start_id_idx (start_id(100));
ALTER TABLE umls_cui_codes ADD INDEX umls_cui_codes_end_id_idx (end_id(100));

ALTER TABLE umls_code_suis ADD INDEX umls_code_suis_start_id_idx (start_id(100));
ALTER TABLE umls_code_suis ADD INDEX umls_code_suis_end_id_idx (end_id(100));
ALTER TABLE umls_code_suis ADD INDEX umls_code_suis_type_idx (type(100));
ALTER TABLE umls_code_suis ADD INDEX umls_code_suis_cui_idx (cui(100));

ALTER TABLE umls_cui_suis ADD INDEX umls_cui_suis_start_id_idx (start_id(100));
ALTER TABLE umls_cui_suis ADD INDEX umls_cui_suis_end_id_idx (end_id(100));
ALTER TABLE umls_cui_suis ADD INDEX umls_cui_suis_type_idx (type(100));
ALTER TABLE umls_cui_suis ADD INDEX umls_cui_suis_sab_idx (sab(20));


ALTER TABLE suis_updated ADD INDEX suis_updated_sui_idx (sui(100));
ALTER TABLE suis_updated ADD INDEX suis_updated_name_idx (name(500));

ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_start_id_idx (start_id(100));
ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_end_id_idx (end_id(100));
ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_type_idx (type(100));
ALTER TABLE code_suis_updated ADD INDEX code_suis_updated_cui_idx (cui(100));




