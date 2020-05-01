-- phpMyAdmin SQL Dump
-- version 4.0.10deb1ubuntu0.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 01, 2020 at 11:37 AM
-- Server version: 5.5.62-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `halukijl_is437`
--

-- --------------------------------------------------------

--
-- Table structure for table `halukijl_admins`
--

CREATE TABLE IF NOT EXISTS `halukijl_admins` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `password` int(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=13 ;

--
-- Dumping data for table `halukijl_admins`
--

INSERT INTO `halukijl_admins` (`id`, `email`, `fname`, `lname`, `password`) VALUES
(1, 'jh@ps.com', 'Jenny', 'Halukiewicz', 1234),
(2, 'jd@gmail.com', 'Joe', 'Deer', 1234),
(11, 'by@ps.com', 'Brett', 'Young', 1234),
(12, 'mw@ps.com', 'Morgan', 'Wallen', 1234);

-- --------------------------------------------------------

--
-- Table structure for table `halukijl_lineItems`
--

CREATE TABLE IF NOT EXISTS `halukijl_lineItems` (
  `lid` int(11) NOT NULL AUTO_INCREMENT,
  `oid` int(11) DEFAULT NULL,
  `pid` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` float(11,2) NOT NULL,
  PRIMARY KEY (`lid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Dumping data for table `halukijl_lineItems`
--

INSERT INTO `halukijl_lineItems` (`lid`, `oid`, `pid`, `quantity`, `price`) VALUES
(3, 3, 2, 2, 15.56),
(4, 3, 4, 2, 19.45),
(5, 4, 2, 6, 15.56),
(6, 4, 4, 1, 19.45);

-- --------------------------------------------------------

--
-- Table structure for table `halukijl_orders`
--

CREATE TABLE IF NOT EXISTS `halukijl_orders` (
  `oid` int(11) NOT NULL AUTO_INCREMENT,
  `createtime` datetime NOT NULL,
  `status` varchar(20) NOT NULL,
  `orderprice` float NOT NULL,
  `userid` int(100) NOT NULL,
  PRIMARY KEY (`oid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `halukijl_orders`
--

INSERT INTO `halukijl_orders` (`oid`, `createtime`, `status`, `orderprice`, `userid`) VALUES
(3, '2020-05-01 09:23:24', 'completed', 70.02, 14),
(4, '2020-05-01 10:55:09', 'completed', 112.81, 14),
(5, '2020-05-01 12:32:46', 'shopping', 0, 14);

-- --------------------------------------------------------

--
-- Table structure for table `halukijl_products`
--

CREATE TABLE IF NOT EXISTS `halukijl_products` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `sku` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `price` decimal(5,2) NOT NULL,
  `description` varchar(100) NOT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `halukijl_products`
--

INSERT INTO `halukijl_products` (`pid`, `sku`, `name`, `price`, `description`) VALUES
(2, '1', 'Sweater', 15.56, 'Red sweater with white accents.'),
(3, '34', 'Hat', 5.43, 'Blue hat with white puff on top'),
(4, '62', 'Coat', 19.45, 'Yellow rain coat with white dots'),
(5, '124', 'Dress', 11.89, 'White dress with blue stripes');

-- --------------------------------------------------------

--
-- Table structure for table `halukijl_users`
--

CREATE TABLE IF NOT EXISTS `halukijl_users` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `subscribed` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

--
-- Dumping data for table `halukijl_users`
--

INSERT INTO `halukijl_users` (`id`, `fname`, `lname`, `email`, `password`, `subscribed`) VALUES
(14, 'Jenny', 'Halukiewicz', 'jh@gmail.com', '1234', 'True'),
(27, 'John', 'Lee', 'jl@gmail.com', '1234', 'true'),
(24, 'Max', 'Green', 'mg@gmail.com', '1234', 'true');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
