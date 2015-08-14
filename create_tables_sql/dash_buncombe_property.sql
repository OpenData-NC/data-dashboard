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
-- Table structure for table `dash_buncombe_property`
--

DROP TABLE IF EXISTS `dash_buncombe_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dash_buncombe_property` (
  `ParcelID` char(15) NOT NULL DEFAULT '',
  `ActiveFlag` char(1) DEFAULT NULL,
  `AccountNum` int(10) unsigned DEFAULT NULL,
  `Owner1_LastName` char(35) DEFAULT NULL,
  `Owner1_FirstName` char(35) DEFAULT NULL,
  `Owner1_ThirdName` char(35) DEFAULT NULL,
  `Owner1_SuffixName` char(4) DEFAULT NULL,
  `Owner2_LastName` char(35) DEFAULT NULL,
  `Owner2_FirstName` char(35) DEFAULT NULL,
  `Owner2_ThirdName` char(35) DEFAULT NULL,
  `Owner2_SuffixName` char(4) DEFAULT NULL,
  `Owner_Address1` char(30) DEFAULT NULL,
  `Owner_Address2` char(30) DEFAULT NULL,
  `Owner_City` char(20) DEFAULT NULL,
  `Owner_State` char(2) DEFAULT NULL,
  `Owner_Zip1` int(10) unsigned DEFAULT NULL,
  `Owner_Zip2` int(10) unsigned DEFAULT NULL,
  `HouseNum` int(10) unsigned DEFAULT NULL,
  `HouseSuffix` char(2) DEFAULT NULL,
  `StreetDirection` char(2) DEFAULT NULL,
  `StreetName` char(20) DEFAULT NULL,
  `StreetType` char(4) DEFAULT NULL,
  `Subdivision` char(35) DEFAULT NULL,
  `SubLot` char(30) DEFAULT NULL,
  `Township` char(2) DEFAULT NULL,
  `CityCode` char(3) DEFAULT NULL,
  `FireCode` char(3) DEFAULT NULL,
  `SchlCode` char(3) DEFAULT NULL,
  `PlatBook` char(4) DEFAULT NULL,
  `PlatPage` char(4) DEFAULT NULL,
  `DeedBook` char(4) DEFAULT NULL,
  `DeedPage` char(4) DEFAULT NULL,
  `DeedDate` date DEFAULT NULL,
  `DeedInstrument` char(3) DEFAULT NULL,
  `Acres` decimal(10,4) DEFAULT NULL,
  `Class` char(20) DEFAULT NULL,
  `Neighborhood` char(20) DEFAULT NULL,
  `LandMarket` int(10) unsigned DEFAULT NULL,
  `BldgMarket` int(10) unsigned DEFAULT NULL,
  `ImprMarket` int(10) unsigned DEFAULT NULL,
  `DfrdMarket` int(10) unsigned DEFAULT NULL,
  `ExemptCode` char(3) DEFAULT NULL,
  `ExemptVal` int(10) unsigned DEFAULT NULL,
  `TaxableVal` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`ParcelID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-08-14 12:15:57
