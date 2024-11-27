#define RECV_MAX_COUNT  10000

#define PIN_ENA   8
#define PIN_DIR   9
#define PIN_PUL   10

typedef enum _CONVEYOR_STATE {Conveyor_Ready, Conveyor_Run} CONVEYOR_STATE;

unsigned long recv_cnt = 0;
unsigned long time_p = 0;
unsigned long time_serial_p = 0;

unsigned long step_count = 0;
CONVEYOR_STATE state = Conveyor_Ready;

void setup() {
  Serial.begin(115200);  // 시리얼 통신 시작
  Serial.write('s');     // 초기화 메시지

  pinMode(PIN_ENA, OUTPUT);
  pinMode(PIN_DIR, OUTPUT);
  pinMode(PIN_PUL, OUTPUT);

  digitalWrite(PIN_ENA, LOW);
  digitalWrite(PIN_DIR, LOW);
}

void step_run(unsigned long time_c) {
  if ((time_c - time_p) > 2) {
    if (state == Conveyor_Run) {
      // 모터 펄스 신호 생성
      digitalWrite(PIN_PUL, HIGH);
      delayMicroseconds(1000);
      digitalWrite(PIN_PUL, LOW);
      delayMicroseconds(1000);

      step_count--;
      if (step_count <= 0) {
        state = Conveyor_Ready;  // 스텝 카운트 완료 시 대기 상태로 전환
      }

      if ((time_c - time_serial_p) > 50) {
        Serial.write('_');  // 실행 중 상태 표시
        time_serial_p = time_c;
      }
      time_p = time_c;
    } else {
      if ((time_c - time_serial_p) > 50) {
        Serial.write('.');  // 대기 상태 표시
        time_serial_p = time_c;
      }
      time_p = time_c;
    }
  }
}

void loop() {
  unsigned long time_c = millis();

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // 줄 단위로 명령 읽기

    command.trim();  // 문자열 앞뒤 공백 제거
    if (command == "0") {
      // '0' 수신 시 즉시 정지
      state = Conveyor_Ready;
      step_count = 0;
      recv_cnt = 0;  // 입력값 초기화
    } else if (command.toInt() > 0) {
      recv_cnt = command.toInt();
      state = Conveyor_Run;  // 상태를 실행으로 변경
      step_count = recv_cnt;
      recv_cnt = 0;
    }
  }

  step_run(time_c);  // 모터 동작 실행
}
