update Regular_17_18
set
	gameDate = printf('%s-%s-%s', cast(substr(gameDate,7,4) as text), cast(substr(gameDate,0,3) as text), cast(substr(gameDate,4,2) as text))