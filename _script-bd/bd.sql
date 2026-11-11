-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : mer. 11 nov. 2026 à 15:36
-- Version du serveur : 9.1.0
-- Version de PHP : 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `vintagemarket`
--

-- --------------------------------------------------------

--
-- Structure de la table `achat`
--

DROP TABLE IF EXISTS `achat`;
CREATE TABLE IF NOT EXISTS `achat` (
  `id_achat` int NOT NULL AUTO_INCREMENT,
  `id_produit` int NOT NULL,
  `id_acheteur` int NOT NULL,
  `prix_achat` decimal(10,2) NOT NULL,
  `date_achat` date NOT NULL,
  `paye` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_achat`),
  UNIQUE KEY `id_produit` (`id_produit`),
  UNIQUE KEY `id_produit_2` (`id_produit`,`id_acheteur`),
  KEY `id_acheteur` (`id_acheteur`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `achat`
--

INSERT INTO `achat` (`id_achat`, `id_produit`, `id_acheteur`, `prix_achat`, `date_achat`, `paye`) VALUES
(1, 1, 2, 34.00, '2026-06-20', 1),
(2, 7, 3, 185.00, '2026-05-03', 1),
(3, 10, 4, 110.00, '2026-02-02', 1),
(4, 15, 5, 145.00, '2025-12-01', 1),
(5, 18, 6, 420.00, '2026-03-07', 1),
(6, 22, 2, 275.00, '2025-06-01', 1),
(7, 4, 1, 1350.00, '2026-03-18', 1),
(8, 8, 3, 2100.00, '2025-11-02', 1),
(9, 13, 5, 780.00, '2026-01-04', 1),
(10, 17, 6, 890.00, '2025-08-01', 1),
(11, 5, 4, 1850.00, '2026-05-28', 1),
(12, 2, 6, 850.00, '2026-05-09', 1),
(14, 11, 1, 2400.00, '2026-10-27', 1),
(15, 24, 1, 1750.00, '2026-10-27', 1),
(16, 6, 1, 650.00, '2026-10-27', 1),
(18, 12, 1, 3200.00, '2026-10-27', 1),
(19, 3, 1, 1150.00, '2026-10-27', 1),
(20, 9, 1, 980.00, '2026-11-02', 1),
(22, 21, 1, 725.00, '2026-11-02', 0);

-- --------------------------------------------------------

--
-- Structure de la table `echange`
--

DROP TABLE IF EXISTS `echange`;
CREATE TABLE IF NOT EXISTS `echange` (
  `id_echange` int NOT NULL AUTO_INCREMENT,
  `proprio` int NOT NULL,
  `id_utilisateur` int NOT NULL,
  `produit_echange` int NOT NULL,
  `produit_offert` int NOT NULL,
  `commentaire` text NOT NULL,
  `approuver` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_echange`),
  KEY `CLE_ETRANGERE_PROPRIO` (`proprio`) USING BTREE,
  KEY `CLE_ETRANGERE_PRODDUIT_OFFERT` (`produit_offert`) USING BTREE,
  KEY `CLE_ETRANGERE_PRODUIT_ECHANGE` (`produit_echange`) USING BTREE,
  KEY `CLE_ETRANGERE_UTILISATEUR` (`id_utilisateur`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Déchargement des données de la table `echange`
--

INSERT INTO `echange` (`id_echange`, `proprio`, `id_utilisateur`, `produit_echange`, `produit_offert`, `commentaire`, `approuver`) VALUES
(1, 5, 2, 19, 14, '', NULL),
(2, 3, 4, 16, 22, '', NULL),
(3, 3, 4, 23, 4, '', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `produit`
--

DROP TABLE IF EXISTS `produit`;
CREATE TABLE IF NOT EXISTS `produit` (
  `id_produit` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `prix` decimal(10,2) NOT NULL,
  `id_vendeur` int NOT NULL,
  `id_statut` int NOT NULL,
  `date` date NOT NULL,
  `archive` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_produit`),
  KEY `id_vendeur` (`id_vendeur`),
  KEY `id_statut` (`id_statut`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `produit`
--

INSERT INTO `produit` (`id_produit`, `nom`, `description`, `prix`, `id_vendeur`, `id_statut`, `date`, `archive`) VALUES
(1, 'Ongles amande renforcés', 'Faux ongles courts en forme d\'amande plus épais à l\'avant pour éviter les fissures et plus fins à l\'arrière', 34.00, 1, 4, '2026-06-12', 0),
(2, 'Portrait à l\'huile Femme au chapeau rouge', 'Portrait original peint à l\'huile représentant une femme avec un chapeau rouge', 850.00, 2, 4, '2026-04-18', 0),
(3, 'Fauteuil Art déco années 1930', 'Fauteuil ancien avec structure en bois et tissu restauré', 1150.00, 3, 4, '2026-09-18', 0),
(4, 'Le Petit Prince édition 1946', 'Ancienne édition française du Petit Prince publiée en 1946', 1350.00, 4, 4, '2026-03-02', 0),
(5, 'Sculpture femme en bronze', 'Sculpture ancienne en bronze représentant une femme debout', 1850.00, 5, 4, '2026-05-08', 0),
(6, 'Game Boy édition Pokémon jaune', 'Console Game Boy Pokémon jaune encore fonctionnelle', 650.00, 6, 4, '2026-09-21', 0),
(7, 'Palette Dior édition limitée', 'Palette Dior provenant d\'une ancienne collection limitée difficile à trouver', 185.00, 1, 4, '2026-04-20', 0),
(8, 'Les Misérables édition reliée', 'Ancienne édition des Misérables avec reliure en cuir', 2100.00, 4, 4, '2025-10-14', 0),
(9, 'Commode en noyer massif 1920', 'Commode ancienne en noyer avec cinq tiroirs et poignées en laiton', 980.00, 3, 4, '2026-09-12', 0),
(10, 'Rouge à lèvres Lancôme collection archive', 'Rouge à lèvres Lancôme provenant d\'une collection qui n\'est plus vendue', 110.00, 1, 4, '2026-01-15', 0),
(11, 'Buste en marbre blanc italien', 'Buste décoratif sculpté dans du marbre blanc', 2400.00, 5, 4, '2026-09-17', 0),
(12, 'PlayStation Net Yaroze', 'Console PlayStation noire rare destinée à la création de jeux', 3200.00, 6, 4, '2026-09-20', 0),
(13, 'L\'Étranger édition canadienne ancienne', 'Ancienne édition canadienne du roman L\'Étranger', 780.00, 4, 4, '2025-12-11', 0),
(14, 'Portrait familial québécois de 1918', 'Ancien portrait d\'une famille québécoise avec son cadre original', 320.00, 2, 1, '2026-08-28', 0),
(15, 'Poudre compacte MAC édition 2008', 'Poudre MAC provenant d\'une collection limitée de 2008', 145.00, 1, 4, '2025-11-20', 0),
(16, 'Brochure Ford Mustang 1967', 'Brochure publicitaire originale de la Ford Mustang 1967', 225.00, 3, 3, '2025-08-03', 0),
(17, 'Dracula édition illustrée ancienne', 'Ancienne édition illustrée de Dracula avec couverture rigide', 890.00, 4, 4, '2025-07-08', 0),
(18, 'Ensemble couture rose années 1990', 'Ensemble deux pièces sur mesure avec veste et jupe assorties', 420.00, 1, 4, '2026-02-19', 0),
(19, 'Coffret skincare Sulwhasoo édition limitée', 'Coffret de soins Sulwhasoo provenant d\'une édition limitée', 315.00, 5, 3, '2026-09-10', 0),
(20, 'iPod Classic première génération', 'iPod Apple de première génération avec sa molette originale', 950.00, 6, 1, '2026-08-30', 0),
(21, 'Portrait miniature peint ancien', 'Petit portrait ancien peint à la main dans un cadre ovale', 725.00, 2, 2, '2026-09-07', 0),
(22, 'Sac à main perlé fait main', 'Sac à main vintage couvert de perles et fabriqué à la main', 275.00, 1, 4, '2025-05-13', 1),
(23, 'Volant Porsche 911 classique', 'Volant original provenant d\'une ancienne Porsche 911', 1450.00, 3, 3, '2026-08-22', 0),
(24, 'Atlas mondial relié en cuir 1904', 'Ancien atlas mondial avec cartes en couleur et reliure en cuir', 1750.00, 4, 4, '2026-09-15', 0),
(25, 'Cadillac DeVille 1994 rose', 'Cadillac DeVille de 1994 avec peinture rose et intérieur restauré', 20000.00, 1, 2, '2026-09-22', 0),
(26, 'Journal en cuir brun', 'Journal en cuir brun avec reliure et attache crayon', 20.00, 1, 1, '2026-10-25', 1);

-- --------------------------------------------------------

--
-- Structure de la table `statut_produit`
--

DROP TABLE IF EXISTS `statut_produit`;
CREATE TABLE IF NOT EXISTS `statut_produit` (
  `id_statut` int NOT NULL AUTO_INCREMENT,
  `nom_statut` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_statut`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `statut_produit`
--

INSERT INTO `statut_produit` (`id_statut`, `nom_statut`) VALUES
(1, 'En vente'),
(2, 'Aux enchères'),
(3, 'À échanger'),
(4, 'Vendu');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

DROP TABLE IF EXISTS `utilisateur`;
CREATE TABLE IF NOT EXISTS `utilisateur` (
  `id_utilisateur` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `courriel` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `mot_de_passe` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_utilisateur`),
  UNIQUE KEY `courriel` (`courriel`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`id_utilisateur`, `nom`, `courriel`, `mot_de_passe`) VALUES
(1, 'Caresha', 'CRESHA@market.com', '87d443d4a9bd1aa4106435d9fdce49647786ecfbd484fb0251e78a27610de65a7d708493bc5ab5914e00ff77a4ac04636602698725c27f737ed1cb745ce1e1af'),
(2, 'Jean-Pierre', 'JP@market.com', '593acecb7eac76e5abd8782fb478e2dfe28911264d31dcea7cec8dfbad1cb9327a66a2898df6cefa7a7045d00947f53b6722ce65ac20d0a6348d47cc184286f5'),
(3, 'Pathy La Belle', 'Plabel@market.com', '9ed738fbf90cb57af9acb851455c5159247c7cae60a826feb5be4c8b866b3071018ba7867dc662d7bfe27f1a1889896126d411174a53c75dad01ed7b8f67bfe6'),
(4, 'Martin Bertrand', 'Mber007@market.com', 'f04ec289bcdc7b8154e2642fc3875df58bbef4ee56e5acc9e33b0f94609bbba882f7524f15315e84ab22c41b9ffa42432e9d000f2d0bdf6ee1e22d629eb9dbaa\r\n'),
(5, 'Rose', 'PinkBarbie@market.com', '873492a645776b82c5a2378aa7d392923b8f8a12d79e0af30f903e100415124d1bfc5bcb310c380fc3c5a295955f88d95b7b5e615885274f119f3696333b6126'),
(6, 'Ethan Manon', 'ManEt@market.com', '1ffb4eadaef5e3fcd9ed860ffe911c07284c94ac18b2b8e1d65daa048f6b0bfc39342b45371cbd7ab711344c36dfb321f401f875d14bec39e1453503dae6d538\r\n');

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `achat`
--
ALTER TABLE `achat`
  ADD CONSTRAINT `achat_ibfk_1` FOREIGN KEY (`id_produit`) REFERENCES `produit` (`id_produit`),
  ADD CONSTRAINT `achat_ibfk_2` FOREIGN KEY (`id_acheteur`) REFERENCES `utilisateur` (`id_utilisateur`);

--
-- Contraintes pour la table `echange`
--
ALTER TABLE `echange`
  ADD CONSTRAINT `echange_ibfk_1` FOREIGN KEY (`proprio`) REFERENCES `utilisateur` (`id_utilisateur`),
  ADD CONSTRAINT `echange_ibfk_2` FOREIGN KEY (`id_utilisateur`) REFERENCES `utilisateur` (`id_utilisateur`) ON DELETE CASCADE,
  ADD CONSTRAINT `echange_ibfk_3` FOREIGN KEY (`produit_echange`) REFERENCES `produit` (`id_produit`) ON DELETE CASCADE,
  ADD CONSTRAINT `echange_ibfk_4` FOREIGN KEY (`produit_offert`) REFERENCES `produit` (`id_produit`) ON DELETE CASCADE;

--
-- Contraintes pour la table `produit`
--
ALTER TABLE `produit`
  ADD CONSTRAINT `produit_ibfk_1` FOREIGN KEY (`id_vendeur`) REFERENCES `utilisateur` (`id_utilisateur`),
  ADD CONSTRAINT `produit_ibfk_2` FOREIGN KEY (`id_statut`) REFERENCES `statut_produit` (`id_statut`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
