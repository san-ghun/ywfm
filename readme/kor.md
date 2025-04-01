# ywfm - "You're welcome, future me!"

> "지금 미래의 자신이 감사할 일을 하세요."

macOS와 Linux에서 네이티브 알림 시스템을 사용하여 지정된 시간 후에 사용자에게 알림을 주는 간단한 Python3 기반 리마인더 도구입니다. 타이머가 종료될 때 URL을 열고 명령을 실행하는 기능도 지원합니다.

## 기능

- **크로스 플랫폼**: macOS(`terminal-notifier` 사용)와 Linux(`notify-send` 사용)에서 작동합니다.
- **맞춤형 알림**: 제목, 메시지, 열 URL 및 실행할 명령을 추가할 수 있습니다.
- **타이머 지원**: `1h10m15s`와 같은 사람이 읽기 쉬운 형식으로 지연 시간을 지정합니다.
- **시각적 피드백**: 진행 표시줄이 있는 리마인더를 시각적으로 실행하는 옵션.
- **백그라운드 실행**: 로깅과 함께 백그라운드 프로세스로 리마인더를 실행하는 옵션.
- **JSON 출력**: 백그라운드에서 실행할 때 JSON 형식으로 리마인더 세부 정보를 출력합니다.
- **최소 시간 제한**: 모든 리마인더에 대해 최소 15초의 시간을 적용합니다.
- **기본 메시지**: 지정되지 않은 경우 친근한 기본 메시지를 제공합니다.
- **로깅**: 백그라운드 프로세스 로그를 `~/.local/state/ywfm/`에 저장합니다.

## 요구 사항

### Python

- Python 3.8 이상
- 진행 표시줄 시각화를 위한 `tqdm` 패키지

### 시스템 의존성

- **macOS**:
  - 알림을 위한 `terminal-notifier`
  - 의존성 설치를 위한 Homebrew(권장)
- **Linux**:
  - 알림을 위한 `notify-send`(libnotify-bin)
  - URL 열기를 위한 `xdg-utils`

## 설치

### 자동 설치

설치 스크립트(`install.py`)는 모든 의존성과 설정을 처리합니다:

