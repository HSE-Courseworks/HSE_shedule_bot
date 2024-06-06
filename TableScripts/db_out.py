import psycopg2


class ScheduleManager:
    def __init__(self, dbname, user, password, host):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host

    def get_schedule_for_group(self, group_name):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host
        )
        cur = conn.cursor()

        try:
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group_id = cur.fetchone()[0]

            cur.execute("""
                SELECT 
                    l.time AS lesson_time, 
                    w.id AS weekday_id,
                    w.name AS weekday_name, 
                    c.name AS classroom_name, 
                    a.name AS address_name,  -- Название адреса (корпуса)
                    s.name AS subject_name, 
                    sch.note AS note,
                    sch.id AS lesson_id
                FROM 
                    schedule sch
                JOIN 
                    lessons l ON sch.lessons = l.id
                JOIN 
                    weekday w ON sch.weekday = w.id
                JOIN 
                    groups g ON sch.groups = g.id
                JOIN 
                    classroom c ON sch.classroom = c.id
                JOIN 
                    address a ON c.color = a.color 
                JOIN 
                    subject s ON sch.subject = s.id
                WHERE 
                    sch.actuality = True AND g.id = %s
            """, (group_id,))

            schedule = cur.fetchall()
            formatted_schedule = [
                {
                    "lesson_time": row[0],
                    "weekday_id": row[1],
                    "weekday_name": row[2],
                    "classroom_name": row[3],
                    "address_name": row[4],
                    "subject_name": row[5],
                    "note": row[6],
                    "lesson_id": row[7]
                }
                for row in schedule
            ]

            return formatted_schedule

        except Exception as e:
            print(e)
            return None

        finally:
            cur.close()
            conn.close()

    def get_weekdays_with_lessons(self, group_name):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host
        )
        cur = conn.cursor()

        try:
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            group_id = cur.fetchone()[0]

            cur.execute("""
                SELECT DISTINCT w.id, w.name
                FROM schedule sch
                JOIN weekday w ON sch.weekday = w.id
                JOIN groups g ON sch.groups = g.id
                WHERE sch.actuality = True AND g.id = %s
                ORDER BY w.id
            """, (group_id,))

            weekdays = cur.fetchall()
            return weekdays

        except Exception as e:
            print(e)
            return []

        finally:
            cur.close()
            conn.close()

    def update_note_for_lesson(self, lesson_id, new_note):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host
        )
        cur = conn.cursor()

        try:
            cur.execute("""
                UPDATE schedule
                SET note = %s
                WHERE id = %s
            """, (new_note, lesson_id))
            conn.commit()
            return True

        except Exception as e:
            print(e)
            return False

        finally:
            cur.close()
            conn.close()

    def switch_actuality_for_lesson(self, lesson_id):
        conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host
        )
        cur = conn.cursor()

        try:
            cur.execute("SELECT actuality FROM schedule WHERE id = %s", (lesson_id,))
            current_actuality = cur.fetchone()[0]
            new_actuality = not current_actuality
            cur.execute("UPDATE schedule SET actuality = %s WHERE id = %s", (new_actuality, lesson_id))
            conn.commit()
            return True

        except Exception as e:
            print(e)
            return False
