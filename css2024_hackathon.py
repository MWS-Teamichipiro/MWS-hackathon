#使用法: python3 css2024_hackathon.py

import argparse
import socket


# 辞書を読み込む関数
def load_dictionary(dictionary_path):
    print(dictionary_path)
    
    



# パケットを投げる関数
def send_packet(attack_ip):
    print(attack_ip)  
    
    
    

# レポートを出力する関数
def generate_report():
    print("generate_report") 
    
    
    

# メイン関数
def main():
    attack_ip = input("攻撃先のIPアドレスを入力してください: ")
    dictionary_path = input("辞書ファイルのパスを入力してください: ")

    load_dictionary(dictionary_path)
    send_packet(attack_ip)
    generate_report()

if __name__ == "__main__":
    main()