1. 저장소를 클론하거나 다운로드
2. 설치 프로그램 실행:

   ```bash
   python3 install.py
   ```

   설치 프로그램은 다음을 수행합니다:

   - 누락된 시스템 의존성 확인
   - 누락된 의존성 설치 전 확인 요청
   - 필요한 Python 패키지 설치
   - PATH에 실행 파일 설정

   참고: 다음이 필요할 수 있습니다:

   - macOS: Homebrew 설치됨 (https://brew.sh)
   - Linux: 패키지 설치를 위한 sudo 권한

3. 설치 프로그램은 다음을 PATH에 추가하는 과정을 안내합니다:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```
   지속성을 위해 이를 쉘 구성 파일(`~/.bashrc`, `~/.zshrc` 등)에 추가하세요.

### 수동 설치

<details>
  <summary>수동 설치 단계를 보려면 클릭하세요</summary>

#### 사전 요구 사항 확인

1. 시스템 의존성 확인:

   - macOS: `which terminal-notifier`
   - Linux: `which notify-send xdg-open`

2. Python 패키지 확인:
   ```bash
   python3 -m pip show tqdm
   ```

#### 시스템 의존성

1. macOS:

   ```bash
   brew install terminal-notifier
   ```

2. Linux:
   ```bash
   sudo apt update
   sudo apt install -y libnotify-bin xdg-utils
   ```

#### Python 의존성

1. 필요한 패키지 설치:
   ```bash
   python3 -m pip install --user tqdm
   ```

#### 스크립트 설치

1. 설치 디렉토리 생성:

   ```bash
   mkdir -p ~/.local/bin
   ```

2. 스크립트를 실행 가능하게 만들고 설치:

   ```bash
   chmod +x main.py
   cp main.py ~/.local/bin/ywfm
   ```

3. PATH에 추가(아직 추가되지 않은 경우):
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # 또는 ~/.zshrc
   source ~/.bashrc  # 또는 ~/.zshrc
   ```
   </details>

## 사용법

```bash
ywfm [-h] [-s SUBJECT] [-m MESSAGE] -t TIMER [-o OPEN_URL] [-c COMMAND] [-p] [-b]
```

### 옵션

| 옵션                   | 설명                                    | 기본값   |
| ---------------------- | --------------------------------------- | -------- |
| `-s` `--subject`       | 리마인더 알림의 제목                    | "ywfm"   |
| `-m` `--message`       | 알림의 메시지                           | 랜덤\*   |
| `-t` `--timer`         | 타이머 지속 시간(예: `1h10m15s`, `10s`) | **필수** |
| `-o` `--open-url`      | 알림이 트리거될 때 열 URL               | 없음     |
| `-c` `--command`       | 타이머가 끝난 후 실행할 명령            | 없음     |
| `-p` `--show-progress` | 진행 표시줄 표시                        | False    |
| `-b` `--background`    | 백그라운드 프로세스로 실행              | False    |

\* 기본 메시지는 "Well done!"과 "You're welcome!" 사이에서 번갈아 표시됩니다.

### 예제

1. **간단한 리마인더**:

   ```bash
   ywfm -t 30m -s "작업 시간" -m "프로젝트 시작"
   ```

2. **타이머에 URL 열기**:

   ```bash
   ywfm -t 10s -s "GitHub 확인" -m "PR 검토" -o "https://github.com"
   ```

3. **명령 실행**:

   ```bash
   ywfm -t 1m -s "빌드" -c 'make clean && make'
   ```

4. **로깅이 있는 백그라운드 프로세스**:

   ```bash
   ywfm -t 2h -s "긴 작업" -b
   ```

   출력:

   ```json
   {
     "pid": 12345,
     "params": {
       "subject": "긴 작업",
       "message": "Well done!",
       "duration": "2h",
       "url": null,
       "command": null,
       "show-progress": false,
       "background": true
     },
     "info": {
       "created_at": "2024-03-21_14:30:00",
       "trigger_at": "2024-03-21_16:30:00",
       "seconds": 7200
     },
     "extra": {
       "os_name": "Darwin",
       "machine": "x86_64",
       "node": "Sanghun.local",
       "platform": "macOS-14.7-x86_64-i386-64bit",
       "description": "[INFO] Output and error message of background process are stored in '~/.local/state/ywfm'."
     }
   }
   ```

5. **진행 표시줄**:
   ```bash
   ywfm -t 10m -s "휴식" -m "커피 타임!" -p
   ```

## 백그라운드 프로세스 관리

백그라운드 모드(`-b`)에서 실행할 때:

- 프로세스 ID(PID)가 JSON 형식으로 출력됩니다
- 로그는 `~/.local/state/ywfm/`에 저장됩니다:
  - `output_[timestamp].log`: 표준 출력
  - `error_[timestamp].log`: 오류 메시지
  - `ywfm.pid`: 현재 프로세스 PID

백그라운드 리마인더를 중지하려면:

```bash
kill $(cat ~/.local/state/ywfm/ywfm.pid)
```

## 제거

1. 실행 파일 제거:

   ```bash
   rm ~/.local/bin/ywfm
   ```

2. 선택 사항: 로그 디렉토리 제거:

   ```bash
   rm -rf ~/.local/state/ywfm
   ```

3. 선택 사항: 의존성 제거:
   - macOS: `brew uninstall terminal-notifier`
   - Linux: `sudo apt remove libnotify-bin xdg-utils`

## 기여

저장소를 포크하고 개선을 위한 풀 리퀘스트를 제출하는 것을 환영합니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다.

## 작성자

박상훈

---

> Thank you, past me.
>
> _Good job, future me._
>
> Well done, past me.
>
> _You're welcome, future me._
>
> Thanks a lot.
