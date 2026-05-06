.\wgrib2 file.grib2  -undefine out-box  2:8 50:54 -csv output.csv 
copy (select STATIONS_ID::int stn,MESS_DATUM_BEGINN::int//10000 as y,MESS_DATUM_ENDE::int // 100 % 100 as m,
 round_even(MO_TT*10,0)::int tg,round_even(MO_TX*10,0)::int tx ,round_even(MO_TN*10,0)::int tn,
         round_even(MO_FK*10,0)::int fk,round_even(MX_TX*10,0)::int xtx,round_even(MX_FX*10,0)::int xfx,
		 round_even(MX_TN*10,0)::int xtn,round_even(MO_SD_S*10,0)::int sds
		 ,round_even(MO_RR*10,0)::int rr,round_even(MX_RS*10,0)::int xrs,QN_4::smallint qn4,QN_6::smallint qn6 from t) to 'm.parquet' (COMPRESSION 'zstd')

copy (
select cast(STATIONS_ID as int) stn,
cast(MESS_DATUM as int) yyyymmdd, 
round_even(cast(fm as float) * 10,0)::int fg,
round_even(cast(fx as float) * 10,0)::int fx,
round_even(cast(rsk as float) * 10,0)::int rh,
round_even(cast(rskf as float) * 10,0)::int rf,
round_even(cast(sdk as float) * 10,0)::int sq,
round_even(cast(shk_tag as float) * 10,0)::int shk,
round_even(cast(vpm as float) * 10,0)::int pm,
round_even(cast(pm as float) * 10,0)::int pg,
round_even(cast(tmk as float) * 10,0)::int tg,
round_even(cast(upm as float) * 10,0)::int ug,
round_even(cast(txk as float) * 10,0)::int tx,
round_even(cast(tnk as float) * 10,0)::int tn,
round_even(cast(tgk as float) * 10,0)::int t5n,
round_even(cast(nm as float) * 10,0)::int ng
 from t) to 'dd.parquet' (COMPRESSION 'zstd');


copy (select "DateTime(UTC)" dt, ResolutionCode rc, AreaCode ac , AreaDisplayName adn, AreaTypeCode atc,AreaMapCode amc, ProductionType pt,
         "ActualGenerationOutput[MW]" ago, "ActualConsumption[MW]" aci,  "UpdateTime(UTC)" ut from ontime) to 'g.parquet' (COMPRESSION 'zstd');

prijs
copy (select  strftime("DateTime(UTC)", '%Y%m%d')::int d, strftime("DateTime(UTC)", '%H%M')::int t,
 ResolutionCode r, AreaCode a ,
	AreaDisplayName ad, AreaTypeCode as at, MapCode m, 
         nullif(trim(Sequence),'')::int s, ("Price[Currency/MWh]"*100)::int p,  Currency c, "UpdateTime(UTC)" ut , InstanceCode i from p) 
		
		 to 'p.parquet' (COMPRESSION 'zstd');
		 		 

copy (select d, t, dt, rc,  ac ,  adn,  atc, amc,  pt,   ago,  aci,  du, tu from g) to 'g.parquet' (COMPRESSION 'zstd');

copy (select station stn, element e, timefunction tf, dt, value v, flag flg, quality qlt from t) to 'd:\d.parquet' (COMPRESSION 'zstd');


copy (select dat//100 dat, round_even(t,0)::int t from t1) to '2290.parquet' ;

DROP TABLE t;
CREATE TABLE t AS SELECT * FROM read_csv('d:\data\w\d\d\zip\pr*.*', all_varchar=True);
DROP TABLE t;CREATE TABLE t AS SELECT * FROM read_csv('dag.csv', auto_type_candidates = ['BIGINT']);
 
 COPY (
           SELECT
             time::INT AS yyyymmdd,
             latitude::INT AS lat,
             longitude::INT AS lon, 
			 fg::SMALLINT AS fg
			FROM t
			ORDER BY time
         ) TO 'cfg.parquet');
		 
COPY (
    SELECT t1.yyyymmdd, t1.lat, t1.lon, fg,  pp
    FROM 'cfg.parquet' t1 
    LEFT JOIN 'cpp.parquet' t2 ON t1.yyyymmdd = t2.yyyymmdd and t1.lat = t2.lat and t1.lon-0.1*10000000 = t2.lon
	ORDER BY t1.yyyymmdd
) TO 'fg_pp.parquet' (FORMAT PARQUET);


daily mean temperature TG, 
daily minimum temperature TN, 
daily maximum temperature TX, 
daily precipitation sum RR, 
daily averaged sea level pressure PP, 
daily averaged relative humidity HU, 
daily mean wind speed FG and 
daily mean global radiation QQ
 copy (SELECT
             yyyymmdd,
                AVG(rh) OVER (
                 ORDER BY yyyymmdd
                 ROWS BETWEEN 273* PRECEDING AND CURRENT ROW
             )::int as vg
         FROM dag2.parquet
         WHERE yyyymmdd>20000000 and  stn=260 and fg is not null order by 2) to 'vg260_10.csv'
         ;
