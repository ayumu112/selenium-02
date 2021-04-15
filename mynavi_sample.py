import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime
from webdriver_manager.chrome import ChromeDriverManager

# Chromeを起動する関数

def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    #課題2-8
    return Chrome(ChromeDriverManager().install(), options=options)


def log(text):

    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    f = open("log file", "a", encoding='utf-8')

    log_result = (now, text)
    f.write(str(log_result) + '\n')
    print(now, text)
    f.close()

# main処理


def main():

    #課題2-7
    log("取得開始")
    #課題2-4
    search_keyword = input("検索条件を入力して下さい >>>")

    log("検索条件 >>>" + search_keyword )
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)


    # def setup_class(cls):
    #     cls.driver = driver.Chrome(ChromeDriverManager().install())
    #
    # setup_class()
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_table_list = []
    success = 0
    failure = 0
    count = 0
    # 検索結果の一番上の会社名を取得

    #課題2-5

    # 検索結果の一番上の会社名を取得
    name_list = name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
    # 課題2-2 その他の要素を取得
    table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")

    #課題2-3　最後のページまで取得
    while True:

        # 検索結果の一番上の会社名を取得
        name_list = name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        # 課題2-2 その他の要素を取得
        table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")  # 初年度年収

        for name, table in zip(name_list, table_list):
            print(name.text, table.text)

            try:
                exp_name_list.append(name.text)
                exp_table_list.append(table.text)
                success += 1
                log(f"{count}件目成功 : {name.text})")

            except:
                failure += 1
                log(f"{count}件目失敗 : {name.text}")

                pass

            finally:
                count += 1

        if len(driver.find_elements_by_class_name("iconFont--arrowLeft")) > 0:
            driver.find_element_by_class_name("iconFont--arrowLeft").click()
            time.sleep(5)

        else:
            log("最後のページまで完了しました。")
            break

    # # 1ページ分繰り返し
    # print(len(name_list))
    # for name, table in zip(name_list, table_list):
    #     # exp_name_list.append(name.text)
    #     print(name.text)

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
