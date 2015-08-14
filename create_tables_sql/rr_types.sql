-- MySQL dump 10.13  Distrib 5.5.44, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: crime
-- ------------------------------------------------------
-- Server version	5.5.44-0+deb7u1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `rr_types`
--

DROP TABLE IF EXISTS `rr_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rr_types` (
  `type` varchar(100) DEFAULT NULL,
  `id` tinyint(3) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rr_types`
--

LOCK TABLES `rr_types` WRITE;
/*!40000 ALTER TABLE `rr_types` DISABLE KEYS */;
INSERT INTO `rr_types` VALUES ('Restaurant',1),('Food Stand',2),('Mobile Food Unit',3),('Pushcart',4),('Private School Lunch Room',5),('Educational Food Service',6),('Elderly Nutrition Site (catered)',9),('Public School Lunch Room',11),('Elderly Nutrition Site',12),('Limited Food Service',14),('Commissary for Pushcarts & Mobile Food Units',15),('Institutional Food Service',16),('Lodging',20),('Bed and Breakfast Home',21),('Summer Camp',22),('Bed and Breakfast Inn',23),('Primitive Camp',24),('Primitive Camp',25),('Resident Camp',26),('Meat Market',30),('Rest/Nursing Home',40),('Hospital',41),('Child Day Care',42),('Residential Care (excluding Foster Homes)',43),('School Building',44),('Local Confinement',45),('Private Boarding School/College',46),('Orphanage, Children\'s Home or Similar Institution',47),('Adult Day Service',48),('Seasonal Swimming Pool',50),('Seasonal Wading Pool',51),('Seasonal Spa',52),('Year-Round Swimming Pool',53),('Year-Round Wading Pool',54),('Year-Round Spa',55),('Tattoo Parlor',61),('Temporary Food Establishment',73);
/*!40000 ALTER TABLE `rr_types` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-08-14 12:15:57
