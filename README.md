# ywfm - "You're welcome, future me!"

## Goal
- Python3 script file to execute and work as reminder, target OS for macOS and Linux.
- The program will use `terminal-notifier` for macOS and `notify-send` for Linux.
- The program will take options, `--title <string>`, `--subtitle <string>`, `--open <URL>`, `--command <string>`, `--timer <string>`.

- An example command would be like this:
    ```bash
    > reminder --title "Start building" --subtitle "github auth feat" --open "https://github.com/" --command 'echo hello' --timer 1h10m15s
    ```

