/*
SQLyog Ultimate v12.4.1 (64 bit)
MySQL - 8.0.22 : Database - jodalcheng
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`jodalcheng` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `jodalcheng`;

/*Table structure for table `tc_contract` */

DROP TABLE IF EXISTS `tc_contract`;

CREATE TABLE `tc_contract` (
  `c_idx` int NOT NULL AUTO_INCREMENT COMMENT '계약 인덱스',
  `c_num` varchar(30) DEFAULT NULL COMMENT '계약 번호',
  `c_date` timestamp NULL DEFAULT NULL COMMENT '계약 일시',
  `c_title` text COMMENT '계약 이름',
  `c_method` varchar(30) DEFAULT NULL COMMENT '계약 방법',
  `c_price` varchar(20) DEFAULT NULL COMMENT '계약 금액',
  `c_institution_name` varchar(100) DEFAULT NULL COMMENT '발주 기관',
  `c_company_name` varchar(30) DEFAULT NULL COMMENT '담당 업체 이름',
  `c_chief` varchar(10) DEFAULT NULL COMMENT '담당 업제 담당자',
  `c_phone` varchar(20) DEFAULT NULL COMMENT '담당 업체 연락처',
  `c_insert_ts` timestamp NULL DEFAULT NULL COMMENT '입력 시간',
  `c_update_ts` timestamp NULL DEFAULT NULL COMMENT '수정 시간',
  PRIMARY KEY (`c_idx`),
  UNIQUE KEY `UNIQUE` (`c_num`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Table structure for table `tco_company` */

DROP TABLE IF EXISTS `tco_company`;

CREATE TABLE `tco_company` (
  `co_idx` int NOT NULL AUTO_INCREMENT COMMENT '업체 인덱스',
  `co_regist_num` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '사업자등록번호',
  `co_company_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '업체명',
  `co_ceo_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '대표자명',
  `co_division` varchar(10) DEFAULT NULL COMMENT '기업구분',
  `co_region` varchar(100) DEFAULT NULL COMMENT '소재지명',
  `co_manufacturing` varchar(10) DEFAULT NULL COMMENT '제조구분',
  `co_post` varchar(30) DEFAULT NULL COMMENT '우편번호',
  `co_phone` varchar(30) DEFAULT NULL COMMENT '전화번호',
  `co_fax` varchar(30) DEFAULT NULL COMMENT '팩스번호',
  `co_national` varchar(30) DEFAULT NULL COMMENT '국적',
  `co_insert_ts` timestamp NULL DEFAULT NULL COMMENT '입력시간',
  `co_update_ts` timestamp NULL DEFAULT NULL COMMENT '수정시간',
  PRIMARY KEY (`co_idx`),
  UNIQUE KEY `UNIQUE` (`co_regist_num`)
) ENGINE=InnoDB AUTO_INCREMENT=575939 DEFAULT CHARSET=utf8;

/*Table structure for table `tpn_public_notice` */

DROP TABLE IF EXISTS `tpn_public_notice`;

CREATE TABLE `tpn_public_notice` (
  `pn_idx` int NOT NULL AUTO_INCREMENT COMMENT '공고 인덱스',
  `pn_num` varchar(30) DEFAULT NULL COMMENT '공고 번호',
  `pn_date` timestamp NULL DEFAULT NULL COMMENT '공고 일시',
  `pn_title` text COMMENT '공고 제목',
  `pn_method` varchar(30) DEFAULT NULL COMMENT '계약 방법',
  `pn_price` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '공고 금액',
  `pn_institution_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '기관명',
  `pn_bid_start_ts` timestamp NULL DEFAULT NULL COMMENT '입찰 개시 일시',
  `pn_bid_end_ts` timestamp NULL DEFAULT NULL COMMENT '입찰 마감 일시',
  `pn_open_ts` timestamp NULL DEFAULT NULL COMMENT '개찰(입찰) 일시',
  `pn_url` text COMMENT '공고 URL',
  `pn_visible` int DEFAULT '1' COMMENT '0 : 표시 안함, 1 : 표시함',
  `pn_insert_ts` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '입력 시간',
  `pn_update_ts` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '수정 시간',
  PRIMARY KEY (`pn_idx`),
  UNIQUE KEY `UNIQUE` (`pn_num`)
) ENGINE=InnoDB AUTO_INCREMENT=622 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
