create table expansao(
  id int not null auto_increment primary key,
  dia TIMESTAMP,
  local varchar(30) not null,
  estacao varchar(30) not null,
  cto char(13) not null,
  defeito int default 0,
  designado int default 0,
  reservado int default 0,
  ocupado int not null,
  vago int not null,
  total int not null,
  previsao_esgotamento int
);


create table concessao(
  id int not null auto_increment primary key,
  dia TIMESTAMP,
  local varchar(30) not null,
  estacao varchar(30) not null,
  cto char(13) not null,
  defeito int default 0,
  designado int default 0,
  reservado int default 0,
  ocupado int not null,
  vago int not null,
  total int not null,
  previsao_esgotamento int
);


create table cidades(
	nome varchar(30) primary key,
	tipo varchar(15) not null,
	regional varchar(30) not null
);


DELIMITER $$
CREATE FUNCTION previsao_esgotamento (nomecto CHAR(13)) RETURNS INTEGER DETERMINISTIC
BEGIN
	DECLARE maxDate TIMESTAMP;
	DECLARE minDate TIMESTAMP;
  DECLARE numDias INT;
  DECLARE ocupadoRecente INT;
  DECLARE ocupadoAntigo INT;
  DECLARE vagoRecente INT;
  DECLARE previsao INTEGER;
  DECLARE taxa FLOAT;

	SELECT MAX(dia), ocupado, vago INTO maxDate, ocupadoRecente, vagoRecente from expansao where cto = nomecto;
	SELECT MAX(dia), ocupado INTO minDate, ocupadoAntigo from expansao where cto = nomecto and dia < maxDate;
	set numDias = (SELECT TIMESTAMPDIFF(day,minDate,maxDate));
  set taxa = (ocupadoRecente - ocupadoAntigo) / numDias;
  set previsao = vagoRecente / taxa;

  RETURN previsao;

END $$
DELIMITER ;




DELIMITER $$
CREATE PROCEDURE get_time_diff (OUT diferenca INTEGER, OUT max_date TIMESTAMP, OUT min_date TIMESTAMP)
BEGIN
  SELECT MAX(dia) into max_date from expansao;
  SELECT MAX(dia) into min_date from expansao where dia < max_date;

  SET diferenca = (SELECT TIMESTAMPDIFF(day, min_date, max_date));

END $$
DELIMITER ;
