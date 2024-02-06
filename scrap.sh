windupbox os list -f 'architecture=x64, language=English' -fi > w.data

while read p;
do
    if [ ! -z "$p" ];
    then
        windupbox os download "$p"
    fi
    break
done < w.data