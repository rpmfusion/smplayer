version=21.1.0
#stube_ver=19.6.0
themes_ver=20.11.0
skins_ver=20.11.0
REPOS="f33 f32 el8 el7"

if [ -z "$1" ]
then
      stage=0
else
      stage=$1
fi

if test $stage -le 0
then
echo STAGE 0
git checkout master && git pull || exit 2

#sed -i "s|^%global smtube_ver .*|%global smtube_ver $stube_ver|" smplayer.spec
sed -i "s|^%global smplayer_themes_ver .*|%global smplayer_themes_ver $themes_ver|" smplayer.spec
sed -i "s|^%global smplayer_skins_ver .*|%global smplayer_skins_ver $skins_ver|" smplayer.spec

if [[ -z $2 ]]; then
MSG="Update smplayer to $version"
else
MSG=$2
fi
if [[ -z $3 ]]; then
rpmdev-bumpspec -n $version -c "$MSG" smplayer.spec
else
rpmdev-bumpspec -c "$MSG" smplayer.spec
fi

spectool -g smplayer.spec
rfpkg scratch-build --srpm --nowait
echo Press enter to upload sources and commit; read dummy;
rfpkg new-sources ./smplayer-$version.tar.bz2 ./smplayer-themes-$themes_ver.tar.bz2 ./smplayer-skins-$skins_ver.tar.bz2
rfpkg ci -c && git show
fi
if test $stage -le 1
then
echo STAGE 1
echo Press enter to push and build in rawhide; read dummy;
rfpkg push && rfpkg build --nowait
fi

if test $stage -le 2
then
for repo in $REPOS ; do
echo Press enter to build on branch $repo; read dummy;
git checkout $repo && git merge master && git push && rfpkg build --nowait; git checkout master
done
fi
