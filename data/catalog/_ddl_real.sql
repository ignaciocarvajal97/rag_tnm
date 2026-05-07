--
-- PostgreSQL database dump
--

\restrict 2E95D4aUmIRKxeiuIDWgGRU7oTkQY1wN3noQ9HWInOlEEMz3ZcbQiah7T8zb8fp

-- Dumped from database version 16.9
-- Dumped by pg_dump version 16.13

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

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: caracteristicas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.caracteristicas (
    id_caracteristicas integer NOT NULL,
    tamano_contenedor character varying(255),
    peso_carga character varying(255),
    impo_expo character varying(255),
    dry character varying(255),
    numero_contenedor character varying(255),
    full_lcl character varying(255),
    fk_servicio integer,
    posicion_fila text,
    posicion_columna text,
    posicion text,
    contenedor_vaciolleno text,
    tipo_movimiento text
);


--
-- Name: caracteristicas_id_caracteristicas_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.caracteristicas_id_caracteristicas_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: caracteristicas_id_caracteristicas_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.caracteristicas_id_caracteristicas_seq OWNED BY public.caracteristicas.id_caracteristicas;


--
-- Name: charlas_transportistas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.charlas_transportistas (
    "TRASPORTE" text,
    "RUT" text,
    "NOMBRE CONDUCTOR" text,
    "CHARLA /TIPO" text,
    "FECHA" text,
    "MES" text,
    "ESTADO" double precision
);


--
-- Name: cliente_despacho; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cliente_despacho (
    id_cliente_despacho integer NOT NULL,
    nombre character varying(255),
    rut character varying(255),
    fk_servicio integer,
    fecha_conversion timestamp with time zone,
    antiguedad text
);


--
-- Name: cliente_despacho_id_cliente_despacho_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cliente_despacho_id_cliente_despacho_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cliente_despacho_id_cliente_despacho_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cliente_despacho_id_cliente_despacho_seq OWNED BY public.cliente_despacho.id_cliente_despacho;


--
-- Name: cliente_facturacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cliente_facturacion (
    id_customer integer NOT NULL,
    name character varying(255),
    rut character varying(255),
    fk_servicio integer,
    fecha_conversion date,
    antiguedad text
);


--
-- Name: cliente_facturacion_id_customer_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cliente_facturacion_id_customer_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cliente_facturacion_id_customer_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cliente_facturacion_id_customer_seq OWNED BY public.cliente_facturacion.id_customer;


--
-- Name: comercial; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.comercial (
    id_comercial integer NOT NULL,
    name character varying(255),
    rut character varying(255),
    fk_servicio integer
);


--
-- Name: comercial_id_comercial_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.comercial_id_comercial_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: comercial_id_comercial_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.comercial_id_comercial_seq OWNED BY public.comercial.id_comercial;


--
-- Name: conductor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.conductor (
    id_conductor integer NOT NULL,
    nombre character varying(255),
    rut character varying(255),
    fk_servicio integer,
    tipo_conductor text
);


--
-- Name: conductor_id_conductor_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.conductor_id_conductor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: conductor_id_conductor_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.conductor_id_conductor_seq OWNED BY public.conductor.id_conductor;


--
-- Name: direccion_llegada; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.direccion_llegada (
    id_direccion integer NOT NULL,
    comuna character varying(255),
    direccion character varying(255),
    fk_servicio integer,
    longitud text,
    latitud text
);


--
-- Name: direccion_llegada_id_direccion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.direccion_llegada_id_direccion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: direccion_llegada_id_direccion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.direccion_llegada_id_direccion_seq OWNED BY public.direccion_llegada.id_direccion;


--
-- Name: direccion_salida; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.direccion_salida (
    id_direccion_salida integer NOT NULL,
    comuna character varying(255),
    direccion character varying(255),
    fk_servicio integer,
    longitud text,
    latitud text
);


--
-- Name: direccion_salida_id_direccion_salida_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.direccion_salida_id_direccion_salida_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: direccion_salida_id_direccion_salida_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.direccion_salida_id_direccion_salida_seq OWNED BY public.direccion_salida.id_direccion_salida;


--
-- Name: documentacion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.documentacion (
    id_documentacion integer NOT NULL,
    docu text,
    ruta text,
    kpi_docu integer,
    creacion_documentacion timestamp without time zone,
    actualizacion_documentacion timestamp without time zone,
    responsable_documentacion text,
    codigo_carga text,
    fk_servicio integer
);


--
-- Name: documentacion_id_documentacion_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.documentacion_id_documentacion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: documentacion_id_documentacion_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.documentacion_id_documentacion_seq OWNED BY public.documentacion.id_documentacion;


