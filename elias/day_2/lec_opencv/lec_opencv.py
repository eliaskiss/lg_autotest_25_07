import cv2
from icecream import ic
from datetime import datetime
import time

ic.configureOutput(includeContext=True)

# VideoCaptureAPIs 열거형 상수	설명
# CAP_ANY	자동 선택
# CAP_V4L, CAP_V4L2	V4L/V4L2(리눅스)
# CAP_FIREWIRE, CAP_FIREWARE, CAP_IEEE1394	IEEE 1394 드라이버
# CAP_DSHOW	다이렉트쇼(DirectShow)
# CAP_PVAPI	PvAPI, Prosilica GigE SDK
# CAP_OPENNI	OpenNI
# CAP_MSMF	마이크로소프트 미디어 파운데이션
# (Microsoft Media Foundation)
# CAP_GSTREAMER	GStreamer
# CAP_FFMPEG	FFMPEG 라이브러리
# CAPIMAGES	OpenCV에서 지원하는 일련의 영상 파일 (예) img%02d.jpg
# CAP_OPENCV_MJPEG	OpenCV에 내장된 MotionJPEG 코덱

class WebCam:
    def __init__(self, portNum=None):
        self.port_num = portNum

    ###################################################################
    # Get WebCam List
    ###################################################################
    def get_valid_camera_list(self, max_port_num=3):
        camera_port_list = []

        for index in range(max_port_num):
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            ret, frame = cap.read()

            if ret is True and frame is not None:
                camera_port_list.append(index)
            else:
                break

        return camera_port_list

    ###################################################################
    # Set Port Number
    ###################################################################
    def set_port(self, portNum):
        self.port_num = portNum

    ###################################################################
    # Capture Webcam Image
    ###################################################################
    def capture_image(self, file_name, width=1280, height=720):
        # 웹캠 객체생성
        cap = cv2.VideoCapture(self.port_num, cv2.CAP_DSHOW) # Windows Directshow 사용

        # 웹캠 옵션설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

        # 카메라 이미지 캡쳐
        ret, frame = cap.read()

        # 캡쳐된 이미지를 파일로 저장
        if ret is True:
            ret = cv2.imwrite(file_name, frame)

        # 객체핸들 릴리즈
        cap.release()

        return ret, file_name

    ###################################################################
    # Capture Video Stream
    ###################################################################
    def capture_video(self, width=1280, height=720, isMono=False, flip=None):
        # 웹캠 객체생성
        cap = cv2.VideoCapture(self.port_num, cv2.CAP_DSHOW)

        # 웹캠 옵션설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

        while True:
            # 현재 영상 캡쳐
            ret, frame = cap.read()

            # 캡쳐 실패시 실행중단
            if ret is False:
                break

            # 흑백전환
            if isMono is True:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            # 플립적용
            if flip is not None:
                # flip: 0 -> bottom to top, 1 -> left to right
                frame = cv2.flip(frame, flip)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        # 객체핸들 릴리즈
        cap.release()

        # 윈도우 닫기
        cv2.destroyWindow('frame')
        # cv2.destroyAllWindows()

    ###################################################################
    # Record Video Stream with AVI codec
    ###################################################################
    def record_video(self, video_file_name, fps=None, width=1280, height=720, flip=None):
        # 웹캠 객체생성
        cap = cv2.VideoCapture(self.port_num, cv2.CAP_DSHOW)
        # cap = cv2.VideoCapture(self.port_num)

        # 웹캠 옵션설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

        # 코덱설정
        # fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')

        # 실제 적용된 크기
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                      int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # FPS 확인
        if fps is None:
            fps = cap.get(cv2.CAP_PROP_FPS)
        ic(fps)

        # Writer 객체
        out = cv2.VideoWriter(f'{video_file_name}.avi', fourcc, fps, frame_size)

        while True:
            # 현재 영상 캡쳐
            ret, frame = cap.read()

            # 캡쳐 실패시 실행중단
            if ret is False:
                break

            # 플립적용
            if flip is not None:
                frame = cv2.flip(frame, flip)

            # 윈도우 화면에 영상출력
            cv2.imshow('frame', frame)

            # 동영상파일에 Frame 저장
            out.write(frame)

            if cv2.waitKey(1) == ord('q'):
                break

        # 객체핸들 릴리즈
        cap.release()

        # 윈도우 닫기
        cv2.destroyWindow('frame')
        # cv2.destroyAllWindows()

    ###################################################################
    # Play Video File
    ###################################################################
    def play_video(self, file_name):
        # 웹캠 객체생성
        cap = cv2.VideoCapture(file_name)
        fps = cap.get(cv2.CAP_PROP_FPS)
        ic(fps)

        while True:
            # 저장된 영상 캡쳐
            ret, frame = cap.read()

            # 캡쳐 실패시 실행중단
            if ret is False:
                break

            cv2.imshow('frame', frame)

            # if cv2.waitKey(1) == ord('q'):
            if cv2.waitKey(int(1000/fps)) == ord('q'):
                break

        # 객체핸들 릴리즈
        cap.release()

        # 윈도우 닫기
        cv2.destroyWindow('frame')
        # cv2.destroyAllWindows()


if __name__ == '__main__':
    cam = WebCam()
    # port_list = cam.get_valid_camera_list()
    # ic(port_list)

    # 사용할 웹캠선택
    port_num = 0
    cam.set_port(port_num)

    ################################################################
    # Capture Image(Snapshot)
    ################################################################
    # file_name = f'{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.png'
    # ret, file_name = cam.capture_image(file_name)
    # if ret is True:
    #     ic(file_name)
    # else:
    #     ic('Capture is fail')

    ################################################################
    # Capture Video Stream
    ################################################################
    # cam.capture_video()
    # cam.capture_video(800, 600)
    # cam.capture_video(isMono=True)
    # cam.capture_video(flip=0)
    # cam.capture_video(flip=1)
    # cam.capture_video(isMono=True, flip=1)

    ################################################################
    # Record Video Stream
    ################################################################
    # file_name = f'{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
    # cam.record_video(file_name, 10)
    # cam.record_video(file_name, width=2048, height=1280)

    ################################################################
    # Play Video Stream
    ################################################################
    # cam.play_video('2024_11_22_10_47_10.avi')



















