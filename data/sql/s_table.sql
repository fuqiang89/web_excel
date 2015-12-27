/*
Navicat MySQL Data Transfer

Source Server         : tornado
Source Server Version : 50535
Source Host           : 10.0.0.110:3306
Source Database       : demo2

Target Server Type    : MYSQL
Target Server Version : 50535
File Encoding         : 65001

Date: 2014-12-28 23:59:26
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for s_table
-- ----------------------------
DROP TABLE IF EXISTS `s_table`;
CREATE TABLE `s_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `srv_num` varchar(255) DEFAULT NULL,
  `inter_ip` varchar(255) DEFAULT NULL,
  `local_ip` varchar(255) DEFAULT NULL,
  `rank_one` varchar(255) DEFAULT NULL,
  `Srv_used` varchar(255) DEFAULT NULL,
  `re_admin` varchar(255) DEFAULT NULL,
  `admin` varchar(255) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `srv_num` (`srv_num`)
) ENGINE=InnoDB AUTO_INCREMENT=426 DEFAULT CHARSET=utf8;
