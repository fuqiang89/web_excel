/*
Navicat MySQL Data Transfer

Source Server         : tornado
Source Server Version : 50535
Source Host           : 10.0.0.110:3306
Source Database       : demo2

Target Server Type    : MYSQL
Target Server Version : 50535
File Encoding         : 65001

Date: 2014-12-28 23:59:36
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for table_module
-- ----------------------------
DROP TABLE IF EXISTS `table_module`;
CREATE TABLE `table_module` (
  `table_name` varchar(255) NOT NULL,
  `fields` varchar(255) NOT NULL,
  `useAdmin` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of table_module
-- ----------------------------
INSERT INTO `table_module` VALUES ('srv_table', 'id,srv_num,inter_ip,local_ip,rank_one,Srv_used,admin,note', '吴枝森,林铮,章伟平,王富强,田碧鑫,方艳燕');
