#
# Configure the docker-compose.yml to persist data to a local folder path
#
SRC_CONFIG="../cvat/docker-compose.yml"
TGT_CONFIG="../cvat/docker-compose.local.yml"
sed -e '381,387d' $SRC_CONFIG > ./docker-compose.tmp.yml
awk 'NR==FNR{n=n s $0; s=ORS; next} {print} FNR==381{print n}' tmp_cvat.conf ./docker-compose.tmp.yml > docker-compose.local.yml
cp docker-compose.local.yml $TGT_CONFIG
echo "Updated the $TGT_CONFIG with local data folder configuration"
rm ./docker-compose.tmp.yml