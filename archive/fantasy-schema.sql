CREATE DATABASE `fantasy` /*!40100 DEFAULT CHARACTER SET latin1 */;

CREATE TABLE `matches` (
  `id` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `round` int(11) NOT NULL,
  `date` varchar(30) DEFAULT NULL,
  `venue_id` int(11) DEFAULT NULL,
  `home_id` int(11) NOT NULL,
  `away_id` int(11) NOT NULL,
  `partial_lockout` tinyint(4) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_goals` int(11) DEFAULT NULL,
  `home_behinds` int(11) DEFAULT NULL,
  `away_goals` int(11) DEFAULT NULL,
  `away_behinds` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `players` (
  `id` int(11) NOT NULL,
  `year` int(11) DEFAULT NULL,
  `firstname` varchar(50) NOT NULL,
  `lastname` varchar(50) NOT NULL,
  `squad_id` int(11) NOT NULL,
  `fwd` tinyint(4) DEFAULT NULL,
  `mid` tinyint(4) DEFAULT NULL,
  `ruc` tinyint(4) DEFAULT NULL,
  `def` tinyint(4) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `scores` (
  `year` int(11) NOT NULL,
  `round` int(11) NOT NULL,
  `player_id` int(11) NOT NULL,
  `squad_id` varchar(45) DEFAULT NULL,
  `squad_against_id` int(11) DEFAULT NULL,
  `venue_id` int(11) DEFAULT NULL,
  `position` varchar(10) DEFAULT NULL COMMENT 'One of:\nfwd,mid,ruc,def',
  `kicks` int(11) DEFAULT NULL,
  `handballs` int(11) DEFAULT NULL,
  `marks` int(11) DEFAULT NULL,
  `tackles` varchar(45) DEFAULT NULL,
  `hitouts` varchar(45) DEFAULT NULL,
  `frees_for` varchar(45) DEFAULT NULL,
  `frees_against` varchar(45) DEFAULT NULL,
  `goals` int(11) DEFAULT NULL COMMENT 'Rank after the round. ',
  `behinds` varchar(45) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `price` int(11) DEFAULT NULL COMMENT 'Price before the round. \nShould be extra round at end of season for final price. ',
  `selections` int(11) DEFAULT NULL COMMENT 'Selections during the round',
  `tog` int(11) DEFAULT NULL,
  PRIMARY KEY (`year`,`round`,`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `squads` (
  `id` int(11) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `shortname` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `venues` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `short_name` varchar(10) NOT NULL,
  `timezone` varchar(100) NOT NULL COMMENT 'e.g. Australia/Sydney',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

