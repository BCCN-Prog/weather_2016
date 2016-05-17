#This script downloads the original folders from the ftp servers and creates some directories that will be filled by 

wget wget --mirror -p --convert-links -P . ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/recent/ ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/historical/ ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/ 
find . -type d -exec sh -c "cd \"{}\" ; unzip \"*.zip\" "produkt\*.txt" " \;

mkdir daily_data_clean
mkdir hourly_data
mkdir hourly_data_clean
