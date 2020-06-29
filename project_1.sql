-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 29, 2020 at 07:52 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project_1`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`name`) VALUES
('China Eastern');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

CREATE TABLE `airline_staff` (
  `user_name` varchar(50) NOT NULL,
  `password` char(128) DEFAULT NULL,
  `first_name` varchar(25) DEFAULT NULL,
  `last_name` varchar(25) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `airline` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`user_name`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline`) VALUES
('robert', '202cb962ac59075b964b07152d234b70', 'Robert', 'Zhu', '1999-03-23', 'China Eastern'),
('robert990420', '1227fe415e79db47285cb2689c93963f', 'Robert', 'Zhu', '2020-06-10', 'China Eastern'),
('robertzhu', '02e74b3a3019e76422e2dd771afe7df3', 'robert', 'zhu', '1999-01-12', 'China Eastern');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `airplane_id` char(5) NOT NULL,
  `airline` varchar(50) NOT NULL,
  `capacity` decimal(3,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airplane_id`, `airline`, `capacity`) VALUES
('AAABB', 'China Eastern', '200'),
('ABCDE', 'China Eastern', '200'),
('ACDFG', 'China Eastern', '400');

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `name` varchar(50) NOT NULL,
  `city` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`name`, `city`) VALUES
('HKG', 'Hong Kong'),
('JFK', 'NYC'),
('PVG', 'Shanghai');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(50) NOT NULL,
  `password` char(128) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `phone_no` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `passport_no` char(9) DEFAULT NULL,
  `passport_exp` date DEFAULT NULL,
  `passport_country` varchar(20) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `street` varchar(50) DEFAULT NULL,
  `building_no` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `password`, `name`, `phone_no`, `date_of_birth`, `passport_no`, `passport_exp`, `passport_country`, `state`, `city`, `street`, `building_no`) VALUES
('123@gmail.com', '202cb962ac59075b964b07152d234b70', 'Tom', '123123123', '1990-01-01', 'AGHJGKHGV', '2020-01-01', 'China', 'Guangdong', 'Guangzhou', 'Jianshe', '12345'),
('456@gmail.com', '250cf8b51c773f3f8dc8b4be867a9a02', 'Jery', '456456456', '1990-02-02', 'BYTDCGNJH', '2020-02-02', 'China', 'Hubei', 'Wuhan', 'Dongchuan', '54321'),
('xurobertzhu@gmail.com', '202cb962ac59075b964b07152d234b70', 'Robert', '123645', '2020-06-02', 'AC1234567', '2020-08-26', 'China', 'New York', 'New York', '310 3rd Ave', '123'),
('xz1947@nyu.edu', '202cb962ac59075b964b07152d234b70', 'Robert', '123645', '1199-01-21', 'AC1234567', '2020-05-15', 'China', 'New York', 'New York', '310 3rd Ave', '123');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `flight_no` varchar(6) NOT NULL,
  `airline` varchar(50) NOT NULL,
  `dep_datetime` datetime NOT NULL,
  `arr_datetime` datetime DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `base_price` decimal(8,2) DEFAULT NULL,
  `seat_sold` decimal(3,0) DEFAULT NULL,
  `dep_airport` varchar(50) DEFAULT NULL,
  `arr_airport` varchar(50) DEFAULT NULL,
  `airplane_id` char(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`flight_no`, `airline`, `dep_datetime`, `arr_datetime`, `status`, `base_price`, `seat_sold`, `dep_airport`, `arr_airport`, `airplane_id`) VALUES
('AA111', 'China Eastern', '2019-01-01 02:00:00', '2019-01-01 11:00:00', 'delayed', '500.00', '100', 'JFK', 'PVG', 'ABCDE'),
('AA111', 'China Eastern', '2019-01-02 02:00:00', '2019-01-02 11:45:30', 'delay', '400.00', '80', 'JFK', 'PVG', 'ABCDE'),
('AA111', 'China Eastern', '2019-01-03 02:00:00', '2019-01-03 11:00:00', 'on-time', '500.00', '120', 'JFK', 'PVG', 'ABCDE'),
('AA111', 'China Eastern', '2019-01-04 02:00:00', '2019-01-04 11:58:45', 'delay', '999.00', '50', 'JFK', 'PVG', 'ABCDE'),
('AA123', 'China Eastern', '2020-07-15 12:35:02', '2020-07-16 03:35:02', 'on-time', '500.00', '0', 'JFK', 'PVG', 'ABCDE'),
('AA234', 'China Eastern', '2020-07-03 14:47:00', '2020-07-04 05:46:00', 'on_time', '1000.00', '0', 'PVG', 'JFK', 'ABCDE'),
('AA888', 'China Eastern', '2022-01-04 02:00:00', '2022-01-05 16:20:01', NULL, '888.00', '50', 'PVG', 'JFK', 'AAABB');

-- --------------------------------------------------------

--
-- Table structure for table `phone_no`
--

CREATE TABLE `phone_no` (
  `user_name` varchar(50) NOT NULL,
  `phone_no` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `take`
--

CREATE TABLE `take` (
  `email` varchar(50) NOT NULL,
  `flight_no` varchar(6) NOT NULL,
  `airline` varchar(50) NOT NULL,
  `dep_datetime` datetime NOT NULL,
  `rate` decimal(1,0) NOT NULL,
  `comment` varchar(1000) DEFAULT NULL,
  `ticket_id` char(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `take`
--

INSERT INTO `take` (`email`, `flight_no`, `airline`, `dep_datetime`, `rate`, `comment`, `ticket_id`) VALUES
('123@gmail.com', 'AA111', 'China Eastern', '2019-01-01 02:00:00', '0', 'The service is good', '10023890'),
('123@gmail.com', 'AA111', 'China Eastern', '2019-01-02 02:00:00', '0', 'The service is good', '10023891'),
('123@gmail.com', 'AA111', 'China Eastern', '2019-01-03 02:00:00', '0', 'The service is good', '10023892'),
('123@gmail.com', 'AA111', 'China Eastern', '2019-01-04 02:00:00', '0', 'The service is good', '10023893'),
('123@gmail.com', 'AA888', 'China Eastern', '2022-01-04 02:00:00', '0', 'The service is good', '10023894'),
('xurobertzhu@gmail.com', 'AA111', 'China Eastern', '2019-01-04 02:00:00', '0', NULL, '10023890'),
('xz1947@nyu.edu', 'AA111', 'China Eastern', '2019-01-02 02:00:00', '0', NULL, '10023888');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ticket_id` char(10) NOT NULL,
  `price` decimal(8,2) DEFAULT NULL,
  `sold_datetime` datetime NOT NULL,
  `card_type` varchar(20) DEFAULT NULL,
  `card_no` varchar(19) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `exp_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `price`, `sold_datetime`, `card_type`, `card_no`, `name`, `exp_date`) VALUES
('10023888', NULL, '2020-05-13 17:01:16', 'credit crad', '5749329854324', 'Jerry', '2024-01-01'),
('10023890', NULL, '2020-04-14 17:01:27', 'credit crad', '2321334785984', 'Tom', '2025-01-01'),
('10023891', '400.00', '2019-01-01 02:00:00', 'credit_card', '2321334785984', 'Tom', '2025-01-01'),
('10023892', '999.00', '2019-01-01 02:00:00', 'credit_card', '2321334785984', 'Tom', '2025-01-01'),
('10023893', '888.00', '2019-01-01 02:00:00', 'credit_card', '2321334785984', 'Tom', '2025-01-01'),
('10023894', '500.00', '2019-01-01 02:00:00', 'credit_card', '2321334785984', 'Tom', '2025-01-01'),
('1234567893', '959.00', '2019-04-16 17:41:46', 'credit', '1234567891234567891', 'Wang', '2020-07-15'),
('1235467123', '1023.23', '2019-02-17 17:38:29', 'credit', '123456781234789', 'Zhang', '2020-07-15'),
('1235467235', '102.23', '2019-07-17 17:38:29', 'credit', '123456781234789', 'Zhang', '2020-07-15'),
('1235467897', '658.23', '2019-12-17 17:38:29', 'credit', '123456781234789', 'Zhang', '2020-07-15'),
('1235469999', '409.23', '2019-01-17 17:38:29', 'credit', '123456781234789', 'Zhang', '2020-07-15');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD PRIMARY KEY (`user_name`),
  ADD KEY `airline` (`airline`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airplane_id`,`airline`),
  ADD KEY `airline` (`airline`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`flight_no`,`airline`,`dep_datetime`),
  ADD KEY `dept_airport` (`dep_airport`),
  ADD KEY `arr_airport` (`arr_airport`),
  ADD KEY `airline` (`airline`),
  ADD KEY `airplane_id` (`airplane_id`);

