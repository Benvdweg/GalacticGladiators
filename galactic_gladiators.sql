-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: galactic_gladiators
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `game_units`
--

DROP TABLE IF EXISTS `game_units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game_units` (
  `game_unit_id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `player_id` int(11) NOT NULL,
  `unit_id` int(11) DEFAULT NULL,
  `has_used_power` tinyint(1) NOT NULL DEFAULT 0,
  `rank` int(11) NOT NULL,
  `is_friendly` tinyint(1) NOT NULL,
  `is_defeated` tinyint(1) DEFAULT 0,
  `captured_at_turn` int(11) DEFAULT NULL,
  PRIMARY KEY (`game_unit_id`),
  UNIQUE KEY `game_unit_id` (`game_unit_id`),
  KEY `game_id` (`game_id`),
  KEY `player_id` (`player_id`),
  KEY `unit_id` (`unit_id`),
  CONSTRAINT `game_units_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `game_units_ibfk_2` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `game_units_ibfk_3` FOREIGN KEY (`unit_id`) REFERENCES `units` (`unit_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9970 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_units`
--

LOCK TABLES `game_units` WRITE;
/*!40000 ALTER TABLE `game_units` DISABLE KEYS */;
/*!40000 ALTER TABLE `game_units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `games`
--

DROP TABLE IF EXISTS `games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `games` (
  `game_id` int(11) NOT NULL AUTO_INCREMENT,
  `has_started` tinyint(1) NOT NULL DEFAULT 0,
  `has_ended` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL,
  `current_turn` int(11) DEFAULT NULL,
  `selected_unit_square_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE KEY `game_id` (`game_id`)
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `games`
--

LOCK TABLES `games` WRITE;
/*!40000 ALTER TABLE `games` DISABLE KEYS */;
/*!40000 ALTER TABLE `games` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `players`
--

DROP TABLE IF EXISTS `players`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `players` (
  `player_id` int(11) NOT NULL AUTO_INCREMENT,
  `nickname` mediumtext NOT NULL,
  `is_bot` tinyint(1) NOT NULL,
  `score` int(11) NOT NULL DEFAULT 0,
  `game_id` int(11) NOT NULL,
  PRIMARY KEY (`player_id`),
  UNIQUE KEY `player_id` (`player_id`),
  KEY `game_id` (`game_id`),
  CONSTRAINT `players_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=698 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `special_powers_log`
--

DROP TABLE IF EXISTS `special_powers_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `special_powers_log` (
  `special_power_id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `game_unit_id` int(11) NOT NULL,
  `power` int(11) DEFAULT NULL,
  `turn_number` int(11) NOT NULL,
  `is_visible` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`special_power_id`),
  UNIQUE KEY `special_power_id` (`special_power_id`),
  KEY `game_id` (`game_id`),
  KEY `game_unit_id` (`game_unit_id`),
  KEY `fk_power` (`power`),
  CONSTRAINT `fk_power` FOREIGN KEY (`power`) REFERENCES `units` (`unit_id`),
  CONSTRAINT `special_powers_log_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `special_powers_log_ibfk_2` FOREIGN KEY (`game_unit_id`) REFERENCES `game_units` (`game_unit_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `special_powers_log`
--

LOCK TABLES `special_powers_log` WRITE;
/*!40000 ALTER TABLE `special_powers_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `special_powers_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `square_logs`
--

DROP TABLE IF EXISTS `square_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `square_logs` (
  `square_log_id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `game_unit_id` int(11) NOT NULL,
  `square_type` text DEFAULT NULL,
  `turn_number` int(11) NOT NULL,
  `square_id` int(11) NOT NULL,
  PRIMARY KEY (`square_log_id`),
  UNIQUE KEY `square_log_id` (`square_log_id`),
  KEY `game_id` (`game_id`),
  KEY `game_unit_id` (`game_unit_id`),
  KEY `fk_square_logs_squares` (`square_id`),
  CONSTRAINT `fk_square_logs_squares` FOREIGN KEY (`square_id`) REFERENCES `squares` (`square_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `square_logs_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `square_logs_ibfk_2` FOREIGN KEY (`game_unit_id`) REFERENCES `game_units` (`game_unit_id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=251 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `square_logs`
--

LOCK TABLES `square_logs` WRITE;
/*!40000 ALTER TABLE `square_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `square_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `squares`
--

DROP TABLE IF EXISTS `squares`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `squares` (
  `square_id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `position_x` int(11) NOT NULL,
  `position_y` int(11) NOT NULL,
  `square_type` varchar(20) DEFAULT NULL,
  `unit_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`square_id`),
  UNIQUE KEY `square_id` (`square_id`),
  KEY `unit_id` (`unit_id`),
  KEY `fk_squares_game` (`game_id`),
  CONSTRAINT `fk_squares_game` FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `squares_ibfk_2` FOREIGN KEY (`unit_id`) REFERENCES `game_units` (`game_unit_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=34702 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `squares`
--

LOCK TABLES `squares` WRITE;
/*!40000 ALTER TABLE `squares` DISABLE KEYS */;
/*!40000 ALTER TABLE `squares` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `units`
--

DROP TABLE IF EXISTS `units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `units` (
  `unit_id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(20) NOT NULL,
  `special_power` varchar(50) NOT NULL,
  PRIMARY KEY (`unit_id`),
  UNIQUE KEY `unit_id` (`unit_id`),
  UNIQUE KEY `type` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `units`
--

LOCK TABLES `units` WRITE;
/*!40000 ALTER TABLE `units` DISABLE KEYS */;
INSERT INTO `units` VALUES (1,'Verkenner','Infiltratie'),(2,'Infanterist','Geen'),(3,'Scherpschutter','Precisieschot'),(4,'Schilddrager','Energieveld'),(5,'Strijdmeester','Strijdkreet'),(6,'Commando','Sabotage'),(7,'Vlag','Geen');
/*!40000 ALTER TABLE `units` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-12 19:57:13
