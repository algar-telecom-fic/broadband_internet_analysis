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
  OCUPADO_DDR INT not null default 0,
  PORTADO INT not null default 0,
  PORTADO_CANCELADO INT not null default 0,
  RESERVA_TECNICA INT not null default 0,
  RESERVA_TP INT not null default 0,
  RESERVADO INT not null default 0,
  RESERVADO_ANATEL INT not null default 0,
  RESERVADO_DDR INT not null default 0,
  RESERVADO_PLIGG INT not null default 0,
  TP_DESIGNADO INT not null default 0,
  TP_RESERVADO INT not null default 0,
  dia TIMESTAMP
);
