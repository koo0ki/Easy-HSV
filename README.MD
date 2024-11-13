# Easy HSV

Easy HSV - это простое приложение, написанное на Python, которое позволяет настраивать диапазон цветов HSV (Hue, Saturation, Value) для изображений.

## Особенности

- Выбор изображения из папки "assets"
- Регулировка диапазонов оттенка (H), насыщенности (S) и яркости (V)
- Визуальное отображение выделенных областей на изображении в реальном времени

## Требования

- Python 3.x
- Библиотеки: OpenCV, Numpy, Termcolor, Tkinter

## Установка
```bash
git clone https://github.com/koo0ki/Easy-HSV.git
pip3 install -r requirements.txt
python3 main.py
```

## Примечание
Если на линуксе программа не запускается воспользуйтесь решением ниже

- Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```     
- Fedora/CentOS/RHEL:
```bash
sudo dnf install python3-tkinter
```
- Arch Linux:
```bash
sudo pacman -S tk     
```
