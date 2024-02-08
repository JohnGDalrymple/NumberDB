/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : PostgreSQL
 Source Server Version : 140005 (140005)
 Source Host           : localhost:5432
 Source Catalog        : number_db
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 140005 (140005)
 File Encoding         : 65001

 Date: 08/02/2024 00:54:23
*/


-- ----------------------------
-- Table structure for assist_dids_voice_carrier
-- ----------------------------
DROP TABLE IF EXISTS "public"."assist_dids_voice_carrier";
CREATE TABLE "public"."assist_dids_voice_carrier" (
  "id" int8 NOT NULL GENERATED BY DEFAULT AS IDENTITY (
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1
),
  "name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "description" varchar(200) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of assist_dids_voice_carrier
-- ----------------------------
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (1, '9296956331', '9296956331');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (2, '9296956332', '9296956332');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (3, '9296956334', '9296956334');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (4, '?', '?');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (5, 'Bandwidth', 'Bandwidth');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (6, 'Disco', 'Disco');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (7, 'INTQ', 'INTQ');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (8, 'INTQ - OC', 'INTQ - OC');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (9, 'INTQ - Wholesale', 'INTQ - Wholesale');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (10, 'Orphan', 'Orphan');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (11, 'Teli', 'Teli');
INSERT INTO "public"."assist_dids_voice_carrier" VALUES (12, 'Twilio', 'Twilio');

-- ----------------------------
-- Auto increment value for assist_dids_voice_carrier
-- ----------------------------
SELECT setval('"public"."assist_dids_voice_carrier_id_seq"', 13, true);

-- ----------------------------
-- Indexes structure for table assist_dids_voice_carrier
-- ----------------------------
CREATE INDEX "assist_dids_voice_carrier_name_6cd4471a_like" ON "public"."assist_dids_voice_carrier" USING btree (
  "name" COLLATE "pg_catalog"."default" "pg_catalog"."varchar_pattern_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table assist_dids_voice_carrier
-- ----------------------------
ALTER TABLE "public"."assist_dids_voice_carrier" ADD CONSTRAINT "assist_dids_voice_carrier_name_key" UNIQUE ("name");

-- ----------------------------
-- Primary Key structure for table assist_dids_voice_carrier
-- ----------------------------
ALTER TABLE "public"."assist_dids_voice_carrier" ADD CONSTRAINT "assist_dids_voice_carrier_pkey" PRIMARY KEY ("id");
