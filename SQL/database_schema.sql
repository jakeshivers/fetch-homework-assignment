--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Debian 17.2-1.pgdg120+1)
-- Dumped by pg_dump version 17.2 (Debian 17.2-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: brands; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.brands (
    brand_id character varying(24) NOT NULL,
    ref character varying(50),
    barcode character varying(50),
    brand_code character varying(50),
    category character varying(50),
    category_code character varying(50),
    top_brand boolean,
    name character varying(255)
);


--
-- Name: cpg; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cpg (
    cpg_id character varying(24) NOT NULL,
    ref character varying(50)
);


--
-- Name: receipt_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.receipt_items (
    receipt_id character varying,
    barcode character varying,
    description character varying,
    final_price numeric,
    needs_fetch_review boolean,
    partner_item_id boolean,
    prevent_target_gap_points boolean,
    quantity_purchased integer,
    user_flagged_barcode character varying,
    user_flagged_new_item boolean,
    user_flagged_price numeric,
    user_flagged_quantity integer
);


--
-- Name: receipt_items_v2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.receipt_items_v2 (
    item_id integer,
    receipt_id character varying,
    barcode character varying,
    description character varying,
    final_price numeric,
    needs_fetch_review boolean,
    partner_item_id boolean,
    prevent_target_gap_points boolean,
    quantity_purchased integer,
    user_flagged_barcode character varying,
    user_flagged_new_item boolean,
    user_flagged_price numeric,
    user_flagged_quantity integer
);


--
-- Name: receipts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.receipts (
    receipt_id character varying NOT NULL,
    user_id character varying DEFAULT 'unknown_user'::character varying,
    bonus_points_earned integer DEFAULT 0,
    bonus_points_reason character varying DEFAULT ''::character varying,
    create_date timestamp without time zone,
    date_scanned timestamp without time zone,
    finished_date timestamp without time zone,
    modify_date timestamp without time zone,
    points_awarded_date timestamp without time zone,
    points_earned numeric DEFAULT 0.0,
    purchase_date timestamp without time zone,
    purchase_item_count integer DEFAULT 0,
    reward_receipt_status character varying DEFAULT 'UNKNOWN'::character varying,
    total_spent numeric DEFAULT 0.0
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id character varying,
    active boolean,
    created_date timestamp without time zone,
    last_login timestamp without time zone,
    role character varying,
    sign_up_source character varying,
    state character varying
);


--
-- Name: brands brands_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_pkey PRIMARY KEY (brand_id);


--
-- Name: cpg cpg_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cpg
    ADD CONSTRAINT cpg_pkey PRIMARY KEY (cpg_id);


--
-- Name: receipts receipts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.receipts
    ADD CONSTRAINT receipts_pkey PRIMARY KEY (receipt_id);


--
-- PostgreSQL database dump complete
--

