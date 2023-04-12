#!/bin/sh
echo "check_certificate = off" >> ~/.wgetrc
echo "Update feeds"
opkg update
echo " "
echo "Install EpgImporter"
opkg --force-reinstall --force-overwrite install enigma2-plugin-extensions-epgimport
echo 'config.plugins.epgimport.enabled=true' >> /etc/enigma2/settings;
echo 'config.plugins.epgimport.longDescDays=5' >> /etc/enigma2/settings;
echo 'config.plugins.epgimport.wakeup=6:0' >> /etc/enigma2/settings;
exit 0
