BEGIN;
CREATE TABLE `customercare_tweet` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tweet_id` bigint NOT NULL,
    `raw_json` longtext NOT NULL,
    `created` datetime NOT NULL
)
;
CREATE INDEX `customercare_tweet_3216ff68` ON `customercare_tweet` (`created`);
COMMIT;
