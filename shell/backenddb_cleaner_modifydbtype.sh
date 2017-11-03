#!/bin/bash

if [ $# != 1 ]; then
    echo "usage: $0 path-to-backenddb"
    exit -1
fi

dbDir=$1
num=0

echo "Cleaning $dbDir..."

for db in `ls $dbDir`
do
    BASE_DB_NAME=`basename $db`
    SEG_ID=`echo ${BASE_DB_NAME} | awk -F"[_\.]" '{print $2}'`
    echo $SEG_ID
    true >  xxx.txt
    chmod a+w xxx.txt
   # sqlite3 ${dbDir}/${db} ".output /home/test/Documents/NURBS/xxx.txt"
    sqlite3 ${dbDir}/${db} "select * from Section_${SEG_ID};" > ${SEG_ID}.txt
   # sqlite3 ${dbDir}/${db} ".output stdout"
    sqlite3 ${dbDir}/${db} "drop table Section_${SEG_ID}"
    sqlite3 ${dbDir}/${db} "CREATE table if not exists Section_${SEG_ID}(ID                UNSIGNED BIG INT, SegID               INTEGER,LeftNeighbourIDs    TEXT, RightNeighbourIDs   TEXT,PassSegmentIDs TEXT,NodeIDA             UNSIGNED BIG INT, NodeIDB             UNSIGNED BIG INT, TrajectoryType      UNSIGNED INTEGER, GPSTrajectory       TEXT, Overlaps            TEXT, Status              INTEGER, Primary Key(ID));"
    #`chmod +x ${SEG_ID}.txt`
    `sed -i "1d" ${SEG_ID}.txt`
    `sed -ie 's/|/| |/4' ${SEG_ID}.txt`
    sqlite3 ${dbDir}/${db} ".separator "\|""
    sqlite3 ${dbDir}/${db} ".import ${SEG_ID}.txt Section_${SEG_ID}"  
    
    echo "Starting $SEG_ID"

    sqlite3 ${dbDir}/${db} "delete from Reference_${SEG_ID};"
    sqlite3 ${dbDir}/${db} "delete from RoadGeometry_${SEG_ID};"
    sqlite3 ${dbDir}/${db} "update Section_${SEG_ID} set LeftNeighbourIDs = replace(LeftNeighbourIDs, ',', ',0;') where LeftNeighbourIDs like '%,%' ;"
    sqlite3 ${dbDir}/${db} "update Section_${SEG_ID} set RightNeighbourIDs = replace(RightNeighbourIDs, ',', ',0;') where RightNeighbourIDs like '%,%' ;"
    sqlite3 ${dbDir}/${db} "update Section_${SEG_ID} set LeftNeighbourIDs = LeftNeighbourIDs||',0' where trim(LeftNeighbourIDs) != '' ;"
    sqlite3 ${dbDir}/${db} "update Section_${SEG_ID} set RightNeighbourIDs = RightNeighbourIDs||',0' where trim(RightNeighbourIDs) != '' ;"
    sqlite3 ${dbDir}/${db} "update DBVersion set VERSION = 106;"
    sqlite3 ${dbDir}/${db} vacuum
    echo "Done!"
done
