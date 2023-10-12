-- --------------------------------------------------------
-- Verkkotietokone:              127.0.0.1
-- Palvelinversio:               11.1.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Versio:              12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for pahuksen_sormus
CREATE DATABASE IF NOT EXISTS `pahuksen_sormus` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `pahuksen_sormus`;

-- Dumping structure for taulu pahuksen_sormus.airport
CREATE TABLE IF NOT EXISTS `airport` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ident` varchar(40) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  `fantasia_nimi` varchar(40) DEFAULT NULL,
  `latitude_deg` double DEFAULT NULL,
  `longitude_deg` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pahuksen_sormus.airport: ~10 rows (suunnilleen)
REPLACE INTO `airport` (`id`, `ident`, `name`, `fantasia_nimi`, `latitude_deg`, `longitude_deg`) VALUES
	(1, 'HT-0001', 'Chancerelles Airport / Bowen Field', 'Uudentoivon-kylä', 18.560801, -72.327797),
	(2, 'MTCH', 'Cap Haitien International Airport', 'Ruoholaakso', 19.726734, -72.199576),
	(3, 'MTJA', 'Jacmel Airport', 'Velhotorni', 18.241100311279297, -72.51850128173828),
	(4, 'MTJE', 'JÃ©rÃ©mie Airport', 'Varisräme', 18.66309928894043, -74.17030334472656),
	(5, 'MTCA', 'Les Cayes Airport', 'Noitametsä', 18.271099090576172, -73.78829956054688),
	(6, 'HT-0012', 'Pignon Airport', 'Sammakkojärvi', 19.32361, -72.11666),
	(7, 'HT-0003', 'Hinche Airport', 'Suurentarmon-kaupunki', 19.13874, -72.016),
	(8, 'HT-0004', 'ÃŽle-Ã -Vache International Airport', 'Hiisisuo', 18.07058, -73.59194),
	(9, 'HT-0006', 'BelladÃ¨re Airport', 'Peikkoluola', 18.85264, -71.8171),
	(10, 'HT-0002', 'Anse-a-Galets Airport', 'Tulivuori', 18.841212270800003, -72.8802323341);

-- Dumping structure for taulu pahuksen_sormus.esineet
CREATE TABLE IF NOT EXISTS `esineet` (
  `esine_id` int(11) NOT NULL AUTO_INCREMENT,
  `esine_nimi` varchar(50) NOT NULL DEFAULT '',
  `esine_arvo` int(11) NOT NULL,
  `vaikutus_kohde` varchar(50) DEFAULT '',
  `esine_saatu_teksti` text DEFAULT NULL,
  `kuvaus` text DEFAULT NULL,
  PRIMARY KEY (`esine_id`),
  UNIQUE KEY `esine_id` (`esine_id`),
  UNIQUE KEY `esine_nimi` (`esine_nimi`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pahuksen_sormus.esineet: ~0 rows (suunnilleen)
REPLACE INTO `esineet` (`esine_id`, `esine_nimi`, `esine_arvo`, `vaikutus_kohde`, `esine_saatu_teksti`, `kuvaus`) VALUES
	(1, 'eliksiiri', 10, 'pelaaja_hp', 'Sait eliksiirin!', NULL),
	(2, 'taitojuoma', 3, 'pelaaja_taitopiste', NULL, NULL);

-- Dumping structure for taulu pahuksen_sormus.inventaario
CREATE TABLE IF NOT EXISTS `inventaario` (
  `pelaajan_id` int(11) NOT NULL,
  `esineen_id` int(11) NOT NULL,
  KEY `FK_inventaario_peli` (`pelaajan_id`),
  KEY `FK_inventaario_esineet` (`esineen_id`),
  CONSTRAINT `FK_inventaario_esineet` FOREIGN KEY (`esineen_id`) REFERENCES `esineet` (`esine_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_inventaario_peli` FOREIGN KEY (`pelaajan_id`) REFERENCES `peli` (`peli_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pahuksen_sormus.inventaario: ~0 rows (suunnilleen)

