/*
MySQL Backup
Database: yqing
Backup Time: 2022-12-05 17:25:37
*/

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `yqing`.`admins`;
DROP TABLE IF EXISTS `yqing`.`config`;
DROP TABLE IF EXISTS `yqing`.`credit_config`;
DROP TABLE IF EXISTS `yqing`.`qjm_config`;
CREATE TABLE `admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `xuehao` varchar(50) NOT NULL COMMENT '学号',
  `password` varchar(20) NOT NULL COMMENT '密码',
  PRIMARY KEY (`id`),
  UNIQUE KEY `xuehao` (`xuehao`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
CREATE TABLE `config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `WebName` varchar(255) NOT NULL COMMENT '网站名称',
  `WebUrl` varchar(200) NOT NULL COMMENT '前端地址',
  `DKURL` varchar(200) NOT NULL COMMENT '学校打卡网站',
  `Managers` varchar(200) NOT NULL COMMENT '管理员id/QQ',
  `Groups` varchar(200) NOT NULL COMMENT '响应的QQ群',
  `CorpID` varchar(200) NOT NULL COMMENT '企业微信ID',
  `AccessToken` text NOT NULL COMMENT '企业微信token',
  `AgentID` varchar(200) NOT NULL COMMENT '企业微信应用ID',
  `CorpSecret` varchar(200) NOT NULL COMMENT '企业微信应用密钥',
  `VpnCookieList` text NOT NULL COMMENT 'vpncookiejson列表',
  `VpnLoginUrl` text NOT NULL COMMENT 'vpn登录二维码链接',
  `VpnLoginTime` datetime NOT NULL COMMENT 'vpn登录二维码获取时间',
  `AdminEmail` varchar(200) NOT NULL COMMENT '管理员的邮箱',
  `SendEmailUser` varchar(200) NOT NULL COMMENT '发送邮箱账号',
  `SendEmailPassword` varchar(200) NOT NULL COMMENT '发送邮箱密码',
  `SendFailMaxNum` int(11) NOT NULL COMMENT '邮件拒收的最大数量',
  `SendEmailMaxNum` int(11) NOT NULL COMMENT '验证邮件的最大发送次数',
  `EmailGG` text NOT NULL COMMENT '邮件通知内容',
  `gg` varchar(200) NOT NULL COMMENT '公告',
  `putdate` datetime NOT NULL COMMENT '公告更新时间',
  `QQGroupUrl` varchar(200) NOT NULL COMMENT 'QQ群加群链接',
  `KamiPayUrl` varchar(200) NOT NULL COMMENT '卡密购买地址',
  `SendEmailUserName` varchar(200) NOT NULL COMMENT '发送邮箱账号前缀',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `putdate` (`putdate`),
  UNIQUE KEY `gg` (`gg`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
CREATE TABLE `credit_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CheckCredit` int(11) NOT NULL COMMENT '签到获得积分数',
  `QJMCredit` int(11) NOT NULL COMMENT '请假码积分单价',
  `JoinCredit` int(11) NOT NULL COMMENT '新注册用户获得积分数',
  `ActivityStartTime` datetime NOT NULL COMMENT '积分活动开始时间',
  `ActivityEndTime` datetime NOT NULL COMMENT '积分活动结束时间',
  `ActivityUserGetNum` int(11) NOT NULL COMMENT '普通群员获得最大积分数',
  `ActivityAdminGetNum` int(11) NOT NULL COMMENT '群管理获得最大积分数',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
CREATE TABLE `qjm_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hour_max` int(11) NOT NULL COMMENT '请假小时上限',
  `AdminQjmSwitch` tinyint(1) NOT NULL COMMENT '全局请假开关',
  `qjm_switch` tinyint(1) NOT NULL COMMENT '请假码开关',
  `QjmHide` tinyint(1) NOT NULL COMMENT '隐藏请假码',
  `today_max_num` int(11) NOT NULL COMMENT '当天限制的请假数量',
  `moring` int(11) NOT NULL COMMENT '最早请假时间',
  `evening` int(11) NOT NULL COMMENT '最晚请假时间',
  `FengXian` tinyint(1) NOT NULL COMMENT '地区是否为风险地区',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
BEGIN;
LOCK TABLES `yqing`.`admins` WRITE;
DELETE FROM `yqing`.`admins`;
INSERT INTO `yqing`.`admins` (`id`,`xuehao`,`password`) VALUES (1, '123456', 'abcd');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `yqing`.`config` WRITE;
DELETE FROM `yqing`.`config`;
INSERT INTO `yqing`.`config` (`id`,`WebName`,`WebUrl`,`DKURL`,`Managers`,`Groups`,`CorpID`,`AccessToken`,`AgentID`,`CorpSecret`,`VpnCookieList`,`VpnLoginUrl`,`VpnLoginTime`,`AdminEmail`,`SendEmailUser`,`SendEmailPassword`,`SendFailMaxNum`,`SendEmailMaxNum`,`EmailGG`,`gg`,`putdate`,`QQGroupUrl`,`KamiPayUrl`,`SendEmailUserName`) VALUES (1, '南京科技疫情自动打卡', 'http://你的域名', 'https://xgyyx.njpi.edu.cn', '123,1234,1234', '124', 'ww118d8a7258126c4', 'UAntBfqmilkiSkk7hgMouG6PP9VtP7_Ma6kBnUm_cQj0d2AwZZ8ySqJ9VzdlrYWbG5jdUHG9soMjNCwqpISQYvEjBH8XLaldLQmvTnS9ZAThRqGwiuKzABNs_UrDJFCbAZ9-8Xgxpum_F0Bg0uhynZkUEtfntxncBh1RinyjYtcQ34wO4mqy35tM5sLA5heGFshZE0YA2e4W7E742jQ', '100007', 'Uazi8C0abPK5tOtzvrMUQU848NHGgD6pRrB3gPK0', '{\'sid\': \'2cfbf444-6dde-4187-b4f0-85da3ca6998f_d49ba6-8373-4202-bf9b-649f8ec3383d\', \'sid-legacy\': \'2cfbf444-6dde-4187-b4f0-85da3ca6998f_d1949ba6-8373-4202-bf9b-649f8ec3383d\', \'sid-legacy.sig\': \'IyFfmrYz5yVB8NidxswuI3lXUWKrqiJACQogaMYruvw\', \'sid.sig\': \'C7T1UJCL5pxGjmpKFSS9N9GEX-oU9nmOA28ou8dAcus\'}', 'https://open.work.weixin.qq.com/wwopen/sso/qrImg?key=800b2bf20b745a4d', '2022-12-05 09:00:02', 'ghwg18@qq.com', 'mail@blog18.cn', '123456', 5, 8, '<p>学校已经把我的服务器ip封了，大家明天自己打卡吧，如果到最后搞不了，本服务将关闭</p>\r\n<p>感谢大家一路的支持</p>', '学校可能封了我服务器ip，暂时不能添加和登录账号', '2022-12-05 15:35:07', 'https://qm.qq.com/cgi-bin/qm/qr?k=-GTDsF20Loc4AA97vT9nFR4nExSi_EFN&jump_from=webapi&authKey=8VWwu9BaC7+X7uPEBTPOPnFJnVwycwLDFCCamgFcpL77eSHqh1YA6y8+U64JjUlq', 'https://dwz.cn/4sfaYq9B', 'mail');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `yqing`.`credit_config` WRITE;
DELETE FROM `yqing`.`credit_config`;
INSERT INTO `yqing`.`credit_config` (`id`,`CheckCredit`,`QJMCredit`,`JoinCredit`,`ActivityStartTime`,`ActivityEndTime`,`ActivityUserGetNum`,`ActivityAdminGetNum`) VALUES (1, 1, 1, 3, '2022-11-08 16:05:00', '2022-11-08 17:10:00', 2, 4);
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `yqing`.`qjm_config` WRITE;
DELETE FROM `yqing`.`qjm_config`;
INSERT INTO `yqing`.`qjm_config` (`id`,`hour_max`,`AdminQjmSwitch`,`qjm_switch`,`QjmHide`,`today_max_num`,`moring`,`evening`,`FengXian`) VALUES (1, 16, 1, 1, 1, 0, 6, 22, 0);
UNLOCK TABLES;
COMMIT;
