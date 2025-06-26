import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Система телеоперации манипулятора UR5e'
    )
    parser.add_argument(
        '--task', 
        type=str, 
        default='PickAndPlace',
        help='Название задачи (default: PickAndPlace)'
    )
    parser.add_argument(
        '--control', 
        type=str, 
        default='joystick',
        choices=['joystick', 'android'],
        help='Режим управления (default: joystick)'
    )
    parser.add_argument(
        '--ip', 
        type=str, 
        default=None,
        help='IP-адрес Android устройства (требуется для android режима)'
    )
    
    args = parser.parse_args()
    
    # Checking required parameters
    if args.control == 'android' and not args.ip:
        print("Ошибка: для android режима необходимо указать IP-адрес через --ip")
        sys.exit(1)
    
    # Start command
    command = [sys.executable, "src/teleop_demo.py"]
    
    # Setting environment variables
    env_vars = {
        "TASK_NAME": args.task,
        "CONTROL_MODE": args.control,
    }
    
    if args.ip:
        env_vars["ANDROID_IP"] = args.ip
    
    # Запускаем основной скрипт с параметрами
    try:
        subprocess.run(command, env={**os.environ, **env_vars}, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при запуске программы: {e}")
    except FileNotFoundError:
        print("Ошибка: файл src/teleop_demo.py не найден")

if __name__ == "__main__":
    import os
    main()