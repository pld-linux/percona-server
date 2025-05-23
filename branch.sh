#!/bin/sh
set -e
url=https://github.com/percona/percona-server.git
package=percona-server
tagbase=Percona-Server-5.7.44-48
tagnew=Percona-Server-5.7.44-52
branch=5.7
out=$package-git.patch
repo=$package.git

# use filterdiff, etc to exclude bad chunks from diff
filter() {
	filterdiff \
	-x '*/build-ps/*'
}

if [ ! -d $repo ]; then
	git clone --bare $url -b $branch $repo
fi

cd $repo
	git fetch origin +$branch:$branch +refs/tags/$tagbase:refs/tags/$tagbase +refs/tags/$tagnew:refs/tags/$tagnew
	git log -p --date=default --reverse $tagbase..$tagnew | filter > ../$out.tmp
cd ..

if cmp -s $out{,.tmp}; then
	echo >&2 "No new diffs..."
	rm -f $out.tmp
	exit 0
fi
mv -f $out{.tmp,}

../md5 $package.spec
../dropin $out