--
-- Name: etapa; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.etapa (
    id_etapa integer NOT NULL,
    titulo character varying(255),
    codigo character varying(255),
    kilometros double precision,
    atraso character varying(255),
    diferencia_minutos double precision,
    tiempo_estadia double precision,
    servicio integer,
    dias_facturacion double precision,
    atraso_auto text,
    diferencia_minutos_auto numeric,
    causa_atrasos text,
    comentarios text,
    id_de_la_etapa numeric,
    posicion_tipo text,
    referencia text,
    fk_responsable text
);


--
-- Name: etapa_id_etapa_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.etapa_id_etapa_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: etapa_id_etapa_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.etapa_id_etapa_seq OWNED BY public.etapa.id_etapa;


--
-- Name: fact_servicios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fact_servicios (
    fk_cliente integer,
    fk_conductor integer,
    fk_comercial integer,
    fk_agencia integer,
    fk_etapa integer,
    fk_servicio integer,
    fk_direccion integer,
    fk_cliente_despacho integer,
    fk_caracteristicas integer,
    fk_nave integer,
    id integer NOT NULL,
    en_sitio text,
    horas_almacenamiento numeric,
    fecha_cierre_servicio date,
    horas_entre_entrega_guia numeric,
    horas_entre_entrega_eir numeric,
    horas_entre_guia_factura numeric,
    horas_entre_eir_factura numeric,
    horas_fecha_cierre numeric,
    estado text,
    referencia text
);


--
-- Name: facturas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.facturas (
    id_factura bigint NOT NULL,
    sii_fecha date,
    total_servicio numeric,
    total_cobros_extras numeric,
    creacion_factura date,
    actualizacion_factura date,
    sii_factura text,
    kpi_factura numeric,
    fk_servicio bigint
);


--
-- Name: nave; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nave (
    id_nave integer NOT NULL,
    nombre text,
    fk_servicio integer,
    "ETA_nave" date
);


--
-- Name: nave_id_nave_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.nave_id_nave_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nave_id_nave_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.nave_id_nave_seq OWNED BY public.nave.id_nave;


--
-- Name: real_time_arribo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.real_time_arribo (
    id_real_time integer NOT NULL,
    fecha_real_arribo timestamp without time zone,
    fk_servicio integer
);


--
-- Name: real_time_arribo_id_real_time_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.real_time_arribo_id_real_time_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: real_time_arribo_id_real_time_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.real_time_arribo_id_real_time_seq OWNED BY public.real_time_arribo.id_real_time;


--
-- Name: real_time_salida; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.real_time_salida (
    id_real_time integer NOT NULL,
    fecha_real_salida timestamp without time zone,
    fk_servicio integer
);


--
-- Name: real_time_salida_id_real_time_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.real_time_salida_id_real_time_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: real_time_salida_id_real_time_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.real_time_salida_id_real_time_seq OWNED BY public.real_time_salida.id_real_time;


--
-- Name: servicios_documentos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.servicios_documentos (
    id bigint NOT NULL,
    estado smallint,
    docu character varying(50),
    ruta character varying(255),
    "createdAt" timestamp without time zone,
    "updatedAt" timestamp without time zone,
    fk_servicio bigint,
    fk_responsable character varying(20),
    codigo_carga character varying(50)
);


--
-- Name: stock; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.stock (
    fk_servicio integer NOT NULL,
    numero_contenedor character varying,
    estado integer,
    cont_fila character varying,
    cont_columna character varying,
    cont_posicion character varying,
    posicion_ubicacion character varying,
    cont_tipo_mov character varying,
    cont_tipo character varying,
    cont_fecha date,
    cont_hora time without time zone,
    almacenaje_principal character varying,
    estado_contenedor character varying,
    tiempo_estadia character varying
);


--
-- Name: stock_fk_servicio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.stock_fk_servicio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: stock_fk_servicio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.stock_fk_servicio_seq OWNED BY public.stock.fk_servicio;


--
-- Name: time; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."time" (
    id_time integer NOT NULL,
    etapa_1_fecha timestamp without time zone,
    fk_servicio integer
);


--
-- Name: time_id_time_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.time_id_time_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: time_id_time_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.time_id_time_seq OWNED BY public."time".id_time;


--
-- Name: caracteristicas id_caracteristicas; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.caracteristicas ALTER COLUMN id_caracteristicas SET DEFAULT nextval('public.caracteristicas_id_caracteristicas_seq'::regclass);


--
-- Name: cliente_despacho id_cliente_despacho; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente_despacho ALTER COLUMN id_cliente_despacho SET DEFAULT nextval('public.cliente_despacho_id_cliente_despacho_seq'::regclass);


--
-- Name: cliente_facturacion id_customer; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente_facturacion ALTER COLUMN id_customer SET DEFAULT nextval('public.cliente_facturacion_id_customer_seq'::regclass);


--
-- Name: comercial id_comercial; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comercial ALTER COLUMN id_comercial SET DEFAULT nextval('public.comercial_id_comercial_seq'::regclass);


