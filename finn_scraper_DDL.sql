drop table if exists listing_info;
create table listing_info (
	id serial primary key,
	arbeidsgiver text not null,
	stillingstittel text not null,
	ansettelsesform text not null,
	sektor text not null,
	bransje text not null,
	stillingsfunksjon text not null,
	url text not null,
	date_added date not null
	);