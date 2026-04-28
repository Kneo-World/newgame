[app]
title = SkibidiApp
package.name = skibidiapp
package.domain = org.kneo
source.dir = .
# Добавили xml и разрешили поиск во всех папках
source.include_exts = py,png,jpg,kv,atlas,xml,json,wav,mp3
source.include_patterns = assets/*,images/*,sounds/*,Боксы/*

version = 0.1

# Если твой код от AI Studio использует дополнительные библиотеки, добавь их через запятую
requirements = python3,kivy,pillow

orientation = portrait
fullscreen = 1

# Архитектуры оставляем как есть, это стандарт
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Иконка (если есть файл icon.png, убери решетку ниже)
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