--
-- Indexes for table `phone_no`
--
ALTER TABLE `phone_no`
  ADD PRIMARY KEY (`user_name`);

--
-- Indexes for table `take`
--
ALTER TABLE `take`
  ADD PRIMARY KEY (`email`,`flight_no`,`airline`,`dep_datetime`),
  ADD KEY `flight_no` (`flight_no`,`airline`,`dep_datetime`),
  ADD KEY `ticket_id` (`ticket_id`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline`) REFERENCES `airline` (`name`) ON DELETE SET NULL;

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline`) REFERENCES `airline` (`name`) ON DELETE CASCADE;

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`dep_airport`) REFERENCES `airport` (`name`) ON DELETE CASCADE,
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`arr_airport`) REFERENCES `airport` (`name`) ON DELETE CASCADE,
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`airline`) REFERENCES `airline` (`name`) ON DELETE CASCADE,
  ADD CONSTRAINT `flight_ibfk_4` FOREIGN KEY (`airplane_id`) REFERENCES `airplane` (`airplane_id`) ON DELETE SET NULL;

--
-- Constraints for table `phone_no`
--
ALTER TABLE `phone_no`
  ADD CONSTRAINT `phone_no_ibfk_1` FOREIGN KEY (`user_name`) REFERENCES `airline_staff` (`user_name`) ON DELETE CASCADE;

--
-- Constraints for table `take`
--
ALTER TABLE `take`
  ADD CONSTRAINT `take_ibfk_1` FOREIGN KEY (`flight_no`,`airline`,`dep_datetime`) REFERENCES `flight` (`flight_no`, `airline`, `dep_datetime`) ON DELETE CASCADE,
  ADD CONSTRAINT `take_ibfk_2` FOREIGN KEY (`email`) REFERENCES `customer` (`email`) ON DELETE CASCADE,
  ADD CONSTRAINT `take_ibfk_3` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
