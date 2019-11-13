version=19.10.2
#stube_ver=19.6.0
themes_ver=18.6.0
skins_ver=15.2.0

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
rfpkg new-sources ./smplayer-$version.tar.bz2 ./smplayer-themes-$themes_ver.tar.bz2 ./smplayer-skins-$skins_ver.tar.bz2
rfpkg ci -c && git show
fi
if test $stage -le 1
then
echo STAGE 1
echo Press enter to continue; read dummy;
rfpkg push && rfpkg build --nowait
echo Press enter to continue; read dummy;
git checkout f31 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout f30 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout f29 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout el7 && git merge master && git push && rfpkg build --nowait; git checkout master
fi
