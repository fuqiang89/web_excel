/*
Navicat MySQL Data Transfer

Source Server         : tornado
Source Server Version : 50535
Source Host           : 10.0.0.110:3306
Source Database       : demo2

Target Server Type    : MYSQL
Target Server Version : 50535
File Encoding         : 65001

Date: 2014-12-28 23:59:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for table_op_reg
-- ----------------------------
DROP TABLE IF EXISTS `table_op_reg`;
CREATE TABLE `table_op_reg` (
  `autoid` int(11) NOT NULL AUTO_INCREMENT,
  `table_name` varchar(255) NOT NULL,
  `id` int(11) DEFAULT NULL,
  `srv_num` varchar(100) DEFAULT NULL,
  `inter_ip` varchar(255) DEFAULT NULL,
  `local_ip` varchar(255) DEFAULT NULL,
  `Srv_used` varchar(255) DEFAULT NULL,
  `admin` varchar(255) DEFAULT NULL,
  `re_admin` varchar(255) DEFAULT NULL,
  `rank_one` varchar(255) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `op_time` datetime DEFAULT NULL,
  `act` varchar(25) DEFAULT NULL,
  `opName` varchar(255) DEFAULT NULL,
  `xExplain` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`autoid`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;
