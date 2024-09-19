/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.5.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: game_test
-- ------------------------------------------------------
-- Server version	11.5.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `user_inventory`
--

DROP TABLE IF EXISTS `user_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_inventory` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `owner` bigint(20) unsigned NOT NULL,
  `code` varchar(4) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL,
  `retail` tinyint(1) NOT NULL DEFAULT 0,
  `startdate` int(10) unsigned NOT NULL,
  `leasing_seconds` int(10) unsigned NOT NULL,
  `price` int(10) unsigned NOT NULL,
  `price_cash` int(10) unsigned NOT NULL DEFAULT 0,
  `expired` tinyint(1) NOT NULL DEFAULT 0,
  `deleted` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `fk_user_inventory_user` (`owner`),
  CONSTRAINT `fk_user_inventory_user` FOREIGN KEY (`owner`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_loadout`
--

DROP TABLE IF EXISTS `user_loadout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_loadout` (
  `id` bigint(20) unsigned NOT NULL,
  `engineer` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL DEFAULT 'DA02,DB01,DF01,DR01,^,^,^,^',
  `medic` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL DEFAULT 'DA02,DB01,DF01,DQ01,^,^,^,^',
  `sniper` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL DEFAULT 'DA02,DB01,DG05,DN01,^,^,^,^',
  `assault` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL DEFAULT 'DA02,DB01,DC02,DN01,^,^,^,^',
  `heavy_trooper` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL DEFAULT 'DA02,DB01,DJ01,DL01,^,^,^,^',
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_user_loadout_user` FOREIGN KEY (`id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_stats`
--

DROP TABLE IF EXISTS `user_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_stats` (
  `id` bigint(20) unsigned NOT NULL,
  `kills` bigint(20) unsigned NOT NULL DEFAULT 0,
  `deaths` bigint(20) unsigned NOT NULL DEFAULT 0,
  `headshots` bigint(20) unsigned NOT NULL DEFAULT 0,
  `bombs_planted` bigint(20) unsigned NOT NULL DEFAULT 0,
  `bombs_defused` bigint(20) unsigned NOT NULL DEFAULT 0,
  `rounds_played` bigint(20) unsigned NOT NULL DEFAULT 0,
  `flags_taken` bigint(20) unsigned NOT NULL DEFAULT 0,
  `victories` bigint(20) unsigned NOT NULL DEFAULT 0,
  `defeats` bigint(20) unsigned NOT NULL DEFAULT 0,
  `vehicles_destroyed` bigint(20) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_user_stats_user` FOREIGN KEY (`id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `xp` bigint(20) unsigned NOT NULL DEFAULT 0,
  `money` int(10) unsigned NOT NULL DEFAULT 30000,
  `premium` tinyint(3) unsigned DEFAULT 0,
  `premium_expiredate` bigint(20) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-09-19 17:27:37
