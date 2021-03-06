#!/bin/bash

folder="stocks/"
item="item.json"
nn="nn.json"
csv="nn.csv"

pre=($(date "+%Y%m%d-%H%M%S-"))

pushd ~/workspace/projects/nn/

touch $nn
echo "[]" > $nn

elementes=($(/usr/bin/php  select_sym_nikkei225.php))
# pushd ${folder}
# elementes=($(ls -d *))
# popd

nmbr_of_elements=${#elementes[@]}
# echo ${nmbr_of_elements}
# perform every element
for (( i = 0 ; i < nmbr_of_elements ; i++ ))
do
   code=${elementes[$i]}
   sym=${folder}${code}

   # Secure new output folder
   OUT_DIR=$sym/out
   NEW_DIR=`dirname $OUT_DIR`
   [ ! -d $NEW_DIR ] && mkdir -p $NEW_DIR
   mkdir -p $OUT_DIR

   touch $sym/out/${item}
   echo "[{" > $sym/out/${item}

   python readCsv2.py $sym

   python writeCsv2.py $sym > $sym/out/new.txt
   rm -rf /tmp/iris_model/

   python tfCsv2.py $sym

   pushd iris
   cp -f ../$sym/out/iris_test.csv ../$sym/out/iris_training.csv ../$sym/out/input.csv  .
   python pqs.py $code

   echo "}]" >> ../$sym/out/${item}
   popd

   python nn.py $sym

   # real-time update, for 1st time
   # cp $nn  $pre$nn
   # sudo cp $nn  $csv /var/www/html/nn/
done

# pre=($(date "+%Y%m%d-%H%M%S-"))

cp $nn  $pre$nn
sudo cp $nn  $csv  /var/www/html/nn/

rm  backup.zip
zip backup.zip stocks -r
sudo cp -f backup.zip /var/www/html/nn/

popd

