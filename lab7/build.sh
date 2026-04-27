#!/bin/bash
echo "Починаємо збірку проєкту..."
mkdir -p build
cd build
cmake ..
make
echo "Збірка успішно завершена!"
