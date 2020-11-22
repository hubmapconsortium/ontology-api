USE information_schema;

DROP DATABASE IF EXISTS knowledge_graph;

SET GLOBAL default_storage_engine = 'InnoDB';

CREATE DATABASE knowledge_graph;

USE knowledge_graph;

ALTER DATABASE knowledge_graph CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin;

    
CREATE TABLE codes (
    id INT NOT NULL AUTO_INCREMENT,
    codeid VARCHAR(2048) NOT NULL,
    sab VARCHAR(2048) NOT NULL,
    code VARCHAR(5120) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE tui_rel (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    type VARCHAR(2048) NOT NULL,
    sab VARCHAR(2048),
    PRIMARY KEY (id)
);

CREATE TABLE def_rel (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    type VARCHAR(2048) NOT NULL,
    sab VARCHAR(2048),
    PRIMARY KEY (id)
);

CREATE TABLE cui_tuis (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    type VARCHAR(2048) NOT NULL,
    sab VARCHAR(2048),
    PRIMARY KEY (id)
);

CREATE TABLE cui_cuis (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    type VARCHAR(2048) NOT NULL,
    sab VARCHAR(2048),
    PRIMARY KEY (id)
);

CREATE TABLE cui_codes (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE code_suis (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    type VARCHAR(2048) NOT NULL,
    cui VARCHAR(2048),
    PRIMARY KEY (id)
);

CREATE TABLE cui_suis (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    type VARCHAR(2048) NOT NULL,
    sab VARCHAR(2048),
    PRIMARY KEY (id)
);

CREATE TABLE cuis (
    id INT NOT NULL AUTO_INCREMENT,
    cui VARCHAR(2048) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE suis (
    id INT NOT NULL AUTO_INCREMENT,
    sui VARCHAR(2048) NOT NULL,
    name VARCHAR(5120) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE tuis (
    id INT NOT NULL AUTO_INCREMENT,
    tui VARCHAR(2048) NOT NULL,
    name VARCHAR(5120) NOT NULL,
    stn VARCHAR(2048) NOT NULL,
    def VARCHAR(5120) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE defs (
    id INT NOT NULL AUTO_INCREMENT,
    atui VARCHAR(2048) NOT NULL,
    sab VARCHAR(2048) NOT NULL,
    def VARCHAR(5120) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE edge_list (
    id INT NOT NULL AUTO_INCREMENT,
    subject VARCHAR(2048) NOT NULL,
    predicate VARCHAR(2048) NOT NULL,
    object VARCHAR(2048) NOT NULL,
    sab VARCHAR(50),
    PRIMARY KEY(id)
);

CREATE TABLE node_metadata (
    id INT NOT NULL AUTO_INCREMENT,
    node_id VARCHAR(2048) NOT NULL,
    node_label VARCHAR(2048) NOT NULL,
    node_definition VARCHAR(2048) NOT NULL,
    sab VARCHAR(50),
    PRIMARY KEY(id)
);

CREATE TABLE ontology_dbxref (
    id INT NOT NULL AUTO_INCREMENT,
    ontology_uri VARCHAR(2048) NOT NULL,
    dbxrefs VARCHAR(5120) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE relations (
    id INT NOT NULL AUTO_INCREMENT,
    relation_id VARCHAR(2048) NOT NULL,
    relation_label VARCHAR(2048) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE suis_updated (
    id INT NOT NULL AUTO_INCREMENT,
    sui VARCHAR(2048),
    name VARCHAR(5120) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE code_suis_updated (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    type VARCHAR(2048) NOT NULL,
    cui VARCHAR(2048),
    PRIMARY KEY (id)
);

CREATE TABLE new_sui_map (
    id INT NOT NULL AUTO_INCREMENT,
    codeid VARCHAR(2048) NOT NULL,
    sui VARCHAR(2048) NOT NULL,
    name VARCHAR(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE new_def_map (
    id INT NOT NULL AUTO_INCREMENT,
    cui VARCHAR(2048) NOT NULL,
    atui VARCHAR(2048) NOT NULL,
    node_definition VARCHAR(2048) NOT NULL,
    sab VARCHAR(50),
    PRIMARY KEY (id)
);

CREATE TABLE defs_updated (
    id INT NOT NULL AUTO_INCREMENT,
    atui VARCHAR(2048) NOT NULL,
    sab VARCHAR(2048) NOT NULL,
    def VARCHAR(5120) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE def_rel_updated (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    type VARCHAR(2048) NOT NULL,
    sab VARCHAR(2048),
    PRIMARY KEY (id)
);

CREATE TABLE cuis_updated (
    id INT NOT NULL AUTO_INCREMENT,
    cui VARCHAR(2048) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE cui_codes_updated (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE cui_suis_updated (
    id INT NOT NULL AUTO_INCREMENT,
    start_id VARCHAR(2048) NOT NULL,
    end_id VARCHAR(2048) NOT NULL,
    type VARCHAR(2048) NOT NULL,
    sab VARCHAR(2048),
    PRIMARY KEY (id)
);


