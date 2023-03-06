import sys
import mariadb

device_id = 1
BackUp_USER= {200248706, 200289830}
def check_if_authorized(card):# function returns true if authorized user otherwise false
    print("ENTER")
    if(card in BackUp_USER):
        return True
    try:
        conn = mariadb.connect(
                user="control_client",
                password="testpass",
                host="127.0.0.1",
                port=8081,
                database="Controller_Utility")
        cur = conn.cursor()

        cur.execute("SELECT `id` FROM \
                    `Controller_Utility`.`allowed_users` WHERE \
                    `controller_id` = ? AND `id` = ?", (device_id, card))

        approved = False
        if cur.fetchall():
            approved = True

        cur.execute("INSERT INTO `Logging`.`log` \
                    (`controller_id`, `device_id`, `user`, `event`) VALUES \
                    (?,?,?,?)", (1, 1, card,
                    "Authentication Approved" if approved else
                    "Authentication Failed") )
        conn.commit()
        conn.close()

        return approved

    except mariadb.Error as e:
        print(f"Database connection error: {e}")
        return False
    return False
