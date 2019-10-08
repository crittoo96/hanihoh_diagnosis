CREATE DATABASE twi_love;

CREATE TABLE `post` (
  `id` bigint(20) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `tweet_id` varchar(20) NOT NULL,
  `created_at` datetime NOT NULL,
  `message` varchar(32) NOT NULL,
  `species` varchar(10) NOT NULL,
  `sample` varchar(32) NOT NULL,
  `diagnosis` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

alter table post add index created_at_desc (`created_at` desc);
alter table post add unique tweet_id(tweet_id)

CREATE TABLE `post_meta` (
  `id` bigint(20) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `post_id` bigint UNSIGNED not null,
  `name` varchar(32) not null,
  FOREIGN KEY (post_id) REFERENCES post(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

