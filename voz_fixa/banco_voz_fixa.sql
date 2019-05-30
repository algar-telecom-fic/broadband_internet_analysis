CREATE TABLE faixa_stfc(
  id int not null auto_increment primary key,
  cidade varchar(30) not null,
  ddd char(2) not null,
  total_recurso INT not null default 0,
  total_comum INT not null default 0,
  dia TIMESTAMP
);

CREATE TABLE area_local(
  id int not null auto_increment primary key,
  cidade varchar(30) not null,
  areaLocal varchar(30) not null,
  tecnologia varchar(30) not null,
  ATIVO INT not null default 0,
  CONGELADO INT not null default 0,
  DEFEITO INT not null default 0,
  DESIGNADO INT not null default 0,
  DISPONIVEL INT not null default 0,
  EXCLUIDO INT not null default 0,
  INDISPONIVEL INT not null default 0,
  INTERCEPTADO INT not null default 0,
  OCUPADO INT not null default 0,
  `OCUPADO DDR` INT not null default 0,
  PORTADO INT not null default 0,
  `PORTADO CANCELADO` INT not null default 0,
  `RESERVA TECNICA` INT not null default 0,
  `RESERVA TP` INT not null default 0,
  RESERVADO INT not null default 0,
  `RESERVADO ANATEL` INT not null default 0,
  `RESERVADO DDR` INT not null default 0,
  `RESERVADO PLIGG` INT not null default 0,
  `TP DESIGNADO` INT not null default 0,
  `TP RESERVADO` INT not null default 0,
  dia TIMESTAMP
);
