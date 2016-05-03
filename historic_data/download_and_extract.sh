wget wget --mirror -p --convert-links -P . ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/recent/ ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/historical/ ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/ 
find . -type d -exec sh -c "cd \"{}\" ; unzip \"*.zip\" "produkt\*.txt" " \;

mkdir clean_data