--
-- Name: conductor id_conductor; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conductor ALTER COLUMN id_conductor SET DEFAULT nextval('public.conductor_id_conductor_seq'::regclass);


--
-- Name: direccion_llegada id_direccion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.direccion_llegada ALTER COLUMN id_direccion SET DEFAULT nextval('public.direccion_llegada_id_direccion_seq'::regclass);


--
-- Name: direccion_salida id_direccion_salida; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.direccion_salida ALTER COLUMN id_direccion_salida SET DEFAULT nextval('public.direccion_salida_id_direccion_salida_seq'::regclass);


--
-- Name: documentacion id_documentacion; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documentacion ALTER COLUMN id_documentacion SET DEFAULT nextval('public.documentacion_id_documentacion_seq'::regclass);


--
-- Name: etapa id_etapa; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.etapa ALTER COLUMN id_etapa SET DEFAULT nextval('public.etapa_id_etapa_seq'::regclass);


--
-- Name: nave id_nave; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nave ALTER COLUMN id_nave SET DEFAULT nextval('public.nave_id_nave_seq'::regclass);


--
-- Name: real_time_arribo id_real_time; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.real_time_arribo ALTER COLUMN id_real_time SET DEFAULT nextval('public.real_time_arribo_id_real_time_seq'::regclass);


--
-- Name: real_time_salida id_real_time; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.real_time_salida ALTER COLUMN id_real_time SET DEFAULT nextval('public.real_time_salida_id_real_time_seq'::regclass);


--
-- Name: stock fk_servicio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock ALTER COLUMN fk_servicio SET DEFAULT nextval('public.stock_fk_servicio_seq'::regclass);


--
-- Name: time id_time; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."time" ALTER COLUMN id_time SET DEFAULT nextval('public.time_id_time_seq'::regclass);


--
-- Name: caracteristicas caracteristicas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.caracteristicas
    ADD CONSTRAINT caracteristicas_pkey PRIMARY KEY (id_caracteristicas);


--
-- Name: cliente_despacho cliente_despacho_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente_despacho
    ADD CONSTRAINT cliente_despacho_pkey PRIMARY KEY (id_cliente_despacho);


--
-- Name: cliente_facturacion cliente_facturacion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cliente_facturacion
    ADD CONSTRAINT cliente_facturacion_pkey PRIMARY KEY (id_customer);


--
-- Name: comercial comercial_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comercial
    ADD CONSTRAINT comercial_pkey PRIMARY KEY (id_comercial);


--
-- Name: conductor conductor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.conductor
    ADD CONSTRAINT conductor_pkey PRIMARY KEY (id_conductor);


--
-- Name: direccion_llegada direccion_llegada_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.direccion_llegada
    ADD CONSTRAINT direccion_llegada_pkey PRIMARY KEY (id_direccion);


--
-- Name: direccion_salida direccion_salida_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.direccion_salida
    ADD CONSTRAINT direccion_salida_pkey PRIMARY KEY (id_direccion_salida);


--
-- Name: etapa etapa_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.etapa
    ADD CONSTRAINT etapa_pkey PRIMARY KEY (id_etapa);


--
-- Name: fact_servicios fact_servicios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fact_servicios
    ADD CONSTRAINT fact_servicios_pkey PRIMARY KEY (id);


--
-- Name: facturas facturas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT facturas_pkey PRIMARY KEY (id_factura);


--
-- Name: nave nave_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nave
    ADD CONSTRAINT nave_pkey PRIMARY KEY (id_nave);


--
-- Name: real_time_arribo real_time_arribo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.real_time_arribo
    ADD CONSTRAINT real_time_arribo_pkey PRIMARY KEY (id_real_time);


--
-- Name: real_time_salida real_time_salida_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.real_time_salida
    ADD CONSTRAINT real_time_salida_pkey PRIMARY KEY (id_real_time);


--
-- Name: servicios_documentos servicios_documentos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.servicios_documentos
    ADD CONSTRAINT servicios_documentos_pkey PRIMARY KEY (id);


--
-- Name: stock stock_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.stock
    ADD CONSTRAINT stock_pkey PRIMARY KEY (fk_servicio);


--
-- Name: time time_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."time"
    ADD CONSTRAINT time_pkey PRIMARY KEY (id_time);


--
-- Name: facturas uk_id_factura; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.facturas
    ADD CONSTRAINT uk_id_factura UNIQUE (id_factura);


--
-- Name: documentacion unique_documentacion; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documentacion
    ADD CONSTRAINT unique_documentacion PRIMARY KEY (id_documentacion);


--
-- PostgreSQL database dump complete
--

\unrestrict 2E95D4aUmIRKxeiuIDWgGRU7oTkQY1wN3noQ9HWInOlEEMz3ZcbQiah7T8zb8fp

