version=18.6.0
stube_ver=18.3.0
themes_ver=18.6.0
skins_ver=15.2.0

git pull

sed -i "s|^%global smtube_ver .*|%global smtube_ver $stube_ver|" smplayer.spec
sed -i "s|^%global smplayer_themes_ver .*|%global smplayer_themes_ver $themes_ver|" smplayer.spec
sed -i "s|^%global smplayer_skins_ver .*|%global smplayer_skins_ver $skins_ver|" smplayer.spec

rpmdev-bumpspec -n $version -c "Update smplayer to $version" smplayer.spec
spectool -g smplayer.spec
rfpkg new-sources ./smplayer-$version.tar.bz2 ./smtube-$stube_ver.tar.bz2 ./smplayer-themes-$themes_ver.tar.bz2 ./smplayer-skins-$skins_ver.tar.bz2
rfpkg ci -c && git show
echo Press enter to continue; read dummy;
rfpkg push && rfpkg build --nowait
echo Press enter to continue; read dummy;
git checkout f28 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout f27 && git merge master && git push && rfpkg build --nowait; git checkout master
echo Press enter to continue; read dummy;
git checkout el7 && git merge master && git push && rfpkg build --nowait; git checkout master
