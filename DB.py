import sqlite3
#импорт программы для работы с базой данных

class DB_Manager:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        #создание выбранной ячейки, курсора

    def push_game_to_games(self, game_name, game_publisher, game_platform):
        """"добавление игры в таблицу Games"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO `Games` (`GAME_NAME`,`GAME_PUBLISHER`,`GAME_PLATFORM`) VALUES (?,?,?)", ((game_name + ' ' + game_platform), game_publisher, game_platform,))
        #передача парметров в Games
        # return self.conn.commit()

    def push_gamecard_to_gamecards(self, game_name, shop_name, game_price, game_url, game_platform):
        """"добавление товаров в таблицу карточки товара"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO `GameCards` (`GAME_NAME`,`SHOP_NAME`,`GAME_PRICE`,`GAME_URL`,`GAME_PLATFORM`) VALUES (?,?,?,?,?)", ((game_name + game_platform), shop_name, game_price, game_url, game_platform,))
        return self.conn.commit()

    def push_publisher_to_publishers(self, publisher_name):
        """добавление издателя в таблицу издателей"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO `Publishers` (`PUBLISHER_NAME`) VALUES (?)", (publisher_name,))
        return self.conn.commit()

    def push_games_list_to_games(self, games_list):
        """добавление списка игр в таблицу Games"""
        self.cursor.executemany(
            """INSERT OR REPLACE INTO `Games` (`GAME_NAME`,`GAME_PLATFORM`) VALUES (?,?)""",
            games_list)
        return self.conn.commit()

    def push_gamecards_list_to_gamecards(self, gamecards_list):
        """добавление списка товаров в табличку карточки игр"""
        self.cursor.executemany(
            """INSERT OR REPLACE INTO `GameCards` (`GAME_NAME`,`SHOP_NAME`,`GAME_PRICE`,`GAME_URL`,`GAME_STOCK`,`GAME_PLATFORM`) VALUES (?,?,?,?,?,?)""", gamecards_list)
        return self.conn.commit()

    def get_game_list_for_cur_platform(self, platform):
        """получение списка игр для кокретной платформы"""
        #используем для заполнения игры
        result = self.cursor.execute(
            "SELECT `GAME_NAME` FROM `Games` WHERE `GAME_PLATFORM` = ?", (platform,))
        return result.fetchall()

    def get_game_cards(self, game_name):
        """получение всех товаров из кароточек товаров"""
        #используем для вывода в таблицу
        result = self.cursor.execute(
            "SELECT * FROM `GameCards` WHERE `GAME_NAME` = ?", (game_name,))
        return result.fetchall()


    def close(self):
        """Закрываем соединение с БД"""
        self.conn.close()
