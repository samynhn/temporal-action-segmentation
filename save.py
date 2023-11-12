import cv2

videoFile = "data/Kento_MOMOTA_CHOU_Tien_Chen_Fuzhou_Open_2019_Finals.mp4/rally_video/1_01_00.mp4"
def show_video_frames(video_path):
    # 打開影片
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 0

    while True:
        # 讀取下一幀
        ret, frame = cap.read()

        # 檢查是否成功讀取
        if not ret:
            break

        frame_count += 1

        # 將幀數顯示在畫面上
        cv2.putText(frame, f'Frame: {frame_count}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 顯示幀
        cv2.imshow('Video', frame)

        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 釋放攝影機資源並關閉視窗
    cap.release()
    cv2.destroyAllWindows()
    # print(frame_count)


def save_video_with_frame_numbers(input_video_path, output_video_path):
    # 打開影片
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # 獲取視頻的基本資訊
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 定義編碼器並創建 VideoWriter 物件
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 或者 'XVID'
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 10452

    while True:
        # 讀取下一幀
        ret, frame = cap.read()

        # 檢查是否成功讀取
        if not ret:
            break

        frame_count += 1

        # 將幀數顯示在畫面上
        cv2.putText(frame, f'Frame: {frame_count}', (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 寫入幀到輸出文件
        out.write(frame)

        # 顯示幀（可選）
        # cv2.imshow('Video', frame)

        # 按 'q' 鍵退出（如果啟用了顯示）
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # 釋放資源
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# 使用範例
save_video_with_frame_numbers(videoFile, 'result/1_01_00.mp4')

# 使用範例
# show_video_frames('your_video.mp4')
