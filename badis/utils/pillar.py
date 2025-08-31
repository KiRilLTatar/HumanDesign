import sxtwl
import pytz
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

STEMS = ["Цзя", "И", "Бин", "Дин", "У", "Цзи", "Гэн", "Синь", "Жэнь", "Гуй"]
BRANCHES = ["Цзы", "Чоу", "Инь", "Мао", "Чэнь", "Сы", "У", "Вэй", "Шэнь", "Ю", "Сюй", "Хай"]

class PillarData:
    def __init__(self, stem, branch):
        self.stem = stem
        self.branch = branch

class Pillar:
    def __init__(self, birth_date, birth_time, place_name):
        self.birth_date = birth_date
        self.birth_time = birth_time
        self.place_name = place_name
        self.local_tz = self._get_timezone()
        self.birth_datetime_local = self._parse_datetime()
        self.birth_datetime_china = self.birth_datetime_local.astimezone(pytz.timezone("Asia/Shanghai"))
    
    def _get_timezone(self):
        """Определяет таймзону по названию города"""
        geolocator = Nominatim(user_agent="bazi_calc")
        location = geolocator.geocode(self.place_name)
        if not location:
            raise ValueError(f"Не удалось найти место: {self.place_name}")
        
        tf = TimezoneFinder()
        tz_name = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        if not tz_name:
            raise ValueError(f"Не удалось определить таймзону для: {self.place_name}")
        
        return pytz.timezone(tz_name)

    def _parse_datetime(self):
        """Парсит дату/время и локализует к местному часовому поясу"""
        try:
            birth_dt = datetime.strptime(f"{self.birth_date} {self.birth_time}", "%Y-%m-%d %H:%M")
            return self.local_tz.localize(birth_dt)
        except Exception as e:
            raise ValueError(f"Ошибка обработки даты/времени: {str(e)}")

    def get_bazi(self):
        """Считает 4 столпа судьбы (ба-цзы) в пекинском времени"""
        try:
            calendar = sxtwl.fromSolar(
                self.birth_datetime_china.year,
                self.birth_datetime_china.month,
                self.birth_datetime_china.day
            )

            year_gz = calendar.getYearGZ()
            month_gz = calendar.getMonthGZ()
            day_gz = calendar.getDayGZ()
            hour_gz = calendar.getHourGZ(self.birth_datetime_china.hour)

            return {
                "year_pillar": PillarData(STEMS[year_gz.tg], BRANCHES[year_gz.dz]),
                "month_pillar": PillarData(STEMS[month_gz.tg], BRANCHES[month_gz.dz]),
                "day_pillar": PillarData(STEMS[day_gz.tg], BRANCHES[day_gz.dz]),
                "hour_pillar": PillarData(STEMS[hour_gz.tg], BRANCHES[hour_gz.dz]),
            }
        except Exception as e:
            raise RuntimeError(f"Ошибка расчета столпов судьбы: {str(e)}")