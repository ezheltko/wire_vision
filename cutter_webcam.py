import cv2
import os
import time


def main():
    # 1. Создаем папку для сохранения будущих кадров датасета
    output_dir = "dataset_raw"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[INFO] Создана папка для кадров: '{output_dir}'")

    # 2. Инициализируем камеру. 0 — это индекс встроенной или первой USB-камеры
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Не удалось открыть камеру. Проверьте подключение.")
        return

    # 3. НАСТРОЙКА КАМЕРЫ (Критически важно для компьютерного зрения!)
    # Принудительно отключаем автофокус (0 = выкл)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    # Отключаем автоэкспозицию (зависит от драйвера камеры, часто -3 или 1)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)

    # Задаем разрешение кадра (например, Full HD 1920x1080 или HD 1280x720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("\n=== Управление скриптом ===")
    print("Нажмите [ПРОБЕЛ] — чтобы сделать снимок для датасета")
    print("Нажмите [Q]      — чтобы выйти из программы\n")

    img_counter = 0

    # 4. Главный бесконечный цикл обработки видеопотока
    while True:
        # Считываем текущий кадр с камеры
        ret, frame = cap.read()

        # Если кадр не считался (например, камеру отключили), выходим
        if not ret:
            print("[ERROR] Не удалось получить кадр с камеры.")
            break

        # Создаем копию кадра, на которой нарисуем визуальные подсказки
        #Если рисовать зеленый круг и текст прямо на исходном кадре (frame), то при нажатии пробела
        # эти рисунки сохранятся на диск вместе с изображением.
        display_frame = frame.copy()

        # Рисуем по центру экрана прицел-окружность, куда сборщик должен подносить разъем
        h, w, _ = display_frame.shape
        center = (w // 2, h // 2)
        cv2.circle(display_frame, center, 250, (0, 255, 0), 2)  # Зеленый круг радиусом 100
        cv2.putText(display_frame, "Place the connector here", (center[0]-145, center[1] -270),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Выводим количество уже сохраненных кадров на экран
        cv2.putText(display_frame, f"Saved: {img_counter}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

        # Показываем окно с видеопотоком
        cv2.imshow("Production Camera MVP", display_frame)

        # 5. Обработка нажатий клавиш (ожидание 1 миллисекунду)
        key = cv2.waitKey(1) & 0xFF

        # Если нажат 'q' — закрываем программу
        if key == ord('q'):
            print("[INFO] Завершение работы...")
            break

        # Если нажат 'Пробел' — сохраняем ЧИСТЫЙ кадр (без зеленого круга и текста!)
        elif key == ord(' '):
            img_name = f"img_{int(time.time())}_{img_counter}.jpg"
            img_path = os.path.join(output_dir, img_name)

            # Сохраняем именно frame (оригинал), а не display_frame (с графикой)
            cv2.imwrite(img_path, frame)

            print(f"[OK] Кадр сохранен: {img_path}")
            img_counter += 1

    # 6. Освобождаем ресурсы камеры и закрываем окна
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
