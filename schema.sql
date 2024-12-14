--
-- PostgreSQL database dump
--

-- Dumped from database version 15.9 (Homebrew)
-- Dumped by pg_dump version 15.9 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: ad_size_format; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ad_size_format (
    size_id integer NOT NULL,
    format_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ad_size_format OWNER TO hoangtv;

--
-- Name: ads; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads (
    ads_id integer NOT NULL,
    ads_group_id integer NOT NULL,
    ads_status_id integer NOT NULL,
    ten_tin_quang_cao character varying(100),
    url_dich text,
    tong_chi_phi numeric(15,2),
    luot_xem integer DEFAULT 0,
    luot_nhan integer DEFAULT 0,
    ctr numeric(5,2) DEFAULT 0,
    cpc numeric(10,2) DEFAULT 0,
    cpm numeric(10,2) DEFAULT 0,
    so_luong_mua_hang integer DEFAULT 0,
    conversion_rate numeric(5,2) DEFAULT 0,
    cps numeric(10,2) DEFAULT 0,
    video_watches_at_3s integer DEFAULT 0,
    video_watches_at_25 integer DEFAULT 0,
    video_watches_at_50 integer DEFAULT 0,
    video_watches_at_75 integer DEFAULT 0,
    video_watches_at_100 integer DEFAULT 0,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads OWNER TO hoangtv;

--
-- Name: ads_ads_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_ads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_ads_id_seq OWNER TO hoangtv;

--
-- Name: ads_ads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_ads_id_seq OWNED BY public.ads.ads_id;


--
-- Name: ads_display; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_display (
    ads_id integer NOT NULL,
    format_id integer,
    dang_tai_tep_anh bytea,
    tieu_de text,
    noi_dung text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_display OWNER TO hoangtv;

--
-- Name: ads_display_ads_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_display_ads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_display_ads_id_seq OWNER TO hoangtv;

--
-- Name: ads_display_ads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_display_ads_id_seq OWNED BY public.ads_display.ads_id;


--
-- Name: ads_ecom; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_ecom (
    ads_id integer NOT NULL,
    format_id integer NOT NULL,
    anh_banner_chan_trang bytea,
    video_banner bytea,
    anh_thumbnail bytea,
    su_dung_mau_banner_co_san boolean DEFAULT false,
    ten_san_pham character varying(100),
    hien_thi_gia_khuyen_mai boolean DEFAULT false,
    hien_thi_freeship_sp boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_ecom OWNER TO hoangtv;

--
-- Name: ads_ecom_ads_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_ecom_ads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_ecom_ads_id_seq OWNER TO hoangtv;

--
-- Name: ads_ecom_ads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_ecom_ads_id_seq OWNED BY public.ads_ecom.ads_id;


--
-- Name: ads_format; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_format (
    format_id integer NOT NULL,
    campaign_type_id integer NOT NULL,
    format_name character varying(100),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_format OWNER TO hoangtv;

--
-- Name: ads_format_format_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_format_format_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_format_format_id_seq OWNER TO hoangtv;

--
-- Name: ads_format_format_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_format_format_id_seq OWNED BY public.ads_format.format_id;


--
-- Name: ads_group; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_group (
    ads_group_id integer NOT NULL,
    camp_id integer NOT NULL,
    ads_group_status_id integer NOT NULL,
    ten_nhom character varying(100),
    nham_chon_all_san_pham boolean DEFAULT false,
    nham_chon_doi_tuong boolean DEFAULT false,
    nham_chon_dia_ly character varying(100),
    gioi_tinh_khong_xac_dinh boolean DEFAULT false,
    gioi_tinh_nam boolean DEFAULT false,
    gioi_tinh_nu boolean DEFAULT false,
    tuoi_less_than_18 boolean DEFAULT false,
    tuoi_from_18_to_24 boolean DEFAULT false,
    tuoi_from_25_to_34 boolean DEFAULT false,
    tuoi_from_35_to_50 boolean DEFAULT false,
    tuoi_more_than_50 boolean DEFAULT false,
    tong_chi_phi numeric(15,2) DEFAULT 0,
    luot_xem integer DEFAULT 0,
    luot_nhan integer DEFAULT 0,
    ctr numeric(5,2) DEFAULT 0,
    cpc numeric(10,2) DEFAULT 0,
    cpm numeric(10,2) DEFAULT 0,
    so_luong_mua_hang integer DEFAULT 0,
    conversion_rate numeric(5,2) DEFAULT 0,
    cps numeric(10,2) DEFAULT 0,
    videoview3s integer DEFAULT 0,
    videowatchesat25 integer DEFAULT 0,
    videowatchesat50 integer DEFAULT 0,
    videowatchesat75 integer DEFAULT 0,
    videowatchesat100 integer DEFAULT 0,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_group OWNER TO hoangtv;

--
-- Name: ads_group_ads_group_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_group_ads_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_group_ads_group_id_seq OWNER TO hoangtv;

--
-- Name: ads_group_ads_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_group_ads_group_id_seq OWNED BY public.ads_group.ads_group_id;


--
-- Name: ads_group_product_group; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_group_product_group (
    id integer NOT NULL,
    ads_group_id integer NOT NULL,
    product_group_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_group_product_group OWNER TO hoangtv;

--
-- Name: ads_group_product_group_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_group_product_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_group_product_group_id_seq OWNER TO hoangtv;

--
-- Name: ads_group_product_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_group_product_group_id_seq OWNED BY public.ads_group_product_group.id;


--
-- Name: ads_group_status; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_group_status (
    ads_group_status_id integer NOT NULL,
    ten_trang_thai character varying(50),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_group_status OWNER TO hoangtv;

--
-- Name: ads_group_status_ads_group_status_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_group_status_ads_group_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_group_status_ads_group_status_id_seq OWNER TO hoangtv;

--
-- Name: ads_group_status_ads_group_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_group_status_ads_group_status_id_seq OWNED BY public.ads_group_status.ads_group_status_id;


--
-- Name: ads_group_target_audience; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_group_target_audience (
    id integer NOT NULL,
    ads_group_id integer NOT NULL,
    ta_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_group_target_audience OWNER TO hoangtv;

--
-- Name: ads_group_target_audience_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_group_target_audience_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_group_target_audience_id_seq OWNER TO hoangtv;

--
-- Name: ads_group_target_audience_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_group_target_audience_id_seq OWNED BY public.ads_group_target_audience.id;


--
-- Name: ads_group_website; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_group_website (
    id integer NOT NULL,
    ads_group_id integer NOT NULL,
    website_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_group_website OWNER TO hoangtv;

--
-- Name: ads_group_website_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_group_website_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_group_website_id_seq OWNER TO hoangtv;

--
-- Name: ads_group_website_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_group_website_id_seq OWNED BY public.ads_group_website.id;


--
-- Name: ads_link_format; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_link_format (
    ads_id integer NOT NULL,
    format_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_link_format OWNER TO hoangtv;

--
-- Name: ads_native; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_native (
    ads_id integer NOT NULL,
    format_id integer,
    video bytea,
    anh_thumbnail bytea,
    logo bytea,
    anh_quang_cao bytea,
    ten_brand character varying(255),
    tieu_de text,
    noi_dung text,
    nut_cta boolean,
    noi_dung_cta text,
    url_cta text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_native OWNER TO hoangtv;

--
-- Name: ads_native_ads_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_native_ads_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_native_ads_id_seq OWNER TO hoangtv;

--
-- Name: ads_native_ads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_native_ads_id_seq OWNED BY public.ads_native.ads_id;


--
-- Name: ads_zone; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_zone (
    zone_id integer NOT NULL,
    website_id integer NOT NULL,
    ten_vung_quang_cao character varying(100),
    size_id integer NOT NULL,
    ma_nhung_vung_quang_cao text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_zone OWNER TO hoangtv;

--
-- Name: ads_zone_format; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_zone_format (
    zone_id integer NOT NULL,
    format_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_zone_format OWNER TO hoangtv;

--
-- Name: ads_zone_size; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.ads_zone_size (
    size_id integer NOT NULL,
    ten_kich_thuoc character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.ads_zone_size OWNER TO hoangtv;

--
-- Name: ads_zone_size_size_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_zone_size_size_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_zone_size_size_id_seq OWNER TO hoangtv;

--
-- Name: ads_zone_size_size_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_zone_size_size_id_seq OWNED BY public.ads_zone_size.size_id;


--
-- Name: ads_zone_zone_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.ads_zone_zone_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ads_zone_zone_id_seq OWNER TO hoangtv;

--
-- Name: ads_zone_zone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.ads_zone_zone_id_seq OWNED BY public.ads_zone.zone_id;


--
-- Name: behaviour; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.behaviour (
    behav_id integer NOT NULL,
    ten_hanh_vi text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.behaviour OWNER TO hoangtv;

--
-- Name: behaviour_behav_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.behaviour_behav_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.behaviour_behav_id_seq OWNER TO hoangtv;

--
-- Name: behaviour_behav_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.behaviour_behav_id_seq OWNED BY public.behaviour.behav_id;


--
-- Name: campaign; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.campaign (
    camp_id integer NOT NULL,
    customer_id integer,
    camp_type_id integer,
    campstatus_id integer,
    source_id integer,
    ten_chien_dich character varying(100),
    ngan_sach_ngay numeric(15,2) DEFAULT 0,
    tong_chi_phi numeric(15,2) DEFAULT 0,
    luot_xem integer DEFAULT 0,
    luot_nhan integer DEFAULT 0,
    ctr numeric(5,2) DEFAULT 0,
    cpc numeric(10,2) DEFAULT 0,
    cpm numeric(10,2) DEFAULT 0,
    so_luong_mua_hang integer DEFAULT 0,
    conversion_rate numeric(5,2) DEFAULT 0,
    cps numeric(10,2) DEFAULT 0,
    videoview3s integer DEFAULT 0,
    videowatchesat25 integer DEFAULT 0,
    videowatchesat50 integer DEFAULT 0,
    videowatchesat75 integer DEFAULT 0,
    videowatchesat100 integer DEFAULT 0,
    ngay_bat_dau timestamp with time zone,
    ngay_ket_thuc timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.campaign OWNER TO hoangtv;

--
-- Name: campaign_camp_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.campaign_camp_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaign_camp_id_seq OWNER TO hoangtv;

--
-- Name: campaign_camp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.campaign_camp_id_seq OWNED BY public.campaign.camp_id;


--
-- Name: campaign_status; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.campaign_status (
    campstatus_id integer NOT NULL,
    ten_trang_thai character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.campaign_status OWNER TO hoangtv;

--
-- Name: campaign_status_campstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.campaign_status_campstatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaign_status_campstatus_id_seq OWNER TO hoangtv;

--
-- Name: campaign_status_campstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.campaign_status_campstatus_id_seq OWNED BY public.campaign_status.campstatus_id;


--
-- Name: campaign_type; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.campaign_type (
    camp_type_id integer NOT NULL,
    ten_loai_chien_dich character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.campaign_type OWNER TO hoangtv;

--
-- Name: campaign_type_camp_type_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.campaign_type_camp_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaign_type_camp_type_id_seq OWNER TO hoangtv;

--
-- Name: campaign_type_camp_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.campaign_type_camp_type_id_seq OWNED BY public.campaign_type.camp_type_id;


--
-- Name: city; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.city (
    city_id integer NOT NULL,
    ten_thanh_pho character varying(100) NOT NULL,
    country_id integer NOT NULL,
    mien character varying(50),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.city OWNER TO hoangtv;

--
-- Name: city_city_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.city_city_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.city_city_id_seq OWNER TO hoangtv;

--
-- Name: city_city_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.city_city_id_seq OWNED BY public.city.city_id;


--
-- Name: country; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.country (
    country_id integer NOT NULL,
    ten_quoc_gia character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.country OWNER TO hoangtv;

--
-- Name: country_country_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.country_country_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.country_country_id_seq OWNER TO hoangtv;

--
-- Name: country_country_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.country_country_id_seq OWNED BY public.country.country_id;


--
-- Name: customer; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.customer (
    customer_id integer NOT NULL,
    ho_va_ten character varying(100),
    ngay_sinh date,
    user_id integer NOT NULL,
    gioi_tinh integer,
    ten_doanh_nghiep character varying(200),
    dia_chi_doanh_nghiep text,
    country_id integer,
    city_id integer,
    district_id integer,
    website_doanh_nghiep character varying(255),
    so_dien_thoai character varying(20),
    email_doanh_nghiep character varying(100),
    ma_remarketing text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.customer OWNER TO hoangtv;

--
-- Name: customer_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.customer_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.customer_customer_id_seq OWNER TO hoangtv;

--
-- Name: customer_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.customer_customer_id_seq OWNED BY public.customer.customer_id;


--
-- Name: data_source; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.data_source (
    source_id integer NOT NULL,
    ten_nguon_du_lieu text NOT NULL,
    source_status_id integer NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.data_source OWNER TO hoangtv;

--
-- Name: data_source_source_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.data_source_source_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.data_source_source_id_seq OWNER TO hoangtv;

--
-- Name: data_source_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.data_source_source_id_seq OWNED BY public.data_source.source_id;


--
-- Name: district; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.district (
    district_id integer NOT NULL,
    ten_quan_huyen character varying(100) NOT NULL,
    city_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.district OWNER TO hoangtv;

--
-- Name: district_district_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.district_district_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.district_district_id_seq OWNER TO hoangtv;

--
-- Name: district_district_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.district_district_id_seq OWNED BY public.district.district_id;


--
-- Name: global_price; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.global_price (
    global_price_id integer NOT NULL,
    website_id integer NOT NULL,
    is_uniform_price boolean DEFAULT false,
    uniform_buy_price numeric(15,2),
    uniform_sell_price numeric(15,2),
    uniform_buy_price_unit_id integer,
    uniform_sell_price_unit_id integer,
    format_id integer,
    buy_price numeric(15,2),
    buy_price_unit_id integer,
    sell_price numeric(15,2),
    sell_price_unit_id integer,
    start_date date NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.global_price OWNER TO hoangtv;

--
-- Name: global_price_global_price_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.global_price_global_price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.global_price_global_price_id_seq OWNER TO hoangtv;

--
-- Name: global_price_global_price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.global_price_global_price_id_seq OWNED BY public.global_price.global_price_id;


--
-- Name: price_type; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.price_type (
    price_type_id integer NOT NULL,
    price_type_name character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.price_type OWNER TO hoangtv;

--
-- Name: price_type_price_type_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.price_type_price_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.price_type_price_type_id_seq OWNER TO hoangtv;

--
-- Name: price_type_price_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.price_type_price_type_id_seq OWNED BY public.price_type.price_type_id;


--
-- Name: product; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.product (
    product_id integer NOT NULL,
    ten_san_pham character varying(255),
    mo_ta_san_pham text,
    bo_chi_so integer,
    lien_ket_san_pham character varying(255),
    hinh_anh_san_pham bytea,
    source_id integer,
    productstatus_id integer,
    gia_san_pham numeric(15,2),
    gia_khuyen_mai numeric(15,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.product OWNER TO hoangtv;

--
-- Name: product_group; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.product_group (
    productgroup_id integer NOT NULL,
    ten_nhom character varying(100) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.product_group OWNER TO hoangtv;

--
-- Name: product_group_mapping; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.product_group_mapping (
    mapping_id integer NOT NULL,
    product_id integer NOT NULL,
    productgroup_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.product_group_mapping OWNER TO hoangtv;

--
-- Name: product_group_mapping_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.product_group_mapping_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_group_mapping_mapping_id_seq OWNER TO hoangtv;

--
-- Name: product_group_mapping_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.product_group_mapping_mapping_id_seq OWNED BY public.product_group_mapping.mapping_id;


--
-- Name: product_group_productgroup_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.product_group_productgroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_group_productgroup_id_seq OWNER TO hoangtv;

--
-- Name: product_group_productgroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.product_group_productgroup_id_seq OWNED BY public.product_group.productgroup_id;


--
-- Name: product_product_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.product_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_product_id_seq OWNER TO hoangtv;

--
-- Name: product_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.product_product_id_seq OWNED BY public.product.product_id;


--
-- Name: product_status; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.product_status (
    productstatus_id integer NOT NULL,
    ten_trang_thai character varying(50),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.product_status OWNER TO hoangtv;

--
-- Name: product_status_productstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.product_status_productstatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_status_productstatus_id_seq OWNER TO hoangtv;

--
-- Name: product_status_productstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.product_status_productstatus_id_seq OWNED BY public.product_status.productstatus_id;


--
-- Name: publisher; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.publisher (
    publisher_id integer NOT NULL,
    ten_publisher character varying(100) NOT NULL,
    user_id integer NOT NULL,
    email character varying(100) NOT NULL,
    so_dien_thoai character varying(20),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.publisher OWNER TO hoangtv;

--
-- Name: publisher_publisher_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.publisher_publisher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.publisher_publisher_id_seq OWNER TO hoangtv;

--
-- Name: publisher_publisher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.publisher_publisher_id_seq OWNED BY public.publisher.publisher_id;


--
-- Name: remarketing_excluded_website; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.remarketing_excluded_website (
    remarketing_id integer NOT NULL,
    website_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.remarketing_excluded_website OWNER TO hoangtv;

--
-- Name: remarketing_setting; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.remarketing_setting (
    remarketing_id integer NOT NULL,
    ads_group_id integer NOT NULL,
    auto_remarketing boolean DEFAULT false,
    tan_suat_hien_thi integer,
    thoi_gian_giua_hai_lan_hien_thi integer,
    thoi_gian_remarketing integer,
    stop_on_click boolean DEFAULT false,
    stop_on_view boolean DEFAULT false,
    max_view integer
);


ALTER TABLE public.remarketing_setting OWNER TO hoangtv;

--
-- Name: remarketing_setting_remarketing_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.remarketing_setting_remarketing_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.remarketing_setting_remarketing_id_seq OWNER TO hoangtv;

--
-- Name: remarketing_setting_remarketing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.remarketing_setting_remarketing_id_seq OWNED BY public.remarketing_setting.remarketing_id;


--
-- Name: role; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.role (
    role_id integer NOT NULL,
    name text NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.role OWNER TO hoangtv;

--
-- Name: role_role_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.role_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.role_role_id_seq OWNER TO hoangtv;

--
-- Name: role_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.role_role_id_seq OWNED BY public.role.role_id;


--
-- Name: source_status; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.source_status (
    source_status_id integer NOT NULL,
    ten_trang_thai character varying(50) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.source_status OWNER TO hoangtv;

--
-- Name: source_status_source_status_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.source_status_source_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.source_status_source_status_id_seq OWNER TO hoangtv;

--
-- Name: source_status_source_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.source_status_source_status_id_seq OWNED BY public.source_status.source_status_id;


--
-- Name: status_ads; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.status_ads (
    status_id integer NOT NULL,
    ten_trang_thai character varying(50),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.status_ads OWNER TO hoangtv;

--
-- Name: status_ads_status_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.status_ads_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.status_ads_status_id_seq OWNER TO hoangtv;

--
-- Name: status_ads_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.status_ads_status_id_seq OWNED BY public.status_ads.status_id;


--
-- Name: target_audience; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.target_audience (
    ta_id integer NOT NULL,
    ten_nhom_doi_tuong character varying(100),
    trang_da_truy_cap text,
    apply_all_product boolean DEFAULT false,
    hanhviid integer,
    loaitruhanhviid integer,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.target_audience OWNER TO hoangtv;

--
-- Name: target_audience_behavior; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.target_audience_behavior (
    tab_id integer NOT NULL,
    ta_id integer,
    behavior_id integer,
    is_excluded boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.target_audience_behavior OWNER TO hoangtv;

--
-- Name: target_audience_behavior_tab_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.target_audience_behavior_tab_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.target_audience_behavior_tab_id_seq OWNER TO hoangtv;

--
-- Name: target_audience_behavior_tab_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.target_audience_behavior_tab_id_seq OWNED BY public.target_audience_behavior.tab_id;


--
-- Name: target_audience_ta_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.target_audience_ta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.target_audience_ta_id_seq OWNER TO hoangtv;

--
-- Name: target_audience_ta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.target_audience_ta_id_seq OWNED BY public.target_audience.ta_id;


--
-- Name: transaction_system; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.transaction_system (
    tran_id integer NOT NULL,
    user_id integer,
    so_tien_nap numeric(18,2),
    thoi_gian_nap timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    ghi_chu character varying(200),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.transaction_system OWNER TO hoangtv;

--
-- Name: transaction_system_tran_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.transaction_system_tran_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transaction_system_tran_id_seq OWNER TO hoangtv;

--
-- Name: transaction_system_tran_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.transaction_system_tran_id_seq OWNED BY public.transaction_system.tran_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username text NOT NULL,
    email text NOT NULL,
    password text NOT NULL,
    role_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.users OWNER TO hoangtv;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO hoangtv;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: website; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.website (
    website_id integer NOT NULL,
    domain_website character varying(255),
    link_url character varying(255),
    tong_so_luong_vung integer DEFAULT 0,
    publisher_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.website OWNER TO hoangtv;

--
-- Name: website_website_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.website_website_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.website_website_id_seq OWNER TO hoangtv;

--
-- Name: website_website_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.website_website_id_seq OWNED BY public.website.website_id;


--
-- Name: zone_price_mapping; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.zone_price_mapping (
    mapping_id integer NOT NULL,
    zone_price_setup_id integer NOT NULL,
    zone_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.zone_price_mapping OWNER TO hoangtv;

--
-- Name: zone_price_mapping_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.zone_price_mapping_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.zone_price_mapping_mapping_id_seq OWNER TO hoangtv;

--
-- Name: zone_price_mapping_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.zone_price_mapping_mapping_id_seq OWNED BY public.zone_price_mapping.mapping_id;


--
-- Name: zone_price_setup; Type: TABLE; Schema: public; Owner: hoangtv
--

CREATE TABLE public.zone_price_setup (
    zone_price_setup_id integer NOT NULL,
    website_id integer NOT NULL,
    buy_price numeric(15,2) NOT NULL,
    buy_price_type_id integer NOT NULL,
    sell_price numeric(15,2) NOT NULL,
    sell_price_type_id integer NOT NULL,
    start_date timestamp with time zone NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    active boolean DEFAULT true
);


ALTER TABLE public.zone_price_setup OWNER TO hoangtv;

--
-- Name: zone_price_setup_zone_price_setup_id_seq; Type: SEQUENCE; Schema: public; Owner: hoangtv
--

CREATE SEQUENCE public.zone_price_setup_zone_price_setup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.zone_price_setup_zone_price_setup_id_seq OWNER TO hoangtv;

--
-- Name: zone_price_setup_zone_price_setup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hoangtv
--

ALTER SEQUENCE public.zone_price_setup_zone_price_setup_id_seq OWNED BY public.zone_price_setup.zone_price_setup_id;


--
-- Name: ads ads_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads ALTER COLUMN ads_id SET DEFAULT nextval('public.ads_ads_id_seq'::regclass);


--
-- Name: ads_display ads_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_display ALTER COLUMN ads_id SET DEFAULT nextval('public.ads_display_ads_id_seq'::regclass);


--
-- Name: ads_ecom ads_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_ecom ALTER COLUMN ads_id SET DEFAULT nextval('public.ads_ecom_ads_id_seq'::regclass);


--
-- Name: ads_format format_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_format ALTER COLUMN format_id SET DEFAULT nextval('public.ads_format_format_id_seq'::regclass);


--
-- Name: ads_group ads_group_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group ALTER COLUMN ads_group_id SET DEFAULT nextval('public.ads_group_ads_group_id_seq'::regclass);


--
-- Name: ads_group_product_group id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_product_group ALTER COLUMN id SET DEFAULT nextval('public.ads_group_product_group_id_seq'::regclass);


--
-- Name: ads_group_status ads_group_status_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_status ALTER COLUMN ads_group_status_id SET DEFAULT nextval('public.ads_group_status_ads_group_status_id_seq'::regclass);


--
-- Name: ads_group_target_audience id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_target_audience ALTER COLUMN id SET DEFAULT nextval('public.ads_group_target_audience_id_seq'::regclass);


--
-- Name: ads_group_website id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_website ALTER COLUMN id SET DEFAULT nextval('public.ads_group_website_id_seq'::regclass);


--
-- Name: ads_native ads_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_native ALTER COLUMN ads_id SET DEFAULT nextval('public.ads_native_ads_id_seq'::regclass);


--
-- Name: ads_zone zone_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_zone ALTER COLUMN zone_id SET DEFAULT nextval('public.ads_zone_zone_id_seq'::regclass);


--
-- Name: ads_zone_size size_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_zone_size ALTER COLUMN size_id SET DEFAULT nextval('public.ads_zone_size_size_id_seq'::regclass);


--
-- Name: behaviour behav_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.behaviour ALTER COLUMN behav_id SET DEFAULT nextval('public.behaviour_behav_id_seq'::regclass);


--
-- Name: campaign camp_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign ALTER COLUMN camp_id SET DEFAULT nextval('public.campaign_camp_id_seq'::regclass);


--
-- Name: campaign_status campstatus_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign_status ALTER COLUMN campstatus_id SET DEFAULT nextval('public.campaign_status_campstatus_id_seq'::regclass);


--
-- Name: campaign_type camp_type_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign_type ALTER COLUMN camp_type_id SET DEFAULT nextval('public.campaign_type_camp_type_id_seq'::regclass);


--
-- Name: city city_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.city ALTER COLUMN city_id SET DEFAULT nextval('public.city_city_id_seq'::regclass);


--
-- Name: country country_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.country ALTER COLUMN country_id SET DEFAULT nextval('public.country_country_id_seq'::regclass);


--
-- Name: customer customer_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.customer ALTER COLUMN customer_id SET DEFAULT nextval('public.customer_customer_id_seq'::regclass);


--
-- Name: data_source source_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.data_source ALTER COLUMN source_id SET DEFAULT nextval('public.data_source_source_id_seq'::regclass);


--
-- Name: district district_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.district ALTER COLUMN district_id SET DEFAULT nextval('public.district_district_id_seq'::regclass);


--
-- Name: global_price global_price_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.global_price ALTER COLUMN global_price_id SET DEFAULT nextval('public.global_price_global_price_id_seq'::regclass);


--
-- Name: price_type price_type_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.price_type ALTER COLUMN price_type_id SET DEFAULT nextval('public.price_type_price_type_id_seq'::regclass);


--
-- Name: product product_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product ALTER COLUMN product_id SET DEFAULT nextval('public.product_product_id_seq'::regclass);


--
-- Name: product_group productgroup_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product_group ALTER COLUMN productgroup_id SET DEFAULT nextval('public.product_group_productgroup_id_seq'::regclass);


--
-- Name: product_group_mapping mapping_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product_group_mapping ALTER COLUMN mapping_id SET DEFAULT nextval('public.product_group_mapping_mapping_id_seq'::regclass);


--
-- Name: product_status productstatus_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product_status ALTER COLUMN productstatus_id SET DEFAULT nextval('public.product_status_productstatus_id_seq'::regclass);


--
-- Name: publisher publisher_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.publisher ALTER COLUMN publisher_id SET DEFAULT nextval('public.publisher_publisher_id_seq'::regclass);


--
-- Name: remarketing_setting remarketing_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.remarketing_setting ALTER COLUMN remarketing_id SET DEFAULT nextval('public.remarketing_setting_remarketing_id_seq'::regclass);


--
-- Name: role role_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.role ALTER COLUMN role_id SET DEFAULT nextval('public.role_role_id_seq'::regclass);


--
-- Name: source_status source_status_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.source_status ALTER COLUMN source_status_id SET DEFAULT nextval('public.source_status_source_status_id_seq'::regclass);


--
-- Name: status_ads status_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.status_ads ALTER COLUMN status_id SET DEFAULT nextval('public.status_ads_status_id_seq'::regclass);


--
-- Name: target_audience ta_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.target_audience ALTER COLUMN ta_id SET DEFAULT nextval('public.target_audience_ta_id_seq'::regclass);


--
-- Name: target_audience_behavior tab_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.target_audience_behavior ALTER COLUMN tab_id SET DEFAULT nextval('public.target_audience_behavior_tab_id_seq'::regclass);


--
-- Name: transaction_system tran_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.transaction_system ALTER COLUMN tran_id SET DEFAULT nextval('public.transaction_system_tran_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: website website_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.website ALTER COLUMN website_id SET DEFAULT nextval('public.website_website_id_seq'::regclass);


--
-- Name: zone_price_mapping mapping_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.zone_price_mapping ALTER COLUMN mapping_id SET DEFAULT nextval('public.zone_price_mapping_mapping_id_seq'::regclass);


--
-- Name: zone_price_setup zone_price_setup_id; Type: DEFAULT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.zone_price_setup ALTER COLUMN zone_price_setup_id SET DEFAULT nextval('public.zone_price_setup_zone_price_setup_id_seq'::regclass);


--
-- Name: ad_size_format ad_size_format_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ad_size_format
    ADD CONSTRAINT ad_size_format_pkey PRIMARY KEY (size_id, format_id);


--
-- Name: ads_display ads_display_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_display
    ADD CONSTRAINT ads_display_pkey PRIMARY KEY (ads_id);


--
-- Name: ads_ecom ads_ecom_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_ecom
    ADD CONSTRAINT ads_ecom_pkey PRIMARY KEY (ads_id);


--
-- Name: ads_format ads_format_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_format
    ADD CONSTRAINT ads_format_pkey PRIMARY KEY (format_id);


--
-- Name: ads_group ads_group_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group
    ADD CONSTRAINT ads_group_pkey PRIMARY KEY (ads_group_id);


--
-- Name: ads_group_product_group ads_group_product_group_ads_group_id_product_group_id_key; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_product_group
    ADD CONSTRAINT ads_group_product_group_ads_group_id_product_group_id_key UNIQUE (ads_group_id, product_group_id);


--
-- Name: ads_group_product_group ads_group_product_group_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_product_group
    ADD CONSTRAINT ads_group_product_group_pkey PRIMARY KEY (id);


--
-- Name: ads_group_status ads_group_status_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_status
    ADD CONSTRAINT ads_group_status_pkey PRIMARY KEY (ads_group_status_id);


--
-- Name: ads_group_target_audience ads_group_target_audience_ads_group_id_ta_id_key; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_target_audience
    ADD CONSTRAINT ads_group_target_audience_ads_group_id_ta_id_key UNIQUE (ads_group_id, ta_id);


--
-- Name: ads_group_target_audience ads_group_target_audience_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_target_audience
    ADD CONSTRAINT ads_group_target_audience_pkey PRIMARY KEY (id);


--
-- Name: ads_group_website ads_group_website_ads_group_id_website_id_key; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_website
    ADD CONSTRAINT ads_group_website_ads_group_id_website_id_key UNIQUE (ads_group_id, website_id);


--
-- Name: ads_group_website ads_group_website_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_website
    ADD CONSTRAINT ads_group_website_pkey PRIMARY KEY (id);


--
-- Name: ads_link_format ads_link_format_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_link_format
    ADD CONSTRAINT ads_link_format_pkey PRIMARY KEY (ads_id, format_id);


--
-- Name: ads_native ads_native_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_native
    ADD CONSTRAINT ads_native_pkey PRIMARY KEY (ads_id);


--
-- Name: ads ads_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads
    ADD CONSTRAINT ads_pkey PRIMARY KEY (ads_id);


--
-- Name: ads_zone_format ads_zone_format_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_zone_format
    ADD CONSTRAINT ads_zone_format_pkey PRIMARY KEY (zone_id, format_id);


--
-- Name: ads_zone ads_zone_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_zone
    ADD CONSTRAINT ads_zone_pkey PRIMARY KEY (zone_id);


--
-- Name: ads_zone_size ads_zone_size_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_zone_size
    ADD CONSTRAINT ads_zone_size_pkey PRIMARY KEY (size_id);


--
-- Name: behaviour behaviour_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.behaviour
    ADD CONSTRAINT behaviour_pkey PRIMARY KEY (behav_id);


--
-- Name: behaviour behaviour_ten_hanh_vi_key; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.behaviour
    ADD CONSTRAINT behaviour_ten_hanh_vi_key UNIQUE (ten_hanh_vi);


--
-- Name: campaign campaign_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign
    ADD CONSTRAINT campaign_pkey PRIMARY KEY (camp_id);


--
-- Name: campaign_status campaign_status_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign_status
    ADD CONSTRAINT campaign_status_pkey PRIMARY KEY (campstatus_id);


--
-- Name: campaign_type campaign_type_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign_type
    ADD CONSTRAINT campaign_type_pkey PRIMARY KEY (camp_type_id);


--
-- Name: campaign_type campaign_type_ten_loai_chien_dich_key; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign_type
    ADD CONSTRAINT campaign_type_ten_loai_chien_dich_key UNIQUE (ten_loai_chien_dich);


--
-- Name: city city_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.city
    ADD CONSTRAINT city_pkey PRIMARY KEY (city_id);


--
-- Name: country country_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (country_id);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (customer_id);


--
-- Name: data_source data_source_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.data_source
    ADD CONSTRAINT data_source_pkey PRIMARY KEY (source_id);


--
-- Name: district district_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.district
    ADD CONSTRAINT district_pkey PRIMARY KEY (district_id);


--
-- Name: global_price global_price_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.global_price
    ADD CONSTRAINT global_price_pkey PRIMARY KEY (global_price_id);


--
-- Name: price_type price_type_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.price_type
    ADD CONSTRAINT price_type_pkey PRIMARY KEY (price_type_id);


--
-- Name: product_group_mapping product_group_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product_group_mapping
    ADD CONSTRAINT product_group_mapping_pkey PRIMARY KEY (mapping_id);


--
-- Name: product_group product_group_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product_group
    ADD CONSTRAINT product_group_pkey PRIMARY KEY (productgroup_id);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (product_id);


--
-- Name: product_status product_status_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product_status
    ADD CONSTRAINT product_status_pkey PRIMARY KEY (productstatus_id);


--
-- Name: publisher publisher_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.publisher
    ADD CONSTRAINT publisher_pkey PRIMARY KEY (publisher_id);


--
-- Name: remarketing_excluded_website remarketing_excluded_website_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.remarketing_excluded_website
    ADD CONSTRAINT remarketing_excluded_website_pkey PRIMARY KEY (remarketing_id, website_id);


--
-- Name: remarketing_setting remarketing_setting_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.remarketing_setting
    ADD CONSTRAINT remarketing_setting_pkey PRIMARY KEY (remarketing_id);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (role_id);


--
-- Name: source_status source_status_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.source_status
    ADD CONSTRAINT source_status_pkey PRIMARY KEY (source_status_id);


--
-- Name: status_ads status_ads_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.status_ads
    ADD CONSTRAINT status_ads_pkey PRIMARY KEY (status_id);


--
-- Name: target_audience_behavior target_audience_behavior_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.target_audience_behavior
    ADD CONSTRAINT target_audience_behavior_pkey PRIMARY KEY (tab_id);


--
-- Name: target_audience_behavior target_audience_behavior_ta_id_behavior_id_key; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.target_audience_behavior
    ADD CONSTRAINT target_audience_behavior_ta_id_behavior_id_key UNIQUE (ta_id, behavior_id);


--
-- Name: target_audience target_audience_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.target_audience
    ADD CONSTRAINT target_audience_pkey PRIMARY KEY (ta_id);


--
-- Name: transaction_system transaction_system_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.transaction_system
    ADD CONSTRAINT transaction_system_pkey PRIMARY KEY (tran_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: website website_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.website
    ADD CONSTRAINT website_pkey PRIMARY KEY (website_id);


--
-- Name: zone_price_mapping zone_price_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.zone_price_mapping
    ADD CONSTRAINT zone_price_mapping_pkey PRIMARY KEY (mapping_id);


--
-- Name: zone_price_mapping zone_price_mapping_zone_price_setup_id_zone_id_key; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.zone_price_mapping
    ADD CONSTRAINT zone_price_mapping_zone_price_setup_id_zone_id_key UNIQUE (zone_price_setup_id, zone_id);


--
-- Name: zone_price_setup zone_price_setup_pkey; Type: CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.zone_price_setup
    ADD CONSTRAINT zone_price_setup_pkey PRIMARY KEY (zone_price_setup_id);


--
-- Name: ad_size_format ad_size_format_format_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ad_size_format
    ADD CONSTRAINT ad_size_format_format_id_fkey FOREIGN KEY (format_id) REFERENCES public.ads_format(format_id) ON DELETE CASCADE;


--
-- Name: ad_size_format ad_size_format_size_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ad_size_format
    ADD CONSTRAINT ad_size_format_size_id_fkey FOREIGN KEY (size_id) REFERENCES public.ads_zone_size(size_id) ON DELETE CASCADE;


--
-- Name: ads ads_ads_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads
    ADD CONSTRAINT ads_ads_group_id_fkey FOREIGN KEY (ads_group_id) REFERENCES public.ads_group(ads_group_id) ON DELETE CASCADE;


--
-- Name: ads ads_ads_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads
    ADD CONSTRAINT ads_ads_status_id_fkey FOREIGN KEY (ads_status_id) REFERENCES public.status_ads(status_id) ON DELETE CASCADE;


--
-- Name: ads_display ads_display_format_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_display
    ADD CONSTRAINT ads_display_format_id_fkey FOREIGN KEY (format_id) REFERENCES public.ads_format(format_id) ON DELETE CASCADE;


--
-- Name: ads_ecom ads_ecom_format_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_ecom
    ADD CONSTRAINT ads_ecom_format_id_fkey FOREIGN KEY (format_id) REFERENCES public.ads_format(format_id) ON DELETE CASCADE;


--
-- Name: ads_format ads_format_campaign_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_format
    ADD CONSTRAINT ads_format_campaign_type_id_fkey FOREIGN KEY (campaign_type_id) REFERENCES public.campaign_type(camp_type_id) ON DELETE CASCADE;


--
-- Name: ads_group ads_group_ads_group_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group
    ADD CONSTRAINT ads_group_ads_group_status_id_fkey FOREIGN KEY (ads_group_status_id) REFERENCES public.ads_group_status(ads_group_status_id) ON DELETE CASCADE;


--
-- Name: ads_group ads_group_camp_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group
    ADD CONSTRAINT ads_group_camp_id_fkey FOREIGN KEY (camp_id) REFERENCES public.campaign(camp_id) ON DELETE CASCADE;


--
-- Name: ads_group_product_group ads_group_product_group_ads_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_product_group
    ADD CONSTRAINT ads_group_product_group_ads_group_id_fkey FOREIGN KEY (ads_group_id) REFERENCES public.ads_group(ads_group_id) ON DELETE CASCADE;


--
-- Name: ads_group_product_group ads_group_product_group_product_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_product_group
    ADD CONSTRAINT ads_group_product_group_product_group_id_fkey FOREIGN KEY (product_group_id) REFERENCES public.product_group(productgroup_id) ON DELETE CASCADE;


--
-- Name: ads_group_target_audience ads_group_target_audience_ads_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_target_audience
    ADD CONSTRAINT ads_group_target_audience_ads_group_id_fkey FOREIGN KEY (ads_group_id) REFERENCES public.ads_group(ads_group_id) ON DELETE CASCADE;


--
-- Name: ads_group_target_audience ads_group_target_audience_ta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_target_audience
    ADD CONSTRAINT ads_group_target_audience_ta_id_fkey FOREIGN KEY (ta_id) REFERENCES public.target_audience(ta_id) ON DELETE CASCADE;


--
-- Name: ads_group_website ads_group_website_ads_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_website
    ADD CONSTRAINT ads_group_website_ads_group_id_fkey FOREIGN KEY (ads_group_id) REFERENCES public.ads_group(ads_group_id) ON DELETE CASCADE;


--
-- Name: ads_group_website ads_group_website_website_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_group_website
    ADD CONSTRAINT ads_group_website_website_id_fkey FOREIGN KEY (website_id) REFERENCES public.website(website_id) ON DELETE CASCADE;


--
-- Name: ads_link_format ads_link_format_ads_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_link_format
    ADD CONSTRAINT ads_link_format_ads_id_fkey FOREIGN KEY (ads_id) REFERENCES public.ads(ads_id) ON DELETE CASCADE;


--
-- Name: ads_link_format ads_link_format_format_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_link_format
    ADD CONSTRAINT ads_link_format_format_id_fkey FOREIGN KEY (format_id) REFERENCES public.ads_format(format_id) ON DELETE CASCADE;


--
-- Name: ads_native ads_native_format_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_native
    ADD CONSTRAINT ads_native_format_id_fkey FOREIGN KEY (format_id) REFERENCES public.ads_format(format_id) ON DELETE CASCADE;


--
-- Name: ads_zone_format ads_zone_format_format_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_zone_format
    ADD CONSTRAINT ads_zone_format_format_id_fkey FOREIGN KEY (format_id) REFERENCES public.ads_format(format_id) ON DELETE CASCADE;


--
-- Name: ads_zone_format ads_zone_format_zone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_zone_format
    ADD CONSTRAINT ads_zone_format_zone_id_fkey FOREIGN KEY (zone_id) REFERENCES public.ads_zone(zone_id) ON DELETE CASCADE;


--
-- Name: ads_zone ads_zone_size_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_zone
    ADD CONSTRAINT ads_zone_size_id_fkey FOREIGN KEY (size_id) REFERENCES public.ads_zone_size(size_id) ON DELETE CASCADE;


--
-- Name: ads_zone ads_zone_website_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.ads_zone
    ADD CONSTRAINT ads_zone_website_id_fkey FOREIGN KEY (website_id) REFERENCES public.website(website_id) ON DELETE CASCADE;


--
-- Name: campaign campaign_camp_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign
    ADD CONSTRAINT campaign_camp_type_id_fkey FOREIGN KEY (camp_type_id) REFERENCES public.campaign_type(camp_type_id) ON DELETE CASCADE;


--
-- Name: campaign campaign_campstatus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign
    ADD CONSTRAINT campaign_campstatus_id_fkey FOREIGN KEY (campstatus_id) REFERENCES public.campaign_status(campstatus_id) ON DELETE CASCADE;


--
-- Name: campaign campaign_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign
    ADD CONSTRAINT campaign_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: campaign campaign_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.campaign
    ADD CONSTRAINT campaign_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.data_source(source_id) ON DELETE CASCADE;


--
-- Name: city city_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.city
    ADD CONSTRAINT city_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.country(country_id) ON DELETE CASCADE;


--
-- Name: customer customer_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.city(city_id) ON DELETE SET NULL;


--
-- Name: customer customer_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.country(country_id) ON DELETE SET NULL;


--
-- Name: customer customer_district_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_district_id_fkey FOREIGN KEY (district_id) REFERENCES public.district(district_id) ON DELETE SET NULL;


--
-- Name: customer customer_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.customer
    ADD CONSTRAINT customer_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: data_source data_source_source_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.data_source
    ADD CONSTRAINT data_source_source_status_id_fkey FOREIGN KEY (source_status_id) REFERENCES public.source_status(source_status_id) ON DELETE CASCADE;


--
-- Name: data_source data_source_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.data_source
    ADD CONSTRAINT data_source_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: district district_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.district
    ADD CONSTRAINT district_city_id_fkey FOREIGN KEY (city_id) REFERENCES public.city(city_id) ON DELETE CASCADE;


--
-- Name: global_price global_price_buy_price_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.global_price
    ADD CONSTRAINT global_price_buy_price_unit_id_fkey FOREIGN KEY (buy_price_unit_id) REFERENCES public.price_type(price_type_id) ON DELETE SET NULL;


--
-- Name: global_price global_price_format_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.global_price
    ADD CONSTRAINT global_price_format_id_fkey FOREIGN KEY (format_id) REFERENCES public.ads_format(format_id) ON DELETE SET NULL;


--
-- Name: global_price global_price_sell_price_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.global_price
    ADD CONSTRAINT global_price_sell_price_unit_id_fkey FOREIGN KEY (sell_price_unit_id) REFERENCES public.price_type(price_type_id) ON DELETE SET NULL;


--
-- Name: global_price global_price_uniform_buy_price_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.global_price
    ADD CONSTRAINT global_price_uniform_buy_price_unit_id_fkey FOREIGN KEY (uniform_buy_price_unit_id) REFERENCES public.price_type(price_type_id) ON DELETE SET NULL;


--
-- Name: global_price global_price_uniform_sell_price_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.global_price
    ADD CONSTRAINT global_price_uniform_sell_price_unit_id_fkey FOREIGN KEY (uniform_sell_price_unit_id) REFERENCES public.price_type(price_type_id) ON DELETE SET NULL;


--
-- Name: global_price global_price_website_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.global_price
    ADD CONSTRAINT global_price_website_id_fkey FOREIGN KEY (website_id) REFERENCES public.website(website_id) ON DELETE CASCADE;


--
-- Name: product_group_mapping product_group_mapping_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product_group_mapping
    ADD CONSTRAINT product_group_mapping_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(product_id) ON DELETE CASCADE;


--
-- Name: product_group_mapping product_group_mapping_productgroup_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product_group_mapping
    ADD CONSTRAINT product_group_mapping_productgroup_id_fkey FOREIGN KEY (productgroup_id) REFERENCES public.product_group(productgroup_id) ON DELETE CASCADE;


--
-- Name: product product_productstatus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_productstatus_id_fkey FOREIGN KEY (productstatus_id) REFERENCES public.product_status(productstatus_id) ON DELETE CASCADE;


--
-- Name: product product_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.data_source(source_id) ON DELETE CASCADE;


--
-- Name: publisher publisher_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.publisher
    ADD CONSTRAINT publisher_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: remarketing_excluded_website remarketing_excluded_website_remarketing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.remarketing_excluded_website
    ADD CONSTRAINT remarketing_excluded_website_remarketing_id_fkey FOREIGN KEY (remarketing_id) REFERENCES public.remarketing_setting(remarketing_id) ON DELETE CASCADE;


--
-- Name: remarketing_excluded_website remarketing_excluded_website_website_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.remarketing_excluded_website
    ADD CONSTRAINT remarketing_excluded_website_website_id_fkey FOREIGN KEY (website_id) REFERENCES public.website(website_id) ON DELETE CASCADE;


--
-- Name: remarketing_setting remarketing_setting_ads_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.remarketing_setting
    ADD CONSTRAINT remarketing_setting_ads_group_id_fkey FOREIGN KEY (ads_group_id) REFERENCES public.ads_group(ads_group_id) ON DELETE CASCADE;


--
-- Name: target_audience_behavior target_audience_behavior_behavior_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.target_audience_behavior
    ADD CONSTRAINT target_audience_behavior_behavior_id_fkey FOREIGN KEY (behavior_id) REFERENCES public.behaviour(behav_id);


--
-- Name: target_audience_behavior target_audience_behavior_ta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.target_audience_behavior
    ADD CONSTRAINT target_audience_behavior_ta_id_fkey FOREIGN KEY (ta_id) REFERENCES public.target_audience(ta_id);


--
-- Name: transaction_system transaction_system_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.transaction_system
    ADD CONSTRAINT transaction_system_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(role_id);


--
-- Name: website website_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.website
    ADD CONSTRAINT website_publisher_id_fkey FOREIGN KEY (publisher_id) REFERENCES public.publisher(publisher_id) ON DELETE SET NULL;


--
-- Name: zone_price_mapping zone_price_mapping_zone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.zone_price_mapping
    ADD CONSTRAINT zone_price_mapping_zone_id_fkey FOREIGN KEY (zone_id) REFERENCES public.ads_zone(zone_id) ON DELETE CASCADE;


--
-- Name: zone_price_mapping zone_price_mapping_zone_price_setup_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.zone_price_mapping
    ADD CONSTRAINT zone_price_mapping_zone_price_setup_id_fkey FOREIGN KEY (zone_price_setup_id) REFERENCES public.zone_price_setup(zone_price_setup_id) ON DELETE CASCADE;


--
-- Name: zone_price_setup zone_price_setup_buy_price_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.zone_price_setup
    ADD CONSTRAINT zone_price_setup_buy_price_type_id_fkey FOREIGN KEY (buy_price_type_id) REFERENCES public.price_type(price_type_id) ON DELETE CASCADE;


--
-- Name: zone_price_setup zone_price_setup_sell_price_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.zone_price_setup
    ADD CONSTRAINT zone_price_setup_sell_price_type_id_fkey FOREIGN KEY (sell_price_type_id) REFERENCES public.price_type(price_type_id) ON DELETE CASCADE;


--
-- Name: zone_price_setup zone_price_setup_website_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hoangtv
--

ALTER TABLE ONLY public.zone_price_setup
    ADD CONSTRAINT zone_price_setup_website_id_fkey FOREIGN KEY (website_id) REFERENCES public.website(website_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