-- Dumping structure for taulu pahuksen_sormus.peli
CREATE TABLE IF NOT EXISTS `peli` (
  `peli_id` int(11) NOT NULL AUTO_INCREMENT,
  `pelaaja_nimi` varchar(12) NOT NULL,
  `pelaaja_sijainti` int(11) NOT NULL DEFAULT 1,
  `sormus_sijainti` int(11) NOT NULL DEFAULT 0,
  `menneet_paivat` int(11) NOT NULL DEFAULT 0,
  `pelaaja_hp` int(11) NOT NULL DEFAULT 30,
  `pelaaja_maksimi_hp` int(11) NOT NULL DEFAULT 30,
  `pelaaja_suojaus` int(11) NOT NULL DEFAULT 12,
  `pelaaja_isku` int(11) NOT NULL DEFAULT 6,
  `pelaaja_taitopiste` int(11) NOT NULL DEFAULT 3,
  `pelaaja_maksimi_taitopiste` int(11) NOT NULL DEFAULT 3,
  `onko_sormus` int(1) NOT NULL DEFAULT 0,
  `paivamaara` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`peli_id`),
  UNIQUE KEY `peli_id` (`peli_id`),
  KEY `pelaaja_sijainti` (`pelaaja_sijainti`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pahuksen_sormus.peli: ~0 rows (suunnilleen)

-- Dumping structure for taulu pahuksen_sormus.pisteet
CREATE TABLE IF NOT EXISTS `pisteet` (
  `id` int(11) DEFAULT NULL,
  `nimi` varchar(50) DEFAULT NULL,
  `paivat` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pahuksen_sormus.pisteet: ~0 rows (suunnilleen)

-- Dumping structure for taulu pahuksen_sormus.taidot
CREATE TABLE IF NOT EXISTS `taidot` (
  `taito_id` int(11) NOT NULL AUTO_INCREMENT,
  `taito_nimi` varchar(50) NOT NULL,
  `taito_arvo` int(11) NOT NULL,
  `taito_kohde` varchar(50) NOT NULL,
  `hahmon_luokka` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`taito_id`),
  UNIQUE KEY `taito_id` (`taito_id`),
  UNIQUE KEY `taito_nimi` (`taito_nimi`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pahuksen_sormus.taidot: ~0 rows (suunnilleen)
REPLACE INTO `taidot` (`taito_id`, `taito_nimi`, `taito_arvo`, `taito_kohde`, `hahmon_luokka`) VALUES
	(1, 'tulipallo', 10, 'vihollinen_hp', NULL);

-- Dumping structure for taulu pahuksen_sormus.viholliset
CREATE TABLE IF NOT EXISTS `viholliset` (
  `vihollinen_id` int(11) NOT NULL AUTO_INCREMENT,
  `vihollinen_nimi` varchar(20) NOT NULL DEFAULT '',
  `vihollinen_hp` int(11) NOT NULL DEFAULT 0,
  `vihollinen_maksimi_hp` int(11) NOT NULL DEFAULT 0,
  `vihollinen_suojaus` int(11) NOT NULL DEFAULT 0,
  `vihollinen_isku` int(11) NOT NULL DEFAULT 0,
  `bossi` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`vihollinen_id`),
  UNIQUE KEY `vihollinen_id` (`vihollinen_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table pahuksen_sormus.viholliset: ~4 rows (suunnilleen)
REPLACE INTO `viholliset` (`vihollinen_id`, `vihollinen_nimi`, `vihollinen_hp`, `vihollinen_maksimi_hp`, `vihollinen_suojaus`, `vihollinen_isku`, `bossi`) VALUES
	(1, 'Peikko', 12, 12, 12, 6, 0),
	(2, 'Luuranko', 10, 10, 10, 6, 0),
	(3, 'Gorgon', 30, 30, 12, 8, 1),
	(4, 'Jättisammakko', 15, 15, 8, 4, 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
