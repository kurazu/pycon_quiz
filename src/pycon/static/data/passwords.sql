PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "auth_group" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
);
CREATE TABLE "auth_group_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("group_id", "permission_id")
);
CREATE TABLE "auth_message" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "message" text NOT NULL
);
CREATE TABLE "auth_permission" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
);
CREATE TABLE "auth_user" (
    "id" integer NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "is_superuser" bool NOT NULL,
    "last_login" datetime NOT NULL,
    "date_joined" datetime NOT NULL
);
INSERT INTO "auth_user" VALUES(1,'john','John','Snow','bastard@example.com','sha1$zbwDv$a90d2337b244dc7dc733329d13dc65a5e714d687',0,1,0,'2013-05-04 13:52:15','2012-07-21 16:01:13');
INSERT INTO "auth_user" VALUES(2,'arya','Arya','Stark','arry@example.com','sha1$8E2Xu$30e26708e4b6ad3d9ee819a00f4e45b2ee204d29',0,1,0,'2013-09-21 05:10:34','2012-08-07 13:04:45');
INSERT INTO "auth_user" VALUES(3,'joffrey','Joffrey','Lannister','joff@example.com','sha1$Ac9Qp$459fbd8f51190ee9e690a67e5be444aefe2e3b1e',0,1,0,'2013-09-06 10:31:29','2012-06-21 00:35:46');
INSERT INTO "auth_user" VALUES(4,'tyrion','Tyrion','Lannister','tyrion@example.com','sha1$5jqu0$3449a78b0ca95d6b8bf71e6784a8132a75194fee',0,1,0,'2013-09-06 06:16:13','2012-01-12 15:55:12');
INSERT INTO "auth_user" VALUES(5,'brienne','Brienne','of Tarth','brienne@example.com','sha1$1d97F$37b99c45c42127f54b5ea9f6b4ed7a3595f81f65',0,1,0,'2013-08-12 12:41:40','2012-09-24 14:27:46');
INSERT INTO "auth_user" VALUES(6,'gregor','Gregor','Clegane','gregor@example.com','sha1$BB6DG$5916747a47932b0a9cdabcae4529e9dd77c9c2d2',0,1,0,'2013-02-17 01:20:02','2012-03-10 14:11:31');
INSERT INTO "auth_user" VALUES(7,'admin','Mance','Ryder','kingbeyondthewall@example.com','sha1$bh9ul$8e808fcea5418aa971311ea1598df65627ea3b98',1,1,1,'2013-08-02 01:54:16','2012-02-16 04:51:09');
CREATE TABLE "auth_user_groups" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    UNIQUE ("user_id", "group_id")
);
CREATE TABLE "auth_user_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("user_id", "permission_id")
);
CREATE TABLE "django_admin_log" (
    "id" integer NOT NULL PRIMARY KEY,
    "action_time" datetime NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "content_type_id" integer REFERENCES "django_content_type" ("id"),
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint unsigned NOT NULL,
    "change_message" text NOT NULL
);
CREATE TABLE "django_content_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
);
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" datetime NOT NULL
);
CREATE TABLE "django_site" (
    "id" integer NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
);
CREATE INDEX "auth_group_permissions_1e014c8f" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_group_permissions_425ae3c4" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_message_403f60f" ON "auth_message" ("user_id");
CREATE INDEX "auth_permission_1bb8f392" ON "auth_permission" ("content_type_id");
CREATE INDEX "auth_user_groups_403f60f" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_425ae3c4" ON "auth_user_groups" ("group_id");
CREATE INDEX "auth_user_user_permissions_1e014c8f" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "auth_user_user_permissions_403f60f" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "django_admin_log_1bb8f392" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_403f60f" ON "django_admin_log" ("user_id");
CREATE INDEX "django_session_3da3d3d8" ON "django_session" ("expire_date");
COMMIT;
