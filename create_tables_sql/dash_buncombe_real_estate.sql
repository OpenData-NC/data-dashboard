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
-- Table structure for table `dash_buncombe_real_estate`
--

DROP TABLE IF EXISTS `dash_buncombe_real_estate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dash_buncombe_real_estate` (
  `ParcelID` char(15) DEFAULT NULL,
  `ActiveStatus` char(1) DEFAULT NULL,
  `SellDate` date DEFAULT NULL,
  `SellNum` int(10) unsigned DEFAULT NULL,
  `Seller_Acct` int(10) unsigned DEFAULT NULL,
  `Seller1_Lname` char(35) DEFAULT NULL,
  `Seller1_Fname` char(35) DEFAULT NULL,
  `Seller1_Tname` char(35) DEFAULT NULL,
  `Seller1_Sufname` char(4) DEFAULT NULL,
  `Seller2_Lname` char(35) DEFAULT NULL,
  `Seller2_Fname` char(35) DEFAULT NULL,
  `Seller2_Tname` char(35) DEFAULT NULL,
  `Seller2_Sufname` char(4) DEFAULT NULL,
  `Seller_Address1` char(30) DEFAULT NULL,
  `Seller_Address2` char(30) DEFAULT NULL,
  `Seller_City` char(20) DEFAULT NULL,
  `Seller_State` char(2) DEFAULT NULL,
  `Seller_Zip1` char(10) DEFAULT NULL,
  `Seller_Zip2` char(10) DEFAULT NULL,
  `Buyer_Acct` int(10) unsigned DEFAULT NULL,
  `Buyer1_Lname` char(35) DEFAULT NULL,
  `Buyer1_Fname` char(35) DEFAULT NULL,
  `Buyer1_Tname` char(35) DEFAULT NULL,
  `Buyer1_Sufname` char(4) DEFAULT NULL,
  `Buyer2_Lname` char(35) DEFAULT NULL,
  `Buyer2_Fname` char(35) DEFAULT NULL,
  `Buyer2_Tname` char(35) DEFAULT NULL,
  `Buyer2_Sufname` char(4) DEFAULT NULL,
  `Buyer_Address1` char(30) DEFAULT NULL,
  `Buyer_Address2` char(30) DEFAULT NULL,
  `Buyer_City` char(20) DEFAULT NULL,
  `Buyer_State` char(2) DEFAULT NULL,
  `Buyer_Zip1` char(10) DEFAULT NULL,
  `Buyer_Zip2` char(10) DEFAULT NULL,
  `Subdivision` char(35) DEFAULT NULL,
  `SubLot` char(30) DEFAULT NULL,
  `HouseNum` int(10) unsigned DEFAULT NULL,
  `HouseSuffix` char(2) DEFAULT NULL,
  `StreetDirection` char(2) DEFAULT NULL,
  `StreetName` char(20) DEFAULT NULL,
  `StreetType` char(4) DEFAULT NULL,
  `Township` char(2) DEFAULT NULL,
  `CityCode` char(3) DEFAULT NULL,
  `FireCode` char(3) DEFAULT NULL,
  `SchlCode` char(3) DEFAULT NULL,
  `PlatBook` char(4) DEFAULT NULL,
  `PlatPage` char(4) DEFAULT NULL,
  `DeedBook` char(4) DEFAULT NULL,
  `DeedPage` char(4) DEFAULT NULL,
  `DeedDate` date DEFAULT NULL,
  `DeedInstument` char(3) DEFAULT NULL,
  `Acres` decimal(10,4) DEFAULT NULL,
  `Class` char(20) DEFAULT NULL,
  `Neighborhood` char(20) DEFAULT NULL,
  `SellingPrice` decimal(20,2) DEFAULT NULL,
  `QualifiedSale` char(1) DEFAULT NULL,
  `VacantLot` char(1) DEFAULT NULL
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
