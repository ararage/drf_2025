-- SQL Manual id to UUID

-- Remove field id from reviews
--
CREATE TABLE "new__watchlist_app_reviews" ("uuid" char(32) NOT NULL PRIMARY KEY, "created" datetime NOT NULL, "modified" datetime NOT NULL, "active" bool NOT NULL, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "description" varchar(200) NULL, "watchlist_id" char(32) NULL REFERENCES "watchlist_app_watchlist" ("uuid") DEFERRABLE INITIALLY DEFERRED);

INSERT INTO "new__watchlist_app_reviews" ("uuid", "created", "modified", "active", "rating", "description", "watchlist_id") SELECT 
lower(
    hex(randomblob(4)) || '-' ||
    hex(randomblob(2)) || '-4' ||
    substr(hex(randomblob(2)), 2) || '-' ||
    substr('89ab', 1 + (abs(random()) % 4) , 1) ||
    substr(hex(randomblob(2)), 2) || '-' ||
    hex(randomblob(6))
) AS "uuid",
"created", "modified", "active", "rating", "description", "watchlist_id" FROM "watchlist_app_reviews";

DROP TABLE "watchlist_app_reviews";
ALTER TABLE "new__watchlist_app_reviews" RENAME TO "watchlist_app_reviews";
CREATE INDEX "watchlist_app_reviews_watchlist_id_4d024ddd" ON "watchlist_app_reviews" ("watchlist_id");

--
-- Add field uuid to reviews
--
CREATE TABLE "new__watchlist_app_reviews" ("uuid" char(32) NOT NULL PRIMARY KEY, "created" datetime NOT NULL, "modified" datetime NOT NULL, "active" bool NOT NULL, "rating" integer unsigned NOT NULL CHECK ("rating" >= 0), "description" varchar(200) NULL, "watchlist_id" char(32) NULL REFERENCES "watchlist_app_watchlist" ("uuid") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__watchlist_app_reviews" ("created", "modified", "active", "rating", "description", "watchlist_id", "uuid") SELECT "created", "modified", "active", "rating", "description", "watchlist_id", '747564c0c55c428c9c0337416649c7c3' FROM "watchlist_app_reviews";
DROP TABLE "watchlist_app_reviews";
ALTER TABLE "new__watchlist_app_reviews" RENAME TO "watchlist_app_reviews";
CREATE INDEX "watchlist_app_reviews_watchlist_id_4d024ddd" ON "watchlist_app_reviews" ("watchlist_id");
COMMIT;