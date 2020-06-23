#Database Project Part 2 Query
#Zachary Zeng  #nz900
#Robert Zhu     #xz1947
#Lewis Liu     #hl2977



#a. Show all the future flights in the system.

SELECT airline,flight_no,dep_datetime, dept_airport, arr_airport
FROM flight
WHERE dep_datetime > NOW();

#b. Show all of the delayed flights in the system.

SELECT airline, flight_no, dep_datetime
FROM flight 
WHERE status = 'delay';

#c. Show the customer names who bought the tickets.

SELECT name
FROM customer
WHERE email IN
(SELECT email
FROM take);

#d. Show all of the airplanes owned by the airline (such as "Emirates")

SELECT airline, airplane_id
FROM airplane
WHERE airline = 'Emirates';
