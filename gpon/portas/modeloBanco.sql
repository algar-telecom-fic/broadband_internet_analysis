create table expansao(
  id int not null auto_increment primary key,
  dia TIMESTAMP default CURRENT_TIMESTAMP,
  local varchar(30) not null,
  estacao varchar(30) not null,
  cto char(13) not null,
  defeito int default 0,
  designado int default 0,
  reservado int default 0,
  ocupado int not null,
  vago int not null,
  total int not null
);


create table concessao(
  id int not null auto_increment primary key,
  dia TIMESTAMP default CURRENT_TIMESTAMP,
  local varchar(30) not null,
  estacao varchar(30) not null,
  cto char(13) not null,
  defeito int default 0,
  designado int default 0,
  reservado int default 0,
  ocupado int not null,
  vago int not null,
  total int not null
);


create table cidades(
	nome varchar(30) primary key,
	tipo varchar(15) not null,
	regional varchar(30) not null
);


DELIMITER $$
CREATE PROCEDURE compara_datas (IN nomecto CHAR(13))
BEGIN
	DECLARE maxDate TIMESTAMP;
	DECLARE minDate TIMESTAMP;
  DECLARE numDias INT;
  DECLARE ocupadoRecente INT;
  DECLARE ocupadoAntigo INT;
  DECLARE vagoRecente INT;
  DECLARE previsao INT;
  DECLARE taxa FLOAT;


	SELECT MAX(dia) INTO maxDate from expansao where cto = nomecto;
	SELECT MAX(dia) INTO minDate from expansao where cto = nomecto and dia < maxDate;

	set numDias = (SELECT TIMESTAMPDIFF(day,minDate,maxDate));
  SELECT ocupado, vago into ocupadoRecente, vagoRecente FROM expansao where cto=nomecto and dia = maxDate limit 1;
  SELECT ocupado into ocupadoAntigo FROM expansao WHERE cto=nomecto and dia = minDate limit 1;

  set taxa = (ocupadoRecente - ocupadoAntigo) / numDias;
  set previsao = vagoRecente / taxa;
  select previsao as Previsao_em_dias;

END $$
DELIMITER ;
