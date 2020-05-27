pyinstaller -n SpeechShadowApp --onefile  main.py
publishDir="./allbuilds/Linux-$(lsb_release -ds)"

mkdir -p "$publishDir"
cp ./dist/SpeechShadowApp "$publishDir"
cp ./README.MD "$publishDir"