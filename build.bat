@echo off
echo [🔄] .exe fayl yig‘ilishi boshlandi...

python -m PyInstaller --noconsole --onefile --icon=ideal.ico --name=IDEAL ^
--add-data "app_config.json;." ^
--add-data "deleted_phones.json;." ^
--add-data "internal_codes.json;." ^
--add-data "passwords.json;." ^
--add-data "selected_phone.json;." ^
--add-data "sold_phones.json;." ^
--add-data "sotish_file.json;." ^
--add-data "telefon_data.json;." ^
--add-data "theme_settings.json;." ^
dukon.py

echo [✅] Tayyor! dist\ideal.exe faylga o'ting.
pause
