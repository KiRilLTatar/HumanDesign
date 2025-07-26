import sxtwl
import pytz
from datetime import datetime

STEMS = ["Цзя", "И", "Бин", "Дин", "У", "Цзи", "Гэн", "Синь", "Жэнь", "Гуй"]
BRANCHES = ["Цзы", "Чоу", "Инь", "Мао", "Чэнь", "Сы", "У", "Вэй", "Шэнь", "Ю", "Сюй", "Хай"]

class PillarData:
    def __init__(self, stem, branch):
        self.stem = stem
        self.branch = branch

class Pillar:
    def __init__(self, birth_date, birth_time, tz_name="Etc/GMT-3"):
        self.birth_date = birth_date
        self.birth_time = birth_time
        self.tz_name = tz_name
        self.birth_datetime = self._parse_datetime()
    
    def _parse_datetime(self):
        try:
            timezone = pytz.timezone(self.tz_name)
            birth_dt = datetime.strptime(f"{self.birth_date} {self.birth_time}", "%Y-%m-%d %H:%M")
            return timezone.localize(birth_dt)
        except Exception as e:
            raise ValueError(f"Ошибка обработки даты/времени: {str(e)}")

    def get_bazi(self):
        try:
            calendar = sxtwl.fromSolar(
                self.birth_datetime.year,
                self.birth_datetime.month,
                self.birth_datetime.day
            )

            year_gz = calendar.getYearGZ()
            month_gz = calendar.getMonthGZ()
            day_gz = calendar.getDayGZ()
            hour_gz = calendar.getHourGZ(self.birth_datetime.hour)

            year_pillar = PillarData(STEMS[year_gz.tg], BRANCHES[year_gz.dz])
            month_pillar = PillarData(STEMS[month_gz.tg], BRANCHES[month_gz.dz])
            day_pillar = PillarData(STEMS[day_gz.tg], BRANCHES[day_gz.dz])
            hour_pillar = PillarData(STEMS[hour_gz.tg], BRANCHES[hour_gz.dz])

            return {
                "year_pillar": year_pillar,
                "month_pillar": month_pillar,
                "day_pillar": day_pillar,
                "hour_pillar": hour_pillar
            }
        except Exception as e:
            raise RuntimeError(f"Ошибка расчета столпов судьбы: {str(e)}")