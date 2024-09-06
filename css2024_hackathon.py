#使用法: python3 css2024_hackathon.py

import argparse
import socket
import concurrent.futures
from tqdm import tqdm


# 辞書を読み込む関数
def load_dictionary(username_path, password_path, attack_ip):
    # ユーザ名とパスワードのリストを読み込む
    with open(username_path, 'r') as user_file:
        usernames = user_file.read().splitlines()
    with open(password_path, 'r') as pass_file:
        passwords = pass_file.read().splitlines()
    
    # 総タスク数を計算
    total_tasks = len(usernames) * len(passwords)
    print(f"Total tasks: {total_tasks}")

    # プログレスバーを初期化
    with tqdm(total=total_tasks) as progress_bar:
        # スレッドプールを作成
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            # 各ユーザ名に対して全てのパスワードを試行
            for username in usernames:
                for password in passwords:
                    futures.append(executor.submit(send_packet, username, password, attack_ip, progress_bar))
            
            # 全てのスレッドが完了するのを待つ
            concurrent.futures.wait(futures)



# パケット送信関数
def send_packet(username, password, attack_ip, progress_bar):
    # パケット送信の処理などよしなに書いて

    # プログレスバーを更新
    progress_bar.update(1)

# レポートを出力する関数
def generate_report():
    print("generate_report") 
    
    
    

# メイン関数
def main():
    attack_ip = input("攻撃先のIPアドレスを入力してください: ")
    username_path = input("ユーザ名ファイルのパスを入力してください: ")
    password_path = input("パスワードファイルのパスを入力してください: ")

    load_dictionary(username_path, password_path, attack_ip)

if __name__ == "__main__":
    main()