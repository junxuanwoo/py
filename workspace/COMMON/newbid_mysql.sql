<<<<<<< .mine
DROP TABLE IF EXISTS `newbid_product_info_table`
CREATE TABLE `newbid_product_info_table`(
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ï¿½ï¿½ï¿½ï¿½ID',
  `platformid` varchar(100) DEFAULT NULL COMMENT 'Æ½Ì¨ID',
  `producttype` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½Æ·ï¿½ï¿½ï¿½ï¿½',
  `productname` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½Æ·ï¿½ï¿½ï¿½ï¿½',
  `producturl` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½Æ·URL',
  `productid` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½Æ·ID',
  `amount` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½ï¿½ï¿½Ü¶ï¿½(Ôª)',
  `balance` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½(Ôª)',
  `maxrate` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½(%)',
  `minrate` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½Ð¡ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½(%)',
  `startdate` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½ï¿½ï¿½Ê±ï¿½ï¿½',
  `enddate` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½ï¿½Ê±ï¿½ï¿½',
  `term` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½',
  `termunit` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½ï¿½Þµï¿½Î»',
  `repaymentmethod` varchar(100) DEFAULT NULL COMMENT 'ï¿½ï¿½ï¿½î·½Ê½',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'ï¿½ï¿½Æ·ï¿½ï¿½Ï¢ï¿½ï¿½ï¿½Ê±ï¿½ï¿½',
||||||| .r17
DROP TABLE IF EXISTS `newbid_product_info`;
CREATE TABLE `newbid_product_info`(
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Ö÷¼üID',
  `platformid` varchar(100) DEFAULT NULL COMMENT 'Æ½Ì¨ID',
  `producttype` varchar(100) DEFAULT NULL COMMENT '²úÆ·ÀàÐÍ',
  `productname` varchar(100) DEFAULT NULL COMMENT '²úÆ·Ãû³Æ',
  `producturl` varchar(100) DEFAULT NULL COMMENT '²úÆ·URL',
  `productid` varchar(100) DEFAULT NULL COMMENT '²úÆ·ID',
  `amount` varchar(100) DEFAULT NULL COMMENT '±êµÄ×Ü¶î(Ôª)',
  `balance` varchar(100) DEFAULT NULL COMMENT '±êµÄÓà¶î(Ôª)',
  `maxrate` varchar(100) DEFAULT NULL COMMENT '×î´óÊÕÒæÂÊ(%)',
  `minrate` varchar(100) DEFAULT NULL COMMENT '×îÐ¡ÊÕÒæÂÊ(%)',
  `startdate` varchar(100) DEFAULT NULL COMMENT '·¢±êÊ±¼ä',
  `enddate` varchar(100) DEFAULT NULL COMMENT '½á±êÊ±¼ä',
  `term` varchar(100) DEFAULT NULL COMMENT '»¹¿îÆÚÏÞ',
  `termunit` varchar(100) DEFAULT NULL COMMENT '»¹¿îÆÚÏÞµ¥Î»',
  `repaymentmethod` varchar(100) DEFAULT NULL COMMENT '»¹¿î·½Ê½',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '²úÆ·ÐÅÏ¢Èë¿âÊ±¼ä',
=======
ï»¿#
# æ–‡ä»¶ç¼–ç è°ƒæ•´ä¸ºUTF8 Alex 20160310
#
DROP TABLE IF EXISTS `newbid_product_info`;
CREATE TABLE `newbid_product_info`(
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ä¸»é”®ID',
  `platformid` varchar(100) DEFAULT NULL COMMENT 'å¹³å°ID',
  `producttype` varchar(100) DEFAULT NULL COMMENT 'äº§å“ç±»åž‹',
  `productname` varchar(100) DEFAULT NULL COMMENT 'äº§å“åç§°',
  `producturl` varchar(100) DEFAULT NULL COMMENT 'äº§å“URL',
  `productid` varchar(100) DEFAULT NULL COMMENT 'äº§å“ID',
  `amount` varchar(100) DEFAULT NULL COMMENT 'æ ‡çš„æ€»é¢(å…ƒ)',
  `balance` varchar(100) DEFAULT NULL COMMENT 'æ ‡çš„ä½™é¢(å…ƒ)',
  `maxrate` varchar(100) DEFAULT NULL COMMENT 'æœ€å¤§æ”¶ç›ŠçŽ‡(%)',
  `minrate` varchar(100) DEFAULT NULL COMMENT 'æœ€å°æ”¶ç›ŠçŽ‡(%)',
  `startdate` varchar(100) DEFAULT NULL COMMENT 'å‘æ ‡æ—¶é—´',
  `enddate` varchar(100) DEFAULT NULL COMMENT 'ç»“æ ‡æ—¶é—´',
  `term` varchar(100) DEFAULT NULL COMMENT 'è¿˜æ¬¾æœŸé™',
  `termunit` varchar(100) DEFAULT NULL COMMENT 'è¿˜æ¬¾æœŸé™å•ä½',
  `repaymentmethod` varchar(100) DEFAULT NULL COMMENT 'è¿˜æ¬¾æ–¹å¼',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'äº§å“ä¿¡æ¯å…¥åº“æ—¶é—´',
>>>>>>> .r29
  PRIMARY KEY (`id`)

<<<<<<< .mine
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='ï¿½Â±ï¿½ï¿½Æ·ï¿½ï¿½Ï¢';
||||||| .r17
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='ÐÂ±ê²úÆ·ÐÅÏ¢';
=======
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='æ–°æ ‡äº§å“ä¿¡æ¯';
>>>>>>> .r29
