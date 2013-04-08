#!/usr/bin/python

# Some channels
channels=dict();
channels["ARD"]          = "frequency=11836000:polarization=H:srate=27500000 --program=28106";
channels["ZDF"]          = "frequency=11953500:polarization=H:srate=27500000 --program=28006";
channels["WDR"]          = "frequency=12421500:polarization=H:srate=27500000 --program=28327";
channels["RTL"]          = "frequency=12187000:polarization=H:srate=27500000 --program=12003";
channels["SAT1"]         = "frequency=12544000:polarization=H:srate=22000000 --program=17500";
channels["PRO7"]         = "frequency=12544000:polarization=H:srate=22000000 --program=17501";
channels["KABEL1"]       = "frequency=12544000:polarization=H:srate=22000000 --program=17502";
channels["VOX"]          = "frequency=12187500:polarization=H:srate=22000000 --program=12060";
channels["SPORT1"]       = "frequency=12480000:polarization=V:srate=27500000 --program=900";
channels["EUROSPORT"]    = "frequency=12226000:polarization=H:srate=27500000 --program=31200";
channels["EINSFESTIVAL"] = "frequency=10743800:polarization=H:srate=22000000 --program=28722";
channels["EINSPLUS"]     = "frequency=10743800:polarization=H:srate=22000000 --program=28723";
channels["ZDFNEO"]       = "frequency=11953500:polarization=H:srate=27500000 --program=28014";
channels["ZDFKULTUR"]    = "frequency=11953500:polarization=H:srate=27500000 --program=28016";
channels["ZDFINFO"]      = "frequency=11953500:polarization=H:srate=27500000 --program=28011";
channels["HR"]           = "frequency=11836500:polarization=H:srate=27500000 --program=28108";
channels["BRALPHA"]      = "frequency=12265500:polarization=H:srate=27500000 --program=28487";
channels["MDR"]          = "frequency=12109500:polarization=H:srate=27500000 --program=28230";
channels["NDR"]          = "frequency=12109500:polarization=H:srate=27500000 --program=28227";
channels["SR"]           = "frequency=12265500:polarization=H:srate=27500000 --program=28486";
channels["SWR"]          = "frequency=11836500:polarization=H:srate=27500000 --program=28113";
channels["KIKA"]         = "frequency=11953500:polarization=H:srate=27500000 --program=28008";
channels["ARTE"]         = "frequency=10743800:polarization=H:srate=22000000 --program=28724";
channels["N24"]          = "frequency=12544800:polarization=H:srate=22000000 --program=17503";
channels["PHOENIX"]      = "frequency=10743800:polarization=H:srate=22000000 --program=28725";
channels["DMAX"]         = "frequency=12480000:polarization=V:srate=27500000 --program=63";

channels["BBC1"]      = "frequency=10773000:polarization=H:srate=22000000 --program=6301 --dvb-satno=2";
channels["BBC2"]      = "frequency=10773000:polarization=H:srate=22000000 --program=6302 --dvb-satno=2";
channels["ITV1"]      = "frequency=10758000:polarization=V:srate=22000000 --program=10060 --dvb-satno=2";
channels["ITV1+1"]    = "frequency=10891000:polarization=H:srate=22000000 --program=10145 --dvb-satno=2";
channels["ITV2"]      = "frequency=10758000:polarization=V:srate=22000000 --program=10070 --dvb-satno=2";
channels["ITV2+1"]    = "frequency=10891000:polarization=H:srate=22000000 --program=10165 --dvb-satno=2";
channels["ITV3"]      = "frequency=10906000:polarization=V:srate=22000000 --program=10260 --dvb-satno=2";
channels["ITV3+1"]    = "frequency=10906000:polarization=V:srate=22000000 --program=10261 --dvb-satno=2";
channels["ITV4"]      = "frequency=10758000:polarization=V:srate=22000000 --program=10072 --dvb-satno=2";
channels["ITV4"]      = "frequency=10832000:polarization=H:srate=22000000 --program=10015 --dvb-satno=2";
channels["E4"]        = "frequency=10729000:polarization=V:srate=22000000 --program=8305 --dvb-satno=2";
channels["E4+1"]      = "frequency=10729000:polarization=V:srate=22000000 --program=8300 --dvb-satno=2";
channels["MORE4"]     = "frequency=10729000:polarization=V:srate=22000000 --program=8340 --dvb-satno=2";
channels["MORE4+1"]   = "frequency=10714000:polarization=H:srate=22000000 --program=9230 --dvb-satno=2";
channels["FILM4"]     = "frequency=10714000:polarization=H:srate=22000000 --program=9220 --dvb-satno=2";
channels["FILM4+1"]   = "frequency=10714000:polarization=H:srate=22000000 --program=9225 --dvb-satno=2";