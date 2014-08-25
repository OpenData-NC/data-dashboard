-- MySQL dump 10.13  Distrib 5.6.17, for Win32 (x86)
--
-- Host: localhost    Database: crime
-- ------------------------------------------------------
-- Server version	5.6.20

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
-- Table structure for table `agency_county`
--

DROP TABLE IF EXISTS `agency_county`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agency_county` (
  `agency` varchar(100) NOT NULL,
  `county` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`agency`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agency_county`
--

LOCK TABLES `agency_county` WRITE;
/*!40000 ALTER TABLE `agency_county` DISABLE KEYS */;
INSERT INTO `agency_county` VALUES ('Asheville Police Department','Buncombe'),('Buncombe County Sheriff\'s Office','Buncombe'),('Burke County Sheriff\'s Office','Burke'),('Chapel Hill Police Department','Orange'),('Cleveland County Sheriff\'s Office','Cleveland'),('Concord Police Department','Cabarrus'),('Forsyth County Sheriff\'s Office','Forsyth'),('Greensboro Police Department','Guilford'),('Hickory Police Department','Catawba'),('High Point Police Department','Guilford'),('Huntersville Police Department','Mecklenburg'),('Kannapolis Police Department','Cabarrus'),('Kernersville Police Department','Forsyth'),('Lenoir Police Department','Caldwell'),('Lexington County Police Department','Davidson'),('Lincoln County Sheriff\'s Office','Lincoln'),('Rocky Mount Police Department','Edgecombe'),('Rowan County Sheriff\'s Office','Rowan'),('Sanford Police Department','Lee'),('Union County Sheriff\'s Office','Union'),('Wake County Sheriff\'s Office','Wake'),('Wake Forest Police Department','Franklin'),('Wilmington Police Department','New Hanover'),('Wilson County Sheriff\'s Office','Wilson'),('Winston-Salem Police Department','Forsyth');
/*!40000 ALTER TABLE `agency_county` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-08-25 15:35:53
