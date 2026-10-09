import sqlite3
import pymysql
import os
from config import Config

class Database:
    _active_db_type = None
    _mysql_tested = False
    _mysql_available = False

    @classmethod
    def check_mysql_availability(cls):
        if cls._mysql_tested:
            return cls._mysql_available
        
        cls._mysql_tested = True
        if Config.DB_TYPE.lower() == 'mysql':
            try:
                temp_conn = pymysql.connect(
                    host=Config.MYSQL_HOST,
                    port=Config.MYSQL_PORT,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    connect_timeout=2
                )
                with temp_conn.cursor() as cur:
                    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                temp_conn.close()
                cls._mysql_available = True
                cls._active_db_type = 'mysql'
                print(f"[Database] Connected to MySQL database '{Config.MYSQL_DB}' on {Config.MYSQL_HOST}:{Config.MYSQL_PORT}")
                return True
            except Exception as e:
                print(f"[Database] MySQL connection check: {e}. Defaulting to SQLite for zero-config local runtime.")
                cls._mysql_available = False
                cls._active_db_type = 'sqlite'
                return False
        else:
            cls._mysql_available = False
            cls._active_db_type = 'sqlite'
            return False

    @classmethod
    def get_connection(cls):
        """
        Connects to MySQL if available, otherwise uses SQLite.
        """
        if not cls._mysql_tested:
            cls.check_mysql_availability()

        if cls._mysql_available:
            try:
                conn = pymysql.connect(
                    host=Config.MYSQL_HOST,
                    port=Config.MYSQL_PORT,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DB,
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=True
                )
                cls._active_db_type = 'mysql'
                return conn
            except Exception as e:
                cls._active_db_type = 'sqlite'

        # SQLite
        os.makedirs(os.path.dirname(Config.SQLITE_PATH), exist_ok=True)
        conn = sqlite3.connect(Config.SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        cls._active_db_type = 'sqlite'
        return conn

    @classmethod
    def get_db_type(cls):
        if cls._active_db_type is None:
            cls.get_connection().close()
        return cls._active_db_type

    @classmethod
    def query(cls, sql, params=None, fetchone=False, fetchall=True, commit=False):
        """
        Executes a parameterized SQL query with automatic placeholder normalization:
        Translates %s to ? for SQLite and ? to %s for MySQL.
        """
        conn = cls.get_connection()
        db_type = cls._active_db_type
        params = params or ()

        # Normalize query placeholders
        if db_type == 'sqlite':
            normalized_sql = sql.replace('%s', '?')
        else:
            normalized_sql = sql.replace('?', '%s')

        try:
            cursor = conn.cursor()
            cursor.execute(normalized_sql, params)

            result = None
            if fetchone:
                row = cursor.fetchone()
                if row is not None and db_type == 'sqlite':
                    result = dict(row)
                else:
                    result = row
            elif fetchall:
                rows = cursor.fetchall()
                if db_type == 'sqlite':
                    result = [dict(r) for r in rows]
                else:
                    result = list(rows) if rows else []
            
            if commit or db_type == 'sqlite':
                conn.commit()

            last_id = cursor.lastrowid
            row_count = cursor.rowcount
            cursor.close()
            conn.close()

            if not fetchone and not fetchall:
                return {'lastrowid': last_id, 'rowcount': row_count}
            return result
        except Exception as e:
            conn.close()
            raise e

    @classmethod
    def execute_script(cls, script_content):
        """
        Executes a multi-statement SQL script.
        """
        conn = cls.get_connection()
        db_type = cls._active_db_type
        try:
            if db_type == 'sqlite':
                cursor = conn.cursor()
                cursor.executescript(script_content)
                conn.commit()
                cursor.close()
            else:
                cursor = conn.cursor()
                statements = [s.strip() for s in script_content.split(';') if s.strip()]
                for stmt in statements:
                    cursor.execute(stmt)
                cursor.close()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            raise e
