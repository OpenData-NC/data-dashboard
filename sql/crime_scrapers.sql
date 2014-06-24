-- MySQL dump 10.13  Distrib 5.5.37, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: crime
-- ------------------------------------------------------
-- Server version	5.5.37-0ubuntu0.12.04.1

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
-- Table structure for table `accidents`
--

DROP TABLE IF EXISTS `accidents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accidents` (
  `record_id` varchar(100) NOT NULL,
  `agency` varchar(150) NOT NULL,
  `name1` varchar(250) DEFAULT NULL,
  `name2` varchar(250) DEFAULT NULL,
  `occurred_date` datetime DEFAULT NULL,
  `date_occurred` date DEFAULT NULL,
  `time_date` time DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `reporting_officer` varchar(250) DEFAULT NULL,
  `pdf` varchar(250) DEFAULT NULL,
  `street_address` varchar(250) DEFAULT NULL,
  `city` varchar(250) DEFAULT NULL,
  `county` varchar(100) DEFAULT NULL,
  `state` char(3) DEFAULT 'NC',
  `zip` int(10) unsigned DEFAULT NULL,
  `lat` float(14,11) DEFAULT NULL,
  `lon` float(14,11) DEFAULT NULL,
  `scrape_type` char(10) NOT NULL,
  `id_generate` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`record_id`,`agency`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accidents`
--

LOCK TABLES `accidents` WRITE;
/*!40000 ALTER TABLE `accidents` DISABLE KEYS */;
/*!40000 ALTER TABLE `accidents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `arrests`
--

DROP TABLE IF EXISTS `arrests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `arrests` (
  `record_id` varchar(100) NOT NULL,
  `agency` varchar(150) NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `age` tinyint(4) DEFAULT NULL,
  `race` char(3) DEFAULT NULL,
  `sex` char(3) DEFAULT NULL,
  `occurred_date` datetime DEFAULT NULL,
  `date_occurred` date DEFAULT NULL,
  `time_date` time DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `charge` varchar(250) DEFAULT NULL,
  `offense_code` char(3) DEFAULT NULL,
  `reporting_officer` varchar(250) DEFAULT NULL,
  `pdf` varchar(250) DEFAULT NULL,
  `street_address` varchar(250) DEFAULT NULL,
  `city` varchar(250) DEFAULT NULL,
  `county` varchar(100) DEFAULT NULL,
  `state` char(3) DEFAULT 'NC',
  `zip` int(10) unsigned DEFAULT NULL,
  `lat` float(14,11) DEFAULT NULL,
  `lon` float(14,11) DEFAULT NULL,
  `scrape_type` char(10) NOT NULL,
  `id_generate` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`record_id`,`agency`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arrests`
--

LOCK TABLES `arrests` WRITE;
/*!40000 ALTER TABLE `arrests` DISABLE KEYS */;
/*!40000 ALTER TABLE `arrests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `citations`
--

DROP TABLE IF EXISTS `citations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `citations` (
  `record_id` varchar(100) NOT NULL,
  `agency` varchar(150) NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `age` tinyint(4) DEFAULT NULL,
  `race` char(3) DEFAULT NULL,
  `sex` char(3) DEFAULT NULL,
  `occurred_date` datetime DEFAULT NULL,
  `date_occurred` date DEFAULT NULL,
  `time_date` time DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `charge` varchar(250) DEFAULT NULL,
  `offense_code` char(3) DEFAULT NULL,
  `reporting_officer` varchar(250) DEFAULT NULL,
  `pdf` varchar(250) DEFAULT NULL,
  `street_address` varchar(250) DEFAULT NULL,
  `city` varchar(250) DEFAULT NULL,
  `county` varchar(100) DEFAULT NULL,
  `state` char(3) DEFAULT 'NC',
  `zip` int(10) unsigned DEFAULT NULL,
  `lat` float(14,11) DEFAULT NULL,
  `lon` float(14,11) DEFAULT NULL,
  `scrape_type` char(10) NOT NULL,
  `id_generate` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`record_id`,`agency`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `citations`
--

LOCK TABLES `citations` WRITE;
/*!40000 ALTER TABLE `citations` DISABLE KEYS */;
/*!40000 ALTER TABLE `citations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incidents`
--

DROP TABLE IF EXISTS `incidents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `incidents` (
  `record_id` varchar(100) NOT NULL,
  `agency` varchar(150) NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `age` tinyint(4) DEFAULT NULL,
  `race` char(3) DEFAULT NULL,
  `sex` char(3) DEFAULT NULL,
  `on_date` datetime DEFAULT NULL,
  `from_date` datetime DEFAULT NULL,
  `to_date` datetime DEFAULT NULL,
  `address` varchar(250) DEFAULT NULL,
  `charge` varchar(250) DEFAULT NULL,
  `offense_code` char(3) DEFAULT NULL,
  `reporting_officer` varchar(250) DEFAULT NULL,
  `pdf` varchar(250) DEFAULT NULL,
  `street_address` varchar(250) DEFAULT NULL,
  `city` varchar(250) DEFAULT NULL,
  `county` varchar(100) DEFAULT NULL,
  `state` char(3) DEFAULT 'NC',
  `zip` int(10) unsigned DEFAULT NULL,
  `lat` float(14,11) DEFAULT NULL,
  `lon` float(14,11) DEFAULT NULL,
  `scrape_type` char(10) NOT NULL,
  `id_generate` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`record_id`,`agency`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incidents`
--

LOCK TABLES `incidents` WRITE;
/*!40000 ALTER TABLE `incidents` DISABLE KEYS */;
/*!40000 ALTER TABLE `incidents` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-06-24 14:46:57
