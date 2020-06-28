#Database Project Part 2 Insersion
#Zachary Zeng  #nz900
#Robert Zhu     #xz1947
#Lewis Liu     #hl2977


insert into airline values('China Eastern');
insert into airport values('JFK','NYC');
insert into airport values('PVG','Shanghai');
insert into customer values ('123@gmail.com',MD5('123'),'Tom','123123123','1990-01-01','AGHJGKHGV','2020-01-01','China','Guangdong','Guangzhou','Jianshe','12345' );
insert into customer values ('456@gmail.com',MD5('456'),'Jery','456456456','1990-02-02','BYTDCGNJH','2020-02-02','China','Hubei','Wuhan','Dongchuan','54321' );
insert into airplane values ('ABCDE','China Eastern','200');
insert into airplane values ('AAABB','China Eastern','200');
insert into airline_staff values('Jack','123456','Xiao','Ming','1990-02-04','China Eastern');
insert into flight values ('AA111','China Eastern','2019-01-01 02:00:00','2019-01-01 11:00:00','on-time','500','100','JFK','PVG','ABCDE');
insert into flight values ('AA111','China Eastern','2019-01-02 02:00:00','2019-01-02 11:45:30','delay','400','80','JFK','PVG','ABCDE');
insert into flight values ('AA111','China Eastern','2019-01-03 02:00:00','2019-01-03 11:00:00','on-time','500','120','JFK','PVG','ABCDE');
insert into flight values ('AA111','China Eastern','2019-01-04 02:00:00','2019-01-04 11:58:45','delay','999','50','JFK','PVG','ABCDE');
insert into flight values ('AA888','China Eastern','2022-01-04 02:00:00',null,null,'888','50','PVG','JFK','AAABB');
insert into ticket values ('10023890','credit crad','2321334785984','Tom','2025-01-01', '2019-01-01 02:00:00');
insert into ticket values ('10023888','credit crad','5749329854324','Jerry','2024-01-01', '2019-01-01 05:00:00');
insert into take values ('456@gmail.com','AA111','China Eastern','2019-01-02 02:00:00','Good','10023888');
insert into take values ('123@gmail.com','AA111','China Eastern','2019-01-02 02:00:00','The service is good','10023890');
