/*
Navicat MySQL Data Transfer

Source Server         : tornado
Source Server Version : 50535
Source Host           : 10.0.0.110:3306
Source Database       : demo2

Target Server Type    : MYSQL
Target Server Version : 50535
File Encoding         : 65001

Date: 2014-12-28 23:59:43
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for table_nmap
-- ----------------------------
DROP TABLE IF EXISTS `table_nmap`;
CREATE TABLE `table_nmap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `srv_num` varchar(50) CHARACTER SET utf8 NOT NULL,
  `nmapdata` text COLLATE utf8_unicode_ci,
  `opTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
