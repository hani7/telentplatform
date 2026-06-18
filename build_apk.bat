@echo off
echo.
echo ====================================================
echo FOOTOP - Android APK Build Script
echo ====================================================
echo.
echo This script will automatically trigger an Expo Application Services (EAS) build
echo to generate your Android APK in the cloud. You will be prompted to log in to
echo your Expo account if you haven't already.
echo.
pause

cd mobile
echo Using local eas.json profile...
npx eas-cli build -p android --profile preview
echo.
echo If the build is successful, EAS will provide a direct download link for your APK!
pause
