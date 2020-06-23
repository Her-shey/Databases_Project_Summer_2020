create table customer(
  email varchar(50),
  password  varchar(20),
  name varchar(50),
  phone_no varchar(20),
  date_of_birth date,
  passport_no char(9),
  passport_exp date,
  passport_country varchar(20),
  state varchar(50),
  city  varchar(50),
  street varchar(50),
  building_no varchar(5),
  primary key (email)
);
create table airline(
  name varchar(50),
  primary key (name)
);
create table ticket(
  ticket_id char(10),
  card_type varchar(20),
  card_no varchar(19),
  name varchar(50),
  exp_date date,
  primary key (ticket_id)
);
create table airline_staff(
  user_name varchar(50),
  password  varchar(20),
  first_name varchar(25),
  last_name varchar(25),
  date_of_birth date,
  airline varchar(50),
  primary key (user_name),
  foreign key (airline) references airline(name)
    on delete set null
);
create table phone_no(
  user_name varchar(50),
  phone_no varchar(20),
  primary key (user_name),
  foreign key (user_name) references airline_staff(user_name)
    on delete cascade
);
create table airport(
  name  varchar(50),
  city  varchar(50),
  primary key (name)
);
create table airplane(
  airplane_id char(5),
  airline varchar(50),
  capacity numeric(3, 0),
  primary key (airplane_id, airline),
  foreign key (airline) references airline(name)
    on delete cascade
);
create table flight(
  flight_no varchar(6),
  airline varchar(50),
  dep_datetime datetime,
  arr_datetime datetime,
  status varchar(10),
  base_price  numeric(8, 2),
  seat_sold numeric(3, 0),
  dept_airport  varchar(50),
  arr_airport varchar(50),
  airplane_id char(5),
  primary key (flight_no, airline, dep_datetime),
  foreign key (dept_airport) references airport(name)
    on delete cascade,
  foreign key (arr_airport) references airport(name)
    on delete cascade,
  foreign key (airline) references airline(name)
    on delete cascade,
  foreign key (airplane_id) references airplane(airplane_id)
    on delete set null
);
create table take(
  email varchar(50),
  flight_no varchar(6),
  airline varchar(50),
  dep_datetime datetime,
  rate_and_comment varchar(1000),
  ticket_id char(10),
  primary key (email, flight_no, airline, dep_datetime),
  foreign key (flight_no, airline, dep_datetime) references flight(flight_no, airline, dep_datetime)
    on delete cascade,
  foreign key (email) references customer(email)
    on delete cascade,
  foreign key (ticket_id) references ticket(ticket_id)
    on delete set null
);
