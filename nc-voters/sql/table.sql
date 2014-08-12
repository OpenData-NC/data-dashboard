-- MySQL dump 10.13  Distrib 5.5.38, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: crime
-- ------------------------------------------------------
-- Server version	5.5.38-0+wheezy1

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
-- Table structure for table `nc_voters`
--

DROP TABLE IF EXISTS `nc_voters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nc_voters` (
  `county_id` tinyint(3) unsigned NOT NULL,
  `county_desc` varchar(50) DEFAULT NULL,
  `voter_reg_num` char(12) NOT NULL,
  `status_cd` char(2) DEFAULT NULL,
  `voter_status_desc` varchar(25) DEFAULT NULL,
  `reason_cd` char(2) DEFAULT NULL,
  `voter_status_reason_desc` varchar(60) DEFAULT NULL,
  `absent_ind` char(1) DEFAULT NULL,
  `name_prefx_cd` char(4) DEFAULT NULL,
  `last_name` char(25) DEFAULT NULL,
  `first_name` char(20) DEFAULT NULL,
  `midl_name` char(20) DEFAULT NULL,
  `name_sufx_cd` char(3) DEFAULT NULL,
  `res_street_address` varchar(250) DEFAULT NULL,
  `res_city_desc` varchar(60) DEFAULT NULL,
  `state_cd` char(2) DEFAULT NULL,
  `zip_code` char(9) DEFAULT NULL,
  `mail_addr1` varchar(250) DEFAULT NULL,
  `mail_addr2` varchar(40) DEFAULT NULL,
  `mail_addr3` varchar(40) DEFAULT NULL,
  `mail_addr4` varchar(40) DEFAULT NULL,
  `mail_city` varchar(30) DEFAULT NULL,
  `mail_state` char(2) DEFAULT NULL,
  `mail_zipcode` char(9) DEFAULT NULL,
  `full_phone_number` int(10) unsigned DEFAULT '0',
  `race_code` char(3) DEFAULT NULL,
  `ethnic_code` char(3) DEFAULT NULL,
  `party_cd` char(3) DEFAULT NULL,
  `gender_code` varchar(1) DEFAULT NULL,
  `birth_age` tinyint(3) unsigned DEFAULT NULL,
  `birth_place` char(30) DEFAULT NULL,
  `registr_dt` char(10) DEFAULT NULL,
  `precinct_abbrv` char(6) DEFAULT NULL,
  `precinct_desc` varchar(60) DEFAULT NULL,
  `municipality_abbrv` char(6) DEFAULT NULL,
  `municipality_desc` varchar(60) DEFAULT NULL,
  `ward_abbrv` char(6) DEFAULT NULL,
  `ward_desc` varchar(60) DEFAULT NULL,
  `cong_dist_abbrv` char(6) DEFAULT NULL,
  `super_court_abbrv` char(6) DEFAULT NULL,
  `judic_dist_abbrv` char(6) DEFAULT NULL,
  `nc_senate_abbrv` char(6) DEFAULT NULL,
  `nc_house_abbrv` char(6) DEFAULT NULL,
  `county_commiss_abbrv` char(6) DEFAULT NULL,
  `county_commiss_desc` varchar(60) DEFAULT NULL,
  `township_abbrv` char(6) DEFAULT NULL,
  `township_desc` varchar(60) DEFAULT NULL,
  `school_dist_abbrv` char(6) DEFAULT NULL,
  `school_dist_desc` varchar(60) DEFAULT NULL,
  `fire_dist_abbrv` char(6) DEFAULT NULL,
  `fire_dist_desc` varchar(60) DEFAULT NULL,
  `water_dist_abbrv` char(6) DEFAULT NULL,
  `water_dist_desc` varchar(60) DEFAULT NULL,
  `sewer_dist_abbrv` char(6) DEFAULT NULL,
  `sewer_dist_desc` varchar(60) DEFAULT NULL,
  `sanit_dist_abbrv` char(6) DEFAULT NULL,
  `sanit_dist_desc` varchar(60) DEFAULT NULL,
  `rescue_dist_abbrv` char(6) DEFAULT NULL,
  `rescue_dist_desc` varchar(60) DEFAULT NULL,
  `munic_dist_abbrv` char(6) DEFAULT NULL,
  `munic_dist_desc` varchar(60) DEFAULT NULL,
  `dist_1_abbrv` char(6) DEFAULT NULL,
  `dist_1_desc` varchar(60) DEFAULT NULL,
  `dist_2_abbrv` char(6) DEFAULT NULL,
  `dist_2_desc` varchar(60) DEFAULT NULL,
  `Confidential_ind` char(1) DEFAULT NULL,
  `age` varchar(50) DEFAULT NULL,
  `ncid` char(12) NOT NULL,
  `vtd_abbrv` char(6) DEFAULT NULL,
  `vtd_desc` char(60) DEFAULT NULL,
  PRIMARY KEY (`ncid`),
  KEY `county_id` (`county_id`),
  KEY `county_desc` (`county_desc`),
  KEY `county_id_2` (`county_id`),
  KEY `last_name` (`last_name`,`first_name`,`midl_name`),
  KEY `zip_code` (`zip_code`),
  KEY `race_code` (`race_code`),
  KEY `ethnic_code` (`ethnic_code`),
  KEY `gender_code` (`gender_code`),
  KEY `res_city_desc` (`res_city_desc`),
  KEY `voter_reg_num` (`voter_reg_num`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-08-12 16:03:37
