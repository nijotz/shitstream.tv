'use strict'
const fs = require('fs')

exports.up = function(knex, Promise) {
  return new Promise((resolve, reject) => {
    fs.readFile('./migrations/init.sql', function(err, sql) {
      if (!err) {
        knex.raw(sql.toString('utf8'))
          .then(resolve, (e) => {
            console.warn("found an init sql file but ran into an error while loading", e)
            setupDb(knex, Promise).then(resolve, reject)
          })
      } else {
        setupDb(knex, Promise).then(resolve, reject)
      }
    })
  })
}

function setupDb(knex, Promise){
  return new Promise((resolve, reject) => {
    knex.raw(setupString).then(resolve, (e) => {
      console.warn('could not set up db', e)
      reject()
    })
  })
}

exports.down = function(knex, Promise) {
  // the shitstream db should be dropped manually in this case
}

// fuck it, just taking the inserts out of the init.sql file i tested on
const setupString = `
  --
  -- PostgreSQL database dump
  --
  
  SET statement_timeout = 0;
  SET lock_timeout = 0;
  SET client_encoding = 'UTF8';
  SET standard_conforming_strings = on;
  SET check_function_bodies = false;
  SET client_min_messages = warning;
  
  --
  -- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
  --
  
  CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
  
  
  --
  -- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
  --
  
  COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
  
  
  SET search_path = public, pg_catalog;
  
  SET default_tablespace = '';
  
  SET default_with_oids = false;
  
  --
  -- Name: played; Type: TABLE; Schema: public; Owner: shitstream; Tablespace: 
  --
  
  CREATE TABLE played (
      id integer NOT NULL,
      created_at timestamp without time zone,
      updated_at timestamp without time zone,
      video_id integer
  );
  
  
  ALTER TABLE public.played OWNER TO shitstream;
  
  --
  -- Name: played_id_seq; Type: SEQUENCE; Schema: public; Owner: shitstream
  --
  
  CREATE SEQUENCE played_id_seq
      START WITH 1
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      CACHE 1;
  
  
  ALTER TABLE public.played_id_seq OWNER TO shitstream;
  
  --
  -- Name: played_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shitstream
  --
  
  ALTER SEQUENCE played_id_seq OWNED BY played.id;
  
  
  --
  -- Name: queue; Type: TABLE; Schema: public; Owner: shitstream; Tablespace: 
  --
  
  CREATE TABLE queue (
      created_at timestamp without time zone,
      updated_at timestamp without time zone,
      id integer NOT NULL,
      number integer,
      video_id integer
  );
  
  
  ALTER TABLE public.queue OWNER TO shitstream;
  
  --
  -- Name: queue_id_seq; Type: SEQUENCE; Schema: public; Owner: shitstream
  --
  
  CREATE SEQUENCE queue_id_seq
      START WITH 1
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      CACHE 1;
  
  
  ALTER TABLE public.queue_id_seq OWNER TO shitstream;
  
  --
  -- Name: queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shitstream
  --
  
  ALTER SEQUENCE queue_id_seq OWNED BY queue.id;
  
  
  --
  -- Name: video; Type: TABLE; Schema: public; Owner: shitstream; Tablespace: 
  --
  
  CREATE TABLE video (
      created_at timestamp without time zone,
      updated_at timestamp without time zone,
      id integer NOT NULL,
      filename text,
      origin text,
      key text
  );
  
  
  ALTER TABLE public.video OWNER TO shitstream;
  
  --
  -- Name: video_id_seq; Type: SEQUENCE; Schema: public; Owner: shitstream
  --
  
  CREATE SEQUENCE video_id_seq
      START WITH 1
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      CACHE 1;
  
  
  ALTER TABLE public.video_id_seq OWNER TO shitstream;
  
  --
  -- Name: video_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shitstream
  --
  
  ALTER SEQUENCE video_id_seq OWNED BY video.id;
  
  
  --
  -- Name: weight; Type: TABLE; Schema: public; Owner: shitstream; Tablespace: 
  --
  
  CREATE TABLE weight (
      id integer NOT NULL,
      created_at timestamp without time zone,
      updated_at timestamp without time zone,
      video_id integer,
      weight integer
  );
  
  
  ALTER TABLE public.weight OWNER TO shitstream;
  
  --
  -- Name: weight_id_seq; Type: SEQUENCE; Schema: public; Owner: shitstream
  --
  
  CREATE SEQUENCE weight_id_seq
      START WITH 1
      INCREMENT BY 1
      NO MINVALUE
      NO MAXVALUE
      CACHE 1;
  
  
  ALTER TABLE public.weight_id_seq OWNER TO shitstream;
  
  --
  -- Name: weight_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: shitstream
  --
  
  ALTER SEQUENCE weight_id_seq OWNED BY weight.id;
  
  
  --
  -- Name: id; Type: DEFAULT; Schema: public; Owner: shitstream
  --
  
  ALTER TABLE ONLY played ALTER COLUMN id SET DEFAULT nextval('played_id_seq'::regclass);
  
  
  --
  -- Name: id; Type: DEFAULT; Schema: public; Owner: shitstream
  --
  
  ALTER TABLE ONLY queue ALTER COLUMN id SET DEFAULT nextval('queue_id_seq'::regclass);
  
  
  --
  -- Name: id; Type: DEFAULT; Schema: public; Owner: shitstream
  --
  
  ALTER TABLE ONLY video ALTER COLUMN id SET DEFAULT nextval('video_id_seq'::regclass);
  
  
  --
  -- Name: id; Type: DEFAULT; Schema: public; Owner: shitstream
  --
  
  ALTER TABLE ONLY weight ALTER COLUMN id SET DEFAULT nextval('weight_id_seq'::regclass);
  
  --
  -- Name: played_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shitstream
  --
  
  SELECT pg_catalog.setval('played_id_seq', 1, true);
  
  --
  -- Name: queue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shitstream
  --
  
  SELECT pg_catalog.setval('queue_id_seq', 1, false);
  
  
  --
  -- Name: video_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shitstream
  --
  
  SELECT pg_catalog.setval('video_id_seq', 1, true);
  
  --
  -- Name: weight_id_seq; Type: SEQUENCE SET; Schema: public; Owner: shitstream
  --
  
  SELECT pg_catalog.setval('weight_id_seq', 1, true);
  
  
  --
  -- Name: played_pkey; Type: CONSTRAINT; Schema: public; Owner: shitstream; Tablespace: 
  --
  
  ALTER TABLE ONLY played
      ADD CONSTRAINT played_pkey PRIMARY KEY (id);
  
  
  --
  -- Name: queue_pkey; Type: CONSTRAINT; Schema: public; Owner: shitstream; Tablespace: 
  --
  
  ALTER TABLE ONLY queue
      ADD CONSTRAINT queue_pkey PRIMARY KEY (id);
  
  
  --
  -- Name: video_pkey; Type: CONSTRAINT; Schema: public; Owner: shitstream; Tablespace: 
  --
  
  ALTER TABLE ONLY video
      ADD CONSTRAINT video_pkey PRIMARY KEY (id);
  
  
  --
  -- Name: weight_pkey; Type: CONSTRAINT; Schema: public; Owner: shitstream; Tablespace: 
  --
  
  ALTER TABLE ONLY weight
      ADD CONSTRAINT weight_pkey PRIMARY KEY (id);
  
  
  --
  -- Name: played_video_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shitstream
  --
  
  ALTER TABLE ONLY played
      ADD CONSTRAINT played_video_id_fkey FOREIGN KEY (video_id) REFERENCES video(id);
  
  
  --
  -- Name: queue_video_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shitstream
  --
  
  ALTER TABLE ONLY queue
      ADD CONSTRAINT queue_video_id_fkey FOREIGN KEY (video_id) REFERENCES video(id);
  
  
  --
  -- Name: weight_video_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: shitstream
  --
  
  ALTER TABLE ONLY weight
      ADD CONSTRAINT weight_video_id_fkey FOREIGN KEY (video_id) REFERENCES video(id);
  
  
  --
  -- Name: public; Type: ACL; Schema: -; Owner: postgres
  --
  
  REVOKE ALL ON SCHEMA public FROM PUBLIC;
  REVOKE ALL ON SCHEMA public FROM postgres;
  GRANT ALL ON SCHEMA public TO postgres;
  GRANT ALL ON SCHEMA public TO PUBLIC;
  
  
  --
  -- PostgreSQL database dump complete
  --
`
