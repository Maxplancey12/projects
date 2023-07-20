import cv2
import numpy as np
import pyautogui
import threading
import win32api
import win32con


def capture_and_process_screenshot():
    try:
        while True:
            screen = pyautogui.screenshot()
            image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

            matches = np.where(np.all(image == [0, 250, 0], axis=-1))
            match_count = len(matches[0])

            if match_count > 0:
                center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
                distances = np.sqrt((matches[1] - center_x) ** 2 + (matches[0] - center_y) ** 2)


                closest_index = np.argmin(distances)
                end_point_x = matches[1][closest_index]
                end_point_y = matches[0][closest_index]

                cursor_x, cursor_y = win32api.GetCursorPos()
                scale_factor = 1  #Only change this if your cpu is good (Increasing this will make the bot faster but use alot of system resources)
                apx = (end_point_x - cursor_x) * scale_factor
                apy = (end_point_y - cursor_y) * scale_factor
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(apx), int(apy))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    screenshot_thread = threading.Thread(target=capture_and_process_screenshot)
    screenshot_thread.start()

    screenshot_thread.join()
