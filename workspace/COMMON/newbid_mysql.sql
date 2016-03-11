<<<<<<< .mine
DROP TABLE IF EXISTS `newbid_product_info_table`
CREATE TABLE `newbid_product_info_table`(
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '����ID',
  `platformid` varchar(100) DEFAULT NULL COMMENT 'ƽ̨ID',
  `producttype` varchar(100) DEFAULT NULL COMMENT '��Ʒ����',
  `productname` varchar(100) DEFAULT NULL COMMENT '��Ʒ����',
  `producturl` varchar(100) DEFAULT NULL COMMENT '��ƷURL',
  `productid` varchar(100) DEFAULT NULL COMMENT '��ƷID',
  `amount` varchar(100) DEFAULT NULL COMMENT '����ܶ�(Ԫ)',
  `balance` varchar(100) DEFAULT NULL COMMENT '������(Ԫ)',
  `maxrate` varchar(100) DEFAULT NULL COMMENT '���������(%)',
  `minrate` varchar(100) DEFAULT NULL COMMENT '��С������(%)',
  `startdate` varchar(100) DEFAULT NULL COMMENT '����ʱ��',
  `enddate` varchar(100) DEFAULT NULL COMMENT '���ʱ��',
  `term` varchar(100) DEFAULT NULL COMMENT '��������',
  `termunit` varchar(100) DEFAULT NULL COMMENT '�������޵�λ',
  `repaymentmethod` varchar(100) DEFAULT NULL COMMENT '���ʽ',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��Ʒ��Ϣ���ʱ��',
||||||| .r17
DROP TABLE IF EXISTS `newbid_product_info`;
CREATE TABLE `newbid_product_info`(
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '����ID',
  `platformid` varchar(100) DEFAULT NULL COMMENT 'ƽ̨ID',
  `producttype` varchar(100) DEFAULT NULL COMMENT '��Ʒ����',
  `productname` varchar(100) DEFAULT NULL COMMENT '��Ʒ����',
  `producturl` varchar(100) DEFAULT NULL COMMENT '��ƷURL',
  `productid` varchar(100) DEFAULT NULL COMMENT '��ƷID',
  `amount` varchar(100) DEFAULT NULL COMMENT '����ܶ�(Ԫ)',
  `balance` varchar(100) DEFAULT NULL COMMENT '������(Ԫ)',
  `maxrate` varchar(100) DEFAULT NULL COMMENT '���������(%)',
  `minrate` varchar(100) DEFAULT NULL COMMENT '��С������(%)',
  `startdate` varchar(100) DEFAULT NULL COMMENT '����ʱ��',
  `enddate` varchar(100) DEFAULT NULL COMMENT '���ʱ��',
  `term` varchar(100) DEFAULT NULL COMMENT '��������',
  `termunit` varchar(100) DEFAULT NULL COMMENT '�������޵�λ',
  `repaymentmethod` varchar(100) DEFAULT NULL COMMENT '���ʽ',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��Ʒ��Ϣ���ʱ��',
=======
﻿#
# 文件编码调整为UTF8 Alex 20160310
#
DROP TABLE IF EXISTS `newbid_product_info`;
CREATE TABLE `newbid_product_info`(
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `platformid` varchar(100) DEFAULT NULL COMMENT '平台ID',
  `producttype` varchar(100) DEFAULT NULL COMMENT '产品类型',
  `productname` varchar(100) DEFAULT NULL COMMENT '产品名称',
  `producturl` varchar(100) DEFAULT NULL COMMENT '产品URL',
  `productid` varchar(100) DEFAULT NULL COMMENT '产品ID',
  `amount` varchar(100) DEFAULT NULL COMMENT '标的总额(元)',
  `balance` varchar(100) DEFAULT NULL COMMENT '标的余额(元)',
  `maxrate` varchar(100) DEFAULT NULL COMMENT '最大收益率(%)',
  `minrate` varchar(100) DEFAULT NULL COMMENT '最小收益率(%)',
  `startdate` varchar(100) DEFAULT NULL COMMENT '发标时间',
  `enddate` varchar(100) DEFAULT NULL COMMENT '结标时间',
  `term` varchar(100) DEFAULT NULL COMMENT '还款期限',
  `termunit` varchar(100) DEFAULT NULL COMMENT '还款期限单位',
  `repaymentmethod` varchar(100) DEFAULT NULL COMMENT '还款方式',
  `createtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '产品信息入库时间',
>>>>>>> .r29
  PRIMARY KEY (`id`)

<<<<<<< .mine
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='�±��Ʒ��Ϣ';
||||||| .r17
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='�±��Ʒ��Ϣ';
=======
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='新标产品信息';
>>>>>>> .r29
