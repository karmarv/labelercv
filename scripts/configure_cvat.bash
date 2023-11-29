shopt -s extglob

ORIG="  cvat_data:"
REP="  cvat_data:
    driver: local
    driver_opts:
      type: 'none'
      o: 'bind'
      device: '~/dev/cvat_data'
"

REP="${REP//+(
)/\\n}"

sed "s/$ORIG/$REP/g"  ../cvat/docker-compose.yml >  ../cvat/docker-compose.local.yml
