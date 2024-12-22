---- postgresql database dump ---- dumped
FROM
    database version 17.2 (
        debian 17.2 -1.pgdg120 + 1
    ) -- dumped BY pg_dump version 17.2 (
        debian 17.2 -1.pgdg120 + 1
    ) SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings =
    ON;
SELECT
    pg_catalog.set_config(
        'search_path',
        '',
        FALSE
    );
SET check_function_bodies = FALSE;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
SET default_tablespace = '';
SET default_table_access_method = HEAP;
CREATE database fetch_rewards;---- NAME: brands;
TYPE: TABLE;
schema: PUBLIC;
owner:--- CREATE TABLE PUBLIC.brands (brand_id CHARACTER VARYING(24) NOT NULL, ref CHARACTER VARYING(50), barcode CHARACTER VARYING(50), brand_code CHARACTER VARYING(50), category CHARACTER VARYING(50), category_code CHARACTER VARYING(50), top_brand BOOLEAN, NAME CHARACTER VARYING(255));---- NAME: cpg;
TYPE: TABLE;
schema: PUBLIC;
owner:--- CREATE TABLE PUBLIC.cpg (cpg_id CHARACTER VARYING(24) NOT NULL, ref CHARACTER VARYING(50));---- NAME: receipt_items;
TYPE: TABLE;
schema: PUBLIC;
owner:--- CREATE TABLE PUBLIC.receipt_items (
        receipt_id CHARACTER VARYING,
        barcode CHARACTER VARYING,
        description CHARACTER VARYING,
        final_price numeric,
        needs_fetch_review BOOLEAN,
        partner_item_id BOOLEAN,
        prevent_target_gap_points BOOLEAN,
        quantity_purchased INTEGER,
        user_flagged_barcode CHARACTER VARYING,
        user_flagged_new_item BOOLEAN,
        user_flagged_price numeric,
        user_flagged_quantity INTEGER
    );---- NAME: receipt_items_v2;
TYPE: TABLE;
schema: PUBLIC;
owner:--- CREATE TABLE PUBLIC.receipt_items_v2 (
        item_id INTEGER,
        receipt_id CHARACTER VARYING,
        barcode CHARACTER VARYING,
        description CHARACTER VARYING,
        final_price numeric,
        needs_fetch_review BOOLEAN,
        partner_item_id BOOLEAN,
        prevent_target_gap_points BOOLEAN,
        quantity_purchased INTEGER,
        user_flagged_barcode CHARACTER VARYING,
        user_flagged_new_item BOOLEAN,
        user_flagged_price numeric,
        user_flagged_quantity INTEGER
    );---- NAME: receipts;
TYPE: TABLE;
schema: PUBLIC;
owner:--- CREATE TABLE PUBLIC.receipts (
        receipt_id CHARACTER VARYING NOT NULL,
        user_id CHARACTER VARYING DEFAULT 'unknown_user' :: CHARACTER VARYING,
        bonus_points_earned INTEGER DEFAULT 0,
        bonus_points_reason CHARACTER VARYING DEFAULT '' :: CHARACTER VARYING,
        create_date TIMESTAMP without TIME ZONE,
        date_scanned TIMESTAMP without TIME ZONE,
        finished_date TIMESTAMP without TIME ZONE,
        modify_date TIMESTAMP without TIME ZONE,
        points_awarded_date TIMESTAMP without TIME ZONE,
        points_earned numeric DEFAULT 0.0,
        purchase_date TIMESTAMP without TIME ZONE,
        purchase_item_count INTEGER DEFAULT 0,
        reward_receipt_status CHARACTER VARYING DEFAULT 'UNKNOWN' :: CHARACTER VARYING,
        total_spent numeric DEFAULT 0.0
    );---- NAME: users;
TYPE: TABLE;
schema: PUBLIC;
owner:--- CREATE TABLE PUBLIC.users (
        user_id CHARACTER VARYING,
        active BOOLEAN,
        created_date TIMESTAMP without TIME ZONE,
        last_login TIMESTAMP without TIME ZONE,
        role CHARACTER VARYING,
        sign_up_source CHARACTER VARYING,
        state CHARACTER VARYING
    );---- NAME: brands brands_pkey;
TYPE: constraint;
schema: PUBLIC;
owner:---
ALTER TABLE
    ONLY PUBLIC.brands
ADD
    constraint brands_pkey primary key (brand_id);---- NAME: cpg cpg_pkey;
TYPE: constraint;
schema: PUBLIC;
owner:---
ALTER TABLE
    ONLY PUBLIC.cpg
ADD
    constraint cpg_pkey primary key (cpg_id);---- NAME: receipts receipts_pkey;
TYPE: constraint;
schema: PUBLIC;
owner:---
ALTER TABLE
    ONLY PUBLIC.receipts
ADD
    constraint receipts_pkey primary key (receipt_id);---- postgresql database dump complete --
