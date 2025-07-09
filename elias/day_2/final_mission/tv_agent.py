# 01. 전원 (Command: k a)
# ▶ 세트의 전원 켜짐/ 꺼짐을 제어합니다.
# Transmission(명령값)
# [k][a][ ][Set ID][ ][Data][Cr]
# Data	00: 꺼짐
#       01: 켜짐
#       ff(FF): 상태값
# ex) ka 01 01, ka 01 00, ka 01 ff

# Acknowledgement(응답값)
# [a][ ][Set ID][ ][OK/NG][Data][x]
# ex) a 01 OK01x, a 01 OK00x, a 01 NG11x
#     a 01 OK01x (켜져있는경우)
#     a 01 OK00x (꺼져있는경우)
# NG인 경우는: 명령어가 잘못된경우, 값이 잘못된경우.
# 처음 시작상태는 poweroff인 상태로 시작
# * 디스플레이의 전원이 완전히 켜진 이후에 정상적인 Acknowledgement 신호가 돌아옵니다.
#
# Extra Mission
# ** Transmission/ Acknowledgement 신호 사이에는 일정시간 지연이 발생할 수 있습니다.
# 'exit'가 입력되면 종료
# 수신된 데이터를 json 포맷으로 저장

# ka 01 00 --> Power Off
# ka 01 01 --> Power On
# ka 01 ff --> Return power status
#
# In terminal
# ka 01 01 --> response a 01 OK01x
# ka 01 00 --> response a 01 OK00x
# ka 01 ff --> response a 01 OK01x or a 01 OK00x

import sys
# sys.path.append('../../day_1/lec_pyserial/')

from lec_pyserial_class import Serial
import json
from datetime import datetime, timedelta
from icecream import ic

RETURN_CODE = b'\x0d'

def main():
    ser = Serial()
    ser.openSerial('com2')
    is_power_on = False

    ic('Program is running...')

    while True:
        # 엔터키가 입력될때까지 데이터를 read
        readed = ser.readUntilExitCode(RETURN_CODE)
        ic(readed)

        # Parsing을 위한 String객체로 Decoding
        readed = readed.decode()
        readed = readed.lower()
        ic(readed)

        # 프로그램 종료확인
        if readed == 'exit':
            ic('Done')
            break

        # ka 01 00
        # ka : command
        # 01 : set id
        # 00 : value (00: Power Off, 01: Power On, FF: Get Current Power Status)
        datalist = readed.split(' ') # 'ka 01 01' --> ['ka', '01', '01']

        # Command Format 점검
        if not(len(readed) == 8 and len(datalist) == 3):
            msg = 'Wrong command format!!!\r\n'
            ic(msg)
            ser.writePortUnicode(msg)
            continue

        command = datalist[0]   # ka
        setId = datalist[1]     # 01
        value = datalist[2]     # 00
        # command, setId, value = datalist # Unpacking
        ic(command, setId, value)

        response = ''

        # 명령어 확인
        if command == 'ka':
            # Power Off
            if value == '00':
                is_power_on = False
                response = f'OK{value}x' # OK00x
                ic(f'Changed power status: {is_power_on}')
            # Power On
            elif value == '01':
                is_power_on = True
                response = f'OK{value}x'
                ic(f'Changed power status: {is_power_on}')
            # Get Current Power Status
            elif value == 'ff':
                response = 'OK01x' if is_power_on is True else 'OK00x'
                ic(f'Current power status: {is_power_on}')
            # Wrong Value
            else:
                response = f'NG{value}x'
                ic(f'Wrong Value!!!')

            # a 01 OK00x
            response = f'{command[1]} {setId} {response}\r\n'
        else:
            msg = 'Not supported command!!!\r\n'
            ic(msg)
            ser.writePortUnicode(msg)
            continue

        # 로그파일 저장
        jsonData = {'command':command, 'setId':setId, 'value':value, 'response':response}
        ic(jsonData)

        jsonString = json.dumps(jsonData) # Dictionary Object --> String Object ('{"command":command, ...})
        # jsonData = json.loads(jsonString) # String Object --> Dictionary Object
        ic(jsonString)

        # [2024-09-11 08:24:11] ....
        # 현재시간
        now = datetime.now()
        ic(now)

        # https://www.geeksforgeeks.org/python-datetime-strptime-function/
        # Datetime Object --> String Object
        now = now.strftime('[%Y-%m-%d %H:%M:%S] ')

        # String Object --> Datetime Object
        # datetime_obj = datetime.strptime('[2024-09-11 08:24:11] ', '[%Y-%m-%d %H:%M:%S] ')

        # f = open(...)
        # f.write(...)
        # f.close()
        with open('command.log', 'a', encoding='utf-8') as f:
            f.write(f'{now}{jsonString}\n')

        ser.writePortUnicode(response)

    ser.closePort()

if __name__ == '__main__':
    main()













