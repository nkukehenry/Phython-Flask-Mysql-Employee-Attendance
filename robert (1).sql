-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 06, 2021 at 01:38 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `robert`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `id` int(11) NOT NULL,
  `employee_id` int(11) NOT NULL,
  `arrival_time` varchar(50) DEFAULT NULL,
  `arrival_picture` varchar(50) DEFAULT NULL,
  `departure_time` varchar(50) DEFAULT NULL,
  `departure_picture` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`id`, `employee_id`, `arrival_time`, `arrival_picture`, `departure_time`, `departure_picture`, `date`) VALUES
(8, 6, '11:8', '2021-9-3/6/arrival.jpg', '22:20', '2021-9-3/6/departure.jpg', '2021-09-03'),
(9, 7, '12:53', '2021-9-3/7/arrival.jpg', '22:12', '2021-9-3/7/departure.jpg', '2021-09-03'),
(10, 7, '12:53', '2021-9-3/7/arrival.jpg', '13:39', '2021-9-3/7/departure.jpg', '2021-01-03');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `id` int(11) NOT NULL,
  `firstname` varchar(40) NOT NULL,
  `lastname` varchar(40) NOT NULL,
  `staffid` varchar(30) DEFAULT NULL,
  `department` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`id`, `firstname`, `lastname`, `staffid`, `department`) VALUES
(6, 'Sarah', 'Kayiwa', '65363637387', 'Accounts'),
(7, 'Henry', 'May', '877899', 'Accounts'),
(8, 'Lesley', 'Sample', '564343', 'Accounts'),
(19, 'Robert', 'Mugisa', '5667888', 'Procurement');

-- --------------------------------------------------------

--
-- Stand-in structure for view `timelog`
-- (See below for the actual view)
--
CREATE TABLE `timelog` (
`id` int(11)
,`employee_id` int(11)
,`name` varchar(81)
,`date` date
,`arrival_time` varchar(50)
,`departure_time` varchar(50)
,`hours` varchar(26)
,`time_worked` decimal(24,4)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `timetotals`
-- (See below for the actual view)
--
CREATE TABLE `timetotals` (
`id` int(11)
,`date` date
,`hours` decimal(46,4)
);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(300) NOT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `photo` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `employee_id`, `photo`) VALUES
(1, 'robert', 'password', 7, ''),
(2, 'sample', 'pbkdf2:sha256:260000$c7oh2n5ZMcAoAQMA$d4b6864ca3298ac597cbc678bd0c690aff0a550aff03090d79758d5509f520cc', 8, '');

-- --------------------------------------------------------

--
-- Structure for view `timelog`
--
DROP TABLE IF EXISTS `timelog`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `timelog`  AS SELECT `attendance`.`id` AS `id`, `employee`.`id` AS `employee_id`, concat(`employee`.`firstname`,' ',`employee`.`lastname`) AS `name`, `attendance`.`date` AS `date`, `attendance`.`arrival_time` AS `arrival_time`, `attendance`.`departure_time` AS `departure_time`, subtime(`attendance`.`departure_time`,`attendance`.`arrival_time`) AS `hours`, timestampdiff(MINUTE,concat(`attendance`.`date`,' ',`attendance`.`arrival_time`),concat(`attendance`.`date`,' ',`attendance`.`departure_time`)) / 60 AS `time_worked` FROM (`employee` join `attendance` on(`employee`.`id` = `attendance`.`employee_id`)) ;

-- --------------------------------------------------------

--
-- Structure for view `timetotals`
--
DROP TABLE IF EXISTS `timetotals`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `timetotals`  AS SELECT `attendance`.`id` AS `id`, `attendance`.`date` AS `date`, sum(timestampdiff(MINUTE,concat(`attendance`.`date`,' ',`attendance`.`arrival_time`),concat(`attendance`.`date`,' ',`attendance`.`departure_time`)) / 60) AS `hours` FROM (`employee` join `attendance` on(`employee`.`id` = `attendance`.`employee_id`)) GROUP BY `attendance`.`date` ORDER BY `attendance`.`date` DESC ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`),
  ADD UNIQUE KEY `id_2` (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
