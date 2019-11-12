create table mgw(
	id int not null auto_increment primary key,
	Localidade varchar(50) not null,
	Estacao varchar(50),
	Elemento varchar(15),
	Capacidade int default 0,
	Ocupado int default 0,
	Disponivel int default 0,
	Crescimento int default 0,
	Esgotamento_M varchar(25),
	Esgotamento int default 0,
	Taxa_Ocupacao int default 0,
	Dia TIMESTAMP
);
