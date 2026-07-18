import cv2
import os
import time


def main():
    # 1. НАСТРОЙКИ ПУТЕЙ И ПАРАМЕТРОВ
    video_path = "sample_video.mp4"  # Путь к вашему видеофайлу
    output_dir = "dataset_from_video"  # Папка для кадров

    # Сохраняем каждый N-й кадр (например, каждый 5-й кадр)
    # При 30 FPS каждый 5-й кадр — это 6 снимков в секунду. Оптимально для датасета!
    frame_interval = 5

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[INFO] Создана папка: '{output_dir}'")

    # 2. Открываем видеофайл вместо веб-камеры
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] Не удалось открыть видеофайл: {video_path}")
        return

    # Получаем общую информацию о видео для логов
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"[INFO] Видео успешно открыто. Всего кадров: {total_frames}, FPS: {fps:.2f}")

    frame_count = 0
    saved_count = 0
    # Генерируем одну метку времени для всей пачки файлов
    timestamp = time.ctime().replace(" ", "_").replace(":", "-")

    # 3. Цикл чтения видео
    while True:
        ret, frame = cap.read()

        # Если кадры закончились, выходим из цикла
        if not ret:
            print("[INFO] Видео полностью обработано.")
            break

        # Проверяем, нужно ли сохранять текущий кадр
        if frame_count % frame_interval == 0:
            # 1. ЗАДАЕМ НОВЫЙ РАЗМЕР (Ширина, Высота)
            # Для нейросетей часто используют квадратные форматы, например, 640x640
            new_size = (640, 640)

            # 2. СЖИМАЕМ КАДР
            # cv2.INTER_AREA — это лучший алгоритм интерполяции именно для уменьшения картинок
            resized_frame = cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)

            # 3. ГЕНЕРИРУЕМ ИМЯ И СОХРАНЯЕМ СЖАТЫЙ КАДР
            img_name = f"vid_{timestamp}_{saved_count:04d}.jpg"
            img_path = os.path.join(output_dir, img_name)

            # Сохраняем resized_frame вместо оригинального frame
            cv2.imwrite(img_path, resized_frame)
            saved_count += 1

        frame_count += 1

        # Показываем процесс нарезки (опционально)
        cv2.imshow("Processing Video...", frame)

        # Нарезку можно прервать, нажав клавишу 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Обработка прервана пользователем.")
            break

    # 4. Освобождаем ресурсы
    cap.release()
    cv2.destroyAllWindows()
    print(f"[SUCCESS] Нарезка завершена! Сохранено кадров: {saved_count}")


if __name__ == "__main__":
    main()
