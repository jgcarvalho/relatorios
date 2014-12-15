for i in {0..5}
do 
	zeca -method 9 -config ./designconfig.toml
	mv population pop_$i
done